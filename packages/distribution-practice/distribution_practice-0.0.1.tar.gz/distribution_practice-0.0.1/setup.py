from setuptools import setup, find_packages

with open("readme.md", 'r') as f:
    long_description = f.read()

setup (
    name = "distribution_practice",
    version = "0.0.1",
    description = "A simple library with one function 'add(a, b)'. ",
    packages = find_packages(where="src"),
    package_dir={"": "src"},
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/tdhdjv/DistrubutionPractice",
    author = "tdhdjv",
    license = "Apache Software License",
    classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.13",
    ],
    extras_require = {
        "dev": ["pytest>=8.0", "twine"]
    },
    python_requires=">=3.0"
)