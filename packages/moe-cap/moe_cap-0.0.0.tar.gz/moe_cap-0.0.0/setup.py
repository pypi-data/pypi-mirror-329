from setuptools import setup, find_packages

setup(
    name="moe-cap",
    version="0.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "moe_cap"},
    install_requires=[
        # Add your dependencies here
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/moe-cap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 