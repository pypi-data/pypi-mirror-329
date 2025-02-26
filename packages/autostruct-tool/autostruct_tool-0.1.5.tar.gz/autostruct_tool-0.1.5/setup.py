from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autostruct-tool",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[],  # No external dependencies
    entry_points={
        "console_scripts": [
            "autostruct=autostruct.creator:main",  # CLI command
        ],
    },
    author="Amandeep Singh",
    author_email="amandeep.singh.dsc@gmail.com",
    description="A tool to create directory structures from text files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amandeepsingh29/autostruct",
    license="MIT",
    license_files=["LICENSE"],  # Explicitly include your LICENSE file
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
