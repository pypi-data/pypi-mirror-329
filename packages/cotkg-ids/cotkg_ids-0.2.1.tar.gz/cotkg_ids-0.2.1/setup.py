from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of LICENSE file
with open("LICENSE", "r", encoding="utf-8") as fh:
    license_text = fh.read()

setup(
    name="cotkg_ids",
    version="0.2.1",
    author="Xingqiang Chen",
    author_email="xingqiang.chen@outlook.com",
    description="A package for intrusion detection using chain of thought and knowledge graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenxingqiang/CoTKG-IDS",
    project_urls={
        "Bug Tracker": "https://github.com/chenxingqiang/CoTKG-IDS/issues",
        "Documentation": "https://github.com/chenxingqiang/CoTKG-IDS",
        "Source Code": "https://github.com/chenxingqiang/CoTKG-IDS",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.5",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.2",
        "torch>=1.9.0",
        "networkx>=2.6.3",
        "matplotlib>=3.4.3",
        "tqdm>=4.62.3",
        "torch-geometric>=2.0.0",
        "transformers>=4.11.3",
        "openai>=0.27.0",
        "dashscope>=1.13.6",
        "ollama>=0.1.6",
    ],
    package_data={
        "cotkg_ids": ["config/*.py"],
    },
    exclude_package_data={
        "": ["data/*"],
    },
    entry_points={
        "console_scripts": [
            "cotkg-ids=cotkg_ids.main:main",
        ],
    },
)
