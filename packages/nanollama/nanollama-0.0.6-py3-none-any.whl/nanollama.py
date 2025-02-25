# Copyright 2025 Josef Albers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import base64
import json
import os
import re
import time
from datetime import datetime
import mlx.core as mx
import mlx.nn as nn
import numpy as np
import tiktoken
from huggingface_hub import snapshot_download
from string import Template
import difflib

CHAT_INIT = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Cutting Knowledge Date: December 2023
Today Date: $date

$system<|eot_id|><|start_header_id|>user<|end_header_id|>

$text<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

CHAT_CONT = """<|eot_id|><|start_header_id|>user<|end_header_id|>

$text<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

FIM_TEMPLATE = """Fill in the missing part of the following code to complete it. Only output the missing part, without explanations, comments, or code fences.

Code until the missing part:
```
{prefix}
```

Code after the missing part:
```
{suffix}
```

Output only the code to complete it."""

def subs(tmp, **kwargs):
    return Template(tmp).safe_substitute(**kwargs)

class Tokenizer:
    def __init__(self, path_tok):
        with open(path_tok) as f:
            ranks = {base64.b64decode(token): int(rank) for token, rank in (line.split() for line in f if line)}
        n_vocab = len(ranks)
        specials = ["<|begin_of_text|>", "<|end_of_text|>", "<|reserved_special_token_0|>", "<|reserved_special_token_1|>", "<|finetune_right_pad_id|>", "<|step_id|>", "<|start_header_id|>", "<|end_header_id|>", "<|eom_id|>", "<|eot_id|>", "<|python_tag|>", *[f"<|reserved_special_token_{2 + i}|>" for i in range(245)]]
        special_tokens = {k:(n_vocab+i) for i,k in enumerate(specials)}
        self.encoding = tiktoken.Encoding(name='jj', explicit_n_vocab=n_vocab + len(special_tokens), pat_str=r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+", mergeable_ranks=ranks, special_tokens=special_tokens)
    def encode(self, lot):
        if isinstance(lot, str):
            lot = [lot]
        return [self.encoding.encode(t, allowed_special='all') for t in lot]
    def decode(self, lol):
        if isinstance(lol[0], int):
            lol = [lol]
        return [self.encoding.decode(l) for l in lol]

class RoPE:
    def __init__(self, cfg):
        dim, base, factor, low, high, omax = cfg['head_dim'], cfg['rope_theta'], cfg['rope_scaling']['factor'], cfg['rope_scaling']['low_freq_factor'], cfg['rope_scaling']['high_freq_factor'], cfg['rope_scaling']['original_max_position_embeddings']
        low_len, high_len = omax/low, omax/high
        freqs = (base ** (np.arange(0, dim, 2) / dim))
        wavelens = 2 * np.pi * freqs
        freqs = np.where(wavelens > low_len, freqs*factor, freqs)
        between = (omax/wavelens - low) / (high - low)
        between = freqs / ((1 - between) / factor + between)
        freqs = np.where((low_len < wavelens) & (wavelens < high_len), between, freqs)
        self._inv_freq = mx.array(1 / freqs)
        self.dtype = eval(f'mx.{cfg['torch_dtype']}')
    def __call__(self, pids):
        freqs = pids[:, None, :, None] @ mx.repeat(self._inv_freq[None, None, None, :], pids.shape[0], axis=0)
        emb = mx.concatenate((freqs, freqs), axis=-1)
        return mx.cos(emb).astype(self.dtype), mx.sin(emb).astype(self.dtype)

class Attention(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        dim = cfg['hidden_size']
        self.n_heads = n_heads = cfg['num_attention_heads']
        self.n_kv_heads = n_kv_heads = cfg['num_key_value_heads']
        self.n_repeat = int(n_heads / n_kv_heads)
        self.head_dim = head_dim = cfg['head_dim']
        self.scale = head_dim**-0.5
        if hasattr(cfg, "attention_bias"):
            attention_bias = cfg['attention_bias']
        else:
            attention_bias = False
        self.q_proj = nn.Linear(dim, n_heads * head_dim, bias=attention_bias)
        self.k_proj = nn.Linear(dim, n_kv_heads * head_dim, bias=attention_bias)
        self.v_proj = nn.Linear(dim, n_kv_heads * head_dim, bias=attention_bias)
        self.o_proj = nn.Linear(n_heads * head_dim, dim, bias=attention_bias)
        self.dtype = eval(f'mx.{cfg['torch_dtype']}')
    def __call__(self, x, rope, mask, cache):
        B, L, D = x.shape
        dtype = x.dtype
        q, k, v = self.q_proj(x), self.k_proj(x), self.v_proj(x)
        q = q.reshape(B, L, self.n_heads, -1).transpose(0, 2, 1, 3)
        k = k.reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)
        v = v.reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)
        q, k = self.apply_rope(q, k, *rope)
        if cache is not None:
            k = mx.concatenate([cache[0], k], axis=2)
            v = mx.concatenate([cache[1], v], axis=2)
        w = (q * self.scale) @ mx.repeat(k, self.n_repeat, axis=1).transpose(0, 1, 3, 2)
        w += mask
        w = mx.softmax(w, axis=-1)
        o = w @ mx.repeat(v, self.n_repeat, axis=1)
        o = o.transpose(0, 2, 1, 3).reshape(B, L, -1)
        return self.o_proj(o).astype(dtype), (k,v)
    def apply_rope(self, q, k, cos, sin):
        q1, q2 = mx.split(q, 2, axis=-1)
        rq = mx.concatenate([-q2, q1], axis = -1)
        k1, k2 = mx.split(k, 2, axis=-1)
        rk = mx.concatenate([-k2, k1], axis = -1)
        return (q * cos + rq * sin).astype(self.dtype), (k * cos + rk * sin).astype(self.dtype)

class MLP(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        dim = cfg['hidden_size']
        hidden_dim = cfg['intermediate_size']
        mlp_bias = cfg['mlp_bias']
        self.gate_proj = nn.Linear(dim, hidden_dim, bias=mlp_bias)
        self.down_proj = nn.Linear(hidden_dim, dim, bias=mlp_bias)
        self.up_proj = nn.Linear(dim, hidden_dim, bias=mlp_bias)
    def __call__(self, x):
        return self.down_proj(nn.silu(self.gate_proj(x)) * self.up_proj(x))

class TransformerBlock(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.self_attn = Attention(cfg)
        self.mlp = MLP(cfg)
        self.input_layernorm = nn.RMSNorm(cfg['hidden_size'], eps=cfg['rms_norm_eps'])
        self.post_attention_layernorm = nn.RMSNorm(cfg['hidden_size'], eps=cfg['rms_norm_eps'])
    def __call__(self, x, rope, mask, cache):
        r, cache = self.self_attn(self.input_layernorm(x), rope=rope, mask=mask, cache=cache)
        h = x + r
        r = self.mlp(self.post_attention_layernorm(h))
        out = h + r
        return out, cache

class LlamaModel(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.embed_tokens = nn.Embedding(cfg['vocab_size'], cfg['hidden_size'])
        self.layers = [TransformerBlock(cfg=cfg) for _ in range(cfg['num_hidden_layers'])]
        self.norm = nn.RMSNorm(cfg['hidden_size'], eps=cfg['rms_norm_eps'])
    def __call__(self, toks, rope, mask, cache):
        h = self.embed_tokens(toks)
        for i, l in enumerate(self.layers):
            h, cache[i] = l(h, rope=rope, mask=mask, cache=cache[i])
        return self.norm(h), cache

class Model(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.model = LlamaModel(cfg)
        self._rope = RoPE(cfg)
        if cfg['tie_word_embeddings']:
            self.tie = True
        else:
            self.tie = False
            self.lm_head = nn.Linear(cfg['hidden_size'], cfg['vocab_size'], bias=False)
    def __call__(self, toks, pids, mask, cache):
        rope = self._rope(pids)
        out, cache = self.model(toks=toks, rope=rope, mask=mask, cache=cache)
        if self.tie:
            return self.model.embed_tokens.as_linear(out), cache
        return self.lm_head(out), cache
    @property
    def layers(self):
        return self.model.layers

def find_added_lines(old_string, new_string):
    diff = list(difflib.unified_diff(
        old_string.rstrip().splitlines(keepends=False),
        new_string.rstrip().splitlines(keepends=False),
        n=0, 
        lineterm=''
    ))
    diff = diff[2:]
    added_lines = []
    for line in diff:
        if line.startswith('+'):
            added_lines.append(line[1:])
    return '\n'.join(added_lines)

def remove_fence(s):
    o = ''
    for i in s.splitlines(keepends=True):
        if '```' not in i:
            o += i
    return o

class Chat:
    def __init__(self, model_path='llama_32_1b_it', system='', c=34, fim_template=FIM_TEMPLATE, think='noop', max_kv_size='noop', dict_repo='noop', cache_dir='noop'):
        path_hf = snapshot_download(repo_id='JosefAlbers/llama', allow_patterns=[f'{model_path}*'])
        with open(f'{path_hf}/{model_path}_config.json', 'r') as f:
            cfg = json.load(f)
        model = Model(cfg)
        model.load_weights(f'{path_hf}/{model_path}_model.safetensors', strict=False)
        model.eval()
        mx.eval(model)
        self.dtype = eval(f'mx.{cfg['torch_dtype']}')
        self.model = model
        self.tokenizer = Tokenizer(f'{path_hf}/{model_path}.tiktoken')
        self.num_layers = cfg['num_hidden_layers']
        self.c = c
        self.fim_template = fim_template
        self.reset(system=system)
    def get_ntok(self, s):
        return len(self.tokenizer.encode(s)[0])
    def reset(self, system='', max_kv_size='noop'):
        self.system = system
        self.toks = None
        self.cache = None
        self.mask = None
        self.stop = None
        self.pids = 0
        self.hx = []
    def fim(self, prefix, suffix, max_new=500, current_path='noop'):
        self.reset()
        prompt = self.fim_template.format(prefix=prefix, suffix=suffix)
        response = self.__call__(inputs=prompt, max_new=max_new, chat_fmt=True, verbose=False, stream=None)
        autocomplete = remove_fence(response['text'])
        autocomplete = find_added_lines(''.join([prefix,suffix]), autocomplete)
        self.reset()
        return dict(autocomplete=autocomplete, prompt=prompt, prefix=prefix, suffix=suffix, dict_repo={'noop':'noop'})
    def set_cache_repo(self, dict_repo, cache_dir='noop', max_kv_size='noop'):
        return 'noop'
    def __call__(self, inputs, max_new=500, chat_fmt=True, verbose=False, stream=None):
        if isinstance(inputs, str):
            if len(inputs) == 0:
                return self.resume(max_new=max_new, verbose=verbose, stream=stream)
            inputs = [inputs]
        assert len(inputs) == 1, 'Batching is not implemented yet'
        if chat_fmt:
            chat_fmt = CHAT_INIT if self.cache is None else CHAT_CONT
            chat_fmt = subs(chat_fmt, date=datetime.now().strftime('%d %b %Y'), system=self.system)
            inputs = [subs(chat_fmt, text=i) for i in inputs]
        toks = self.tokenizer.encode(inputs)
        return self.generate(inputs, toks, max_new=max_new, verbose=verbose, stream=stream)
    def resume(self, max_new=500, verbose=False, stream=None):
        if self.stop == 'len':
            return self.generate([''], self.toks, max_new=max_new, verbose=verbose, stream=stream)
        return dict(text='', outputs=[''], benchmark='n/a', stop=self.stop)
    def generate(self, inputs, toks, max_new, verbose, stream):
        tic = time.perf_counter()
        toks, pids, mask = self.pad_to_batch(toks)
        ntok_i = toks.size
        cache = [None] * self.num_layers if self.cache is None else self.cache
        result = mx.zeros((toks.shape[0],0), dtype=mx.uint32)
        goon = mx.ones((toks.shape[0],1), dtype=mx.bool_)
        f = None
        if isinstance(stream, str):
            try:
                f = open(stream, "a", encoding="utf-8")
            except:
                f = None
        idx_sofar = 0
        stop = 'len'
        for i in range(max_new):
            toks, cache = self.model(toks=toks, pids=pids, mask=self.get_mask(mask, toks.shape[-1]), cache=cache)
            toks = mx.argmax(toks[:,-1,:], axis=-1, keepdims=True)
            mx.eval(toks, cache)
            result = mx.concatenate([result, toks], axis=-1)
            pids = pids[:,-1:]+1
            goon *= (toks != 128009)
            mask = mx.pad(mask, ((0,0), (0, 1)), constant_values=1)
            if stream and i % 10 == 2:
                txt = self.tokenizer.decode(result.tolist())[0]
                idx_split = txt.rfind(' ', idx_sofar)
                if idx_split > 0:
                    frag = txt[idx_sofar:idx_split]
                    if f:
                        f.write(frag)
                        f.flush()
                    else:
                        print(frag, end='', flush=True)
                    idx_sofar = idx_split
            if goon.sum() < 1:
                stop='stop'
                break
        outputs = self.tokenizer.decode(result.tolist())
        self.stop = stop
        if stream:
            if f:
                f.write(outputs[0][idx_sofar:])
                f.flush()
                f.close()
            else:
                print(outputs[0][idx_sofar:], end='', flush=True)
                print()
        self.toks = toks.tolist()
        self.cache = cache
        self.mask = mask[:,:-1]
        self.pids = pids
        self.hx += inputs + outputs
        ntok_o = result.size
        benchmark = f'{ntok_i} input and {ntok_o} output tokens in {time.perf_counter()-tic:.2f} seconds'
        if verbose:
            print(f'\033[{self.c-3}m{'\n\n---\n\n'.join(inputs)}\033[0m---\n\n\033[{self.c}m{'\n\n---\n\n'.join(outputs)}\033[0m\n\n---\n\n{benchmark}')
        text = outputs[0][:-10].strip() if stop == 'stop' else outputs[0].strip()
        return dict(text=text, outputs=outputs, hx=self.hx, benchmark=benchmark, stop=stop)
    def pad_to_batch(self, input_ids):
        max_length = max(len(sublist) for sublist in input_ids)
        toks = mx.array([[128009]*(max_length-len(sublist)) + sublist for sublist in input_ids])
        pids = mx.array([[1]*(max_length-len(sublist)) + list(range(len(sublist))) for sublist in input_ids])
        mask = mx.array([[False]*(max_length-len(sublist)) + [True]*len(sublist) for sublist in input_ids])
        if self.cache is not None:
            pids += self.pids
            mask = mx.concatenate([self.mask, mask], axis=-1)
        return toks, pids, mask
    def get_mask(self, mask, trunc):
        _mask = mx.triu(mx.full((mask.shape[-1], mask.shape[-1]), -mx.inf), k=1)
        _mask += mx.where(mask[:, None, :, None]*mask[:, None, None, :], 0, -mx.inf)
        _mask = _mask[...,-trunc:,:]
        return _mask.astype(self.dtype)

def add_text(input_string):
    def get_text(match):
        filename = match.group(1)
        try:
            with open(filename, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return f"Error: {filename} not found."
        except Exception as e:
            return f"An error occurred: {e}"
    output_string = re.sub(r'\{([^}]+)\}', get_text, input_string)
    return output_string

def main():
    parser = argparse.ArgumentParser(description='jj')
    parser.add_argument('input', type=str, nargs='*')
    parser.add_argument('-s', '--system', type=str, default='')
    parser.add_argument('-p', '--model_path', type=str, default='uncn_llama_32_3b_it')
    parser.add_argument('-hx', '--history', type=str, default='history.json')
    parser.add_argument('-r', '--resume', type=int, default=-1)
    parser.add_argument('-m', '--max', type=int, default=5000)
    parser.add_argument('-t', '--test', action='store_true')
    args = parser.parse_args()
    if args.test:
        return test()
    chat = Chat(model_path=args.model_path, system=args.system)
    user_input = ' '.join(args.input)
    if len(user_input) < 1:
        user_input = input('# ')
    user_input = add_text(user_input)
    history=args.history
    chat_fmt = True
    if os.path.exists(history):
        with open(history, 'r') as f:
            hx = json.load(f)
        if args.resume >= 0:
            idx_ctx = sorted(hx, key=int, reverse=True)[0] if args.resume == 0 else str(args.resume)
            user_input = hx[idx_ctx] + subs(CHAT_CONT[10:], text=user_input)
            chat_fmt = False
            print(f'= {user_input}')
    else:
        hx = {}
    while user_input != 'q':
        llm_output = chat(user_input, verbose=False, chat_fmt=chat_fmt, max_new=args.max)['text']
        print(f'\033[34m{llm_output}\033[0m') #\n\n---\n\n{benchmark}')
        user_input = input('# ')
        user_input = add_text(user_input)
        chat_fmt = True
    hx[datetime.now().strftime('%Y%m%d%H%M%S')] = ''.join(chat.hx)
    with open(history, "w") as f:
        json.dump(hx, f, indent=4)

def test_fim():
    prefix = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]"""
    suffix = """middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
    """
    chat = Chat()
    a = chat.fim(prefix=prefix, suffix=suffix)
    print(a['autocomplete'])

if __name__ == '__main__':
    main()
