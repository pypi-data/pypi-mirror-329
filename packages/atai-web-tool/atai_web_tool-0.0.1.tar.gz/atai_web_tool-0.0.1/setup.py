# setup.py
from setuptools import setup, find_packages

setup(
    name="atai-web-tool",
    version="0.0.1",
    description="Extract the main content from a webpage using zendriver, readability-lxml, and BeautifulSoup.",
    author="AtomGradient",
    author_email="alex@atomgradient.com",
    url="https://github.com/AtomGradient/atai-web-tool",
    packages=find_packages(),
    install_requires=[
        "zendriver",
        "readability-lxml",
        "beautifulsoup4",
        "lxml[html_clean]"
    ],
    entry_points={
        "console_scripts": [
            "atai-web-tool = atai_web_tool.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
