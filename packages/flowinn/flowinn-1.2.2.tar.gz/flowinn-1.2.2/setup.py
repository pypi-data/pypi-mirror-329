from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flowinn",
    version="1.2.2",
    author="Jon Errasti Odriozola",
    author_email="errasti13@gmail.com",
    description="fl0wINN: Multi-Scale Turbulent Flow Investigation using Neural Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/errasti13/flowINN",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.26.4',
        'matplotlib>=3.8.3',
        'scipy>=1.13.1',
        'tensorflow>=2.14.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
