from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='nanollama',
    url='https://github.com/JosefAlbers/nanollama32',
    py_modules=['nanollama'],
    packages=find_packages(),
    version='0.0.6',
    readme="README.md",
    author_email="albersj66@gmail.com",
    description="Nano Llama",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Josef Albers",
    license="MIT",
    python_requires=">=3.12.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nlm = nanollama:main",
        ],
    },
)
