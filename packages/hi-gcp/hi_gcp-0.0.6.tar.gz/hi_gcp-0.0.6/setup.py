from setuptools import setup, find_packages

setup(
    name="hi-gcp",
    version="0.0.6",
    author="J L",
    author_email="jliu5277@gmail.com",
    description="GCP Utilities for BigQuery",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/xileven",
    py_modules=["hi_gcp"],  
    install_requires=[
        "google-cloud-bigquery>=3.27.0",
        "google-cloud-storage>=2.18.2",
        "pandas>=2.2.3",
        "numpy>=2.0.2",
        "pandas-gbq>=0.24.0",
        "pyarrow>=18.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)

# python3 -m build
# twine upload dist/*
# twine upload dist/hi_gcp-0.0.5*