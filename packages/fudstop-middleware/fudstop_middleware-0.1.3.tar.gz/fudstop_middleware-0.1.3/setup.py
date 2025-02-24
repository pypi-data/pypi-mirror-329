from setuptools import setup, find_packages

setup(
    name="fudstop_middleware",  # Package name on PyPI
    version="0.1.3",  # Increment version for updates
    author="Charlies Vids",
    author_email="chuckdustin12@gmail.com",
    description="A middleware for seamless integration of financial APIs like Polygon, Webull, OCC, and more.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fudstop_middleware",  # Update with your GitHub repo
    packages=find_packages(),
    install_requires=[
        "requests",
        "asyncpg",
        "aiohttp",
        "pandas",
        "numpy",
        "disnake",
        "discord_webhook",
    ],  # List your dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Minimum Python version
)
