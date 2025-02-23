from setuptools import setup, find_packages

setup(
    name="spssstar",
    version="0.1.1",
    author="Sumedh Patil",
    author_email="sumedh.patil@aipresso.co.uk",
    description="A library for encoding session-specific data into star maps.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/spssstar",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["hashlib"],
)