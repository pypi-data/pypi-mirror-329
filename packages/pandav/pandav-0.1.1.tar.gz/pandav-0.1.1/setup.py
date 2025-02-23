from setuptools import setup, find_packages

setup(
    name="pandav",  # Your package name
    version="0.1.1",  # Package version
    include_package_data=True,
    packages=find_packages(),  # Automatically detect package
    install_requires=[],  # Dependencies (empty if none)
    author="Pubg Lover",
    author_email="pubglover2511@gmail.com",
    description="A simple Python module with basic functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
)
