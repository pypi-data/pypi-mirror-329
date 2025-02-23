from setuptools import setup, find_packages

# Read README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pastit-cli",
    version="1.0.5",
    author="harryeffinpotter",
    author_email="your.email@example.com",  # Add your email here
    description="A command-line tool for quickly sharing files and text snippets using a Zipline server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harryeffinpotter/pastit",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'python-dotenv>=1.0.0',
        'rich>=13.7.0',
    ],
    entry_points={
        'console_scripts': [
            'pasta=pastit_cli.pasta:main',
            'pastit=pastit_cli.pastit:main',
            'pastit-setup=pastit_cli.setup_cmd:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
)
