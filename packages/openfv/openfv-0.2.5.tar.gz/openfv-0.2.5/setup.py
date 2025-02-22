from setuptools import setup, find_packages

setup(
    name="openfv",
    version="0.2.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'scipy',
    ],
    author="Wonwoo Park",
    author_email="bemore.one@gmail.com",
    description="computer vision packages in frequency domain",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bemoregt/openfv",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
)
