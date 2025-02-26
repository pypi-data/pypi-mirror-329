from setuptools import setup, find_packages

setup(
    name="mycalculator112",  # Unique package name
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    author="mdsaif",
    author_email="mdsaifkhan200@gmail.com",
    description="A simple calculator package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mycalculator112",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
