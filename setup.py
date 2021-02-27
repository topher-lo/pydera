from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name='pydera',
    version='0.0.2',
    description='Tools for downloading and processing aggregated datasets from'
                ' the SEC\'s Division of Economic and Risk Analysis',
    packages=['getdera'],
    install_requires=["numpy",
                      "pandas",
                      "requests",
                      "requests-toolbelt",
                      "tqdm"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    tests_require=["pytest"],
    extras_require={
        "dev": [
            "pytest",
            "responses",
            "check-manifest",
            "wheel",
        ]
    },
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://topher-lo.github.io/pydera/getdera/",
        "Issues": "https://github.com/topher-lo/pydera/issues",
    },
    url="https://github.com/topher-lo/pydera",
    author="Christopher Lo",
    author_email="lochristopherhy@gmail.com",
)
