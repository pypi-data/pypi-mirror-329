from setuptools import setup, find_packages

setup(
    name="revtools",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["google-generativeai"],
    description="An AI-powered Python module to automatically debug your code using Google's Gemini.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Syed Ahmed Uddin",
    author_email="revdevtools@gmail.com",
    url="https://github.com/PcHelpdone/revtools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)