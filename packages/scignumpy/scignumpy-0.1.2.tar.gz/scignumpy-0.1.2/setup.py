from setuptools import setup, find_packages

setup(
    name="scignumpy",
    version="0.1.2",  # Update this as needed
    author="Sumedh Patil",
    author_email="admin@aipresso.uk",
    description="A lightweight numerical computation library inspired by NumPy.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/scignumpy",  # Replace with your private GitHub repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy"],  # Add dependencies here
)