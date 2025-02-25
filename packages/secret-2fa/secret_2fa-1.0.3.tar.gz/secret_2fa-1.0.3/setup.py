from setuptools import setup, find_packages

setup(
    name="secret_2fa",
    version="1.0.3",
    packages=find_packages(),

    install_requires=[
        "pyppeteer",
    ],
    author="Nguyễn Minh Đức",
    author_email="dancntt7@mail.com",
    description="A library for handling secret 2fa authentication using Pyppeteer.",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
