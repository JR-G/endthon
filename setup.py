from setuptools import setup, find_packages

setup(
        name="endthon",
        version="0.1.0",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        install_requires=[],
        entry_points={
            "console_scripts": [
                "endthon=endthon.runner:main",
                ],
        },
        author="James Glenn",
        author_email="",
        description="Python but with explicit end",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/JR-G/endthon",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires=">=3.6",
        )
