from setuptools import setup, find_packages
import os

version = os.getenv("PACKAGE_VERSION", "0.1.0")

setup(
    name="python_viu_api",  # Keep this as your package name
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio",
    ],
    extras_require={ 
        "dev": [
            "grpcio-tools",
            "betterproto[compiler]", # Put build/dev dependencies here
            "pytest",          # For testing
            "pytest-asyncio",  # For testing async code
            "twine",
        ]
    },
    author="Michael Weber",
    author_email="info@searchviu.com",
    description="gRPC client for VIU API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/VIU-one/python-viu-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # It is a good practice to include license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Modernize to 3.8+ (or your minimum supported version)
)
