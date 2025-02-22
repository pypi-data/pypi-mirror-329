from setuptools import setup, find_packages

setup(
    name="glad-kit",  # Unique package name
    version="0.1.0",  # Start with a small version
    author="Navthej",
    author_email="gladgamingstudio@gmail.com",
    description="This library makes your lifes easier, it contains three librarys inside it for maths, text editing(fg,bg,design ' and more ')(on terminal) and file managing, create, delete, rename, copy, paste and more",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)