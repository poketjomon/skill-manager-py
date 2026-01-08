#!/usr/bin/env python3
"""Setup configuration for Claude Skill Manager (Python version)"""

from setuptools import setup

setup(
    name="claude-skill-manager",
    version="2.0.0",
    description="Search, browse, and install Claude Code skills from a database of 31,767+ community skills with intelligent SVN/Git downloads",
    long_description=open("../README.md", "r", encoding="utf-8").read()
    if __name__ == "__main__"
    else "",
    long_description_content_type="text/markdown",
    author="Claude Skill Manager",
    license="MIT",
    url="https://github.com/yourusername/skill-manager",
    python_requires=">=3.7",
    py_modules=["index"],
    entry_points={
        "console_scripts": [
            "skill-manager=index:main",
        ],
    },
    keywords=[
        "claude",
        "claude-code",
        "skills",
        "ai",
        "assistant",
        "package-manager",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
