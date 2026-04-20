"""
Yogacara - The Awakening Engine for AI Agents

An open-source framework that enables AI agents to truly evolve through
the ancient wisdom of Yogacara Buddhism.

:copyright: (c) 2024 Juexin
:license: MIT License
"""

from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yogacara",
    version="0.1.0",
    author="Juexin",
    author_email="juexin@example.com",
    description="The Awakening Engine for AI Agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yogacara/yogacara",
    project_urls={
        "Bug Reports": "https://github.com/yogacara/yogacara/issues",
        "Source": "https://github.com/yogacara/yogacara",
        "Documentation": "https://yogacara.readthedocs.io",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
        "cli": [
            "click>=8.0.0",
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yogacara=yogacara.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
