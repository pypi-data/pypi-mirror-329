from setuptools import setup, find_packages

setup(
    name="simplex",
    version="1.2.33",
    packages=find_packages(),
    package_data={
        "simplex": ["browser_agent/dom/*.js"],  # Include JS files in the dom directory
    },
    install_requires=[
        "colorama",
        "requests",
        "python-dotenv",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'simplex=simplex.cli:main',
        ],
    },
    author="Simplex Labs, Inc.",
    author_email="founders@simplex.sh",
    description="Official Python SDK for Simplex API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://simplex.sh",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.9",
) 