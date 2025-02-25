from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TIRAI",
    # Update this version number for new releases
    # Format: MAJOR.MINOR.PATCH (e.g., 0.1.0)
    # - MAJOR: Incompatible API changes
    # - MINOR: Add functionality in a backwards-compatible manner
    # - PATCH: Backwards-compatible bug fixes
    version="0.2.0",
    author="The I Research",
    author_email="jl@theiresearch.com",
    description=
    "The I Research AI Tools - A unified SDK for various AI model providers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheIResearch/tirai-sdk",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "typing-extensions>=4.0.0",
    ],
    keywords="ai, sdk, openai, grok, deepseek, azure",
)
