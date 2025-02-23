from setuptools import setup, find_packages

setup(
    name="spssimage",
    version="0.1.0",
    author="Sumedh Patil",
    author_email="sumedh.patil@aipresso.co.uk",
    description="A lightweight library for image creation and manipulation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/spssimage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "Pillow"],
)