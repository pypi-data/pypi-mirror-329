import setuptools

setuptools.setup(
    name="QAnglesKit",
    version="0.0.4.3",
    author="saipranay",
    author_email="saipranay57@gmail.com",
    description="A Python client library for interacting with quantum job details",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Correct Python version specifier
    install_requires=[
        "pymongo",
        "python-dotenv",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "mypackage-cli=mypackage.db_handler:main",  # Optional CLI command
        ],
    },
)


