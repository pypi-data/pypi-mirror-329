from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ownerrez-wrapper",
    version="0.1.0",
    author="Geody Moore",
    author_email="geody.moore@gmail.com",
    description="A Python wrapper for the OwnerRez API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmoorevt/ownerrez-wrapper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.25.0",
        "python-dateutil>=2.8.0",
        "python-dotenv>=1.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=3.9.0",
            "mypy>=0.900",
            "freezegun>=1.2.0"
        ]
    },
    entry_points={
        'console_scripts': [
            'ownerrez=ownerrez_wrapper.cli:main',
        ],
    },
)
