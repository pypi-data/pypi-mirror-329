from setuptools import setup, find_packages

setup(
    name="vinehoollm",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "socksio>=1.0.0",
    ],
    author="Vinehoo",
    author_email="wei.du@vinehoo.com",
    description="A Python package for interacting with OpenAI-compatible LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vinehoo/vinehoollm",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 