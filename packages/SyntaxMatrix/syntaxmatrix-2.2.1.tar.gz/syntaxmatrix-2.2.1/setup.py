from setuptools import setup, find_packages
import os

# Read the README for a long description (ensure you have a README.md in your project root)
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="SyntaxMatrix",
    version="2.2.1",
    author="Bob Nti",
    author_email="bob.nti@syntaxmatrix.com",
    description="SyntaxMUI: A customisable UI framework for Python AI Assistant Projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bobganti/SyntaxMatrix", 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "openai"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


# from setuptools import setup, find_packages

# setup(
#     name="syntaxmatrix",
#     version="0.1.0",
#     packages=find_packages(),
#     install_requires=[
#         "flask",
#         # Add other dependencies here
#     ],
#     author="Your Name",
#     description="A UI framework for RAG projects",
#     license="MIT",
# )
