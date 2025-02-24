from setuptools import setup, find_packages

setup(
    name="cobiformulate",
    version="0.84",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    author="William Cho",
    author_email="william.cho@cobi.tech",
    description="Create and solve optimization problems. Property of COBI Inc.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cobi-inc/CobiCloud/tree/main",  # Change to your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
