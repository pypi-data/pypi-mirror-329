from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yoix-pi",
    version="0.1.0",
    author="Alex Crocker",
    description="BBEdit-style persistent includes for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/crock/yoix-pi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click>=8.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'yoixpi=yoix_pi.cli:main',
        ],
    },
)
