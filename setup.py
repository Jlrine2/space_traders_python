import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="space_traders_python",
    version="0.0.1",
    author="James Rine",
    description="A collection of reusable AWS CDK constructs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jlrine2/python_aws_constructs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        'aws-cdk-lib==2.0.0',
        'constructs>=10.0.0,<11.0.0',
        'aws-cdk.aws-lambda-python-alpha',
        'aws-cdk.aws-apigatewayv2-alpha'
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)