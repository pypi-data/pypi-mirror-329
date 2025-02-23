from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sais-prism-sdk",
    version="0.1.0-beta",
    author="Shepard",
    author_email="zhaoxun@sais.com.cn",
    description="Unified ML Lifecycle Management SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab-paas.internal.sais.com.cn/data_intelligence_platform/sais-prism",
    packages=find_packages(),
    install_requires=[
        "mlflow>=2.0.0",
        "PyYAML>=6.0",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "peft>=0.4.0",
    ],
    extras_require={
        "test": ["pytest>=7.0.0", "pytest-cov>=4.0.0", "pytest-mock>=3.10.0"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
