import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="space_traders_python",
    version="0.0.1",
    author="James Rine",
    description="Python SDK for Space Traders Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jlrine2/space_traders_python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'python-dateutil',
        'requests'
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
