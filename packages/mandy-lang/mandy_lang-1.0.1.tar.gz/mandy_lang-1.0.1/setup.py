from setuptools import setup, find_packages

setup(
    name="mandy-lang",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "mandyc=mandy_lang.main:main",
        ],
    },
    install_requires=[],
)
