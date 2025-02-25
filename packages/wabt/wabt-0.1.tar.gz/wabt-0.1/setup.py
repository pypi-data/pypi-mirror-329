from setuptools import setup, find_packages

setup(
    name="wabt",
    version="0.1",
    description="A Python wrapper for the WebAssembly Binary Toolkit (WABT)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="c7a2d9e (dropout)",
    author_email="c7a2d9e@sys32.dev",
    url="https://github.com/c7a2d9e/wabt-py",
    packages=find_packages(),
    install_requires=["requests>=2.32.3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)