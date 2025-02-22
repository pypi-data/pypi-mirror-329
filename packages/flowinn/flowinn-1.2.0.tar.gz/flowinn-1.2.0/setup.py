from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flowinn",
    version="1.2.0",
    packages=find_packages(include=['flowinn', 'flowinn.*']),
    install_requires=[
        'numpy>=1.26.4',
        'matplotlib>=3.8.3',
        'scipy>=1.13.1',
        'tensorflow>=2.18',
        'h5py>=3.8.0',
        'scikit-learn>=1.0.0',
    ],
    author="Jon Errasti Odriozola",
    author_email="errasti13@gmail.com",
    description="fl0wINN: Multi-Scale Turbulent Flow Investigation using Neural Networks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/errasti13/flowINN",
    project_urls={
        "Bug Tracker": "https://github.com/errasti13/flowINN/issues",
        "Documentation": "https://flowinn.readthedocs.io/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
