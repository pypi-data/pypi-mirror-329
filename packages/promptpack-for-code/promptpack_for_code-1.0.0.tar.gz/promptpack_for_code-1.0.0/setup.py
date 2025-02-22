import os
import re
from setuptools import setup, find_packages

def read_version():
    """Read version from __init__.py"""
    version_file = os.path.join(
        os.path.dirname(__file__),
        'src',
        'promptpack_for_code',
        '__init__.py'
    )
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']',
                            content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="promptpack-for-code",
    version=read_version(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["tqdm"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "promptpack-for-code=promptpack_for_code.__main__:main",
        ],
    },
    author="Yuan-Yi Chang",
    author_email="changyy.csie@gmail.com",
    description="A tool to bundle code files into a single file for AI analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/changyy/py-promptpack-for-code",
    project_urls={
        "Bug Tracker": "https://github.com/changyy/py-promptpack-for-code/issues",
        "Documentation": "https://github.com/changyy/py-promptpack-for-code#readme",
        "Source Code": "https://github.com/changyy/py-promptpack-for-code",
    },
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # Environment
        "Operating System :: OS Independent",
        
        # Topics
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    keywords="ai, code-review, static-analysis, development-tools",
)
