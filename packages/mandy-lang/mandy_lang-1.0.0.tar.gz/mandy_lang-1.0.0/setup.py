from setuptools import setup, find_packages

setup(
    name="mandy-lang",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mandyc=mandy.main:compile",
            "mandy=mandy.main:run"
        ]
    },
    author="Mandar Dadhich",
    author_email="your-email@example.com",
    description="Mandy Programming Language - A simple interpreted language.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-github/mandy-lang",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
