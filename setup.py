from setuptools import setup

setup(
    name='pydera',
    version='0.0.1',
    description='Tools for downloading and processing aggregated datasets from'
                ' the SEC\'s Division of Economic and Risk Analysis',
    packages=['getdera'],
    install_requires=["numpy",
                      "pandas",
                      "requests",
                      "requests-toolbelt",
                      "tqdm",
                      "zipfile"],
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

)
