from setuptools import setup, find_packages

setup(
    name="flaskion-cli",
    version="1.0.4",
    author="Graham Patrick",
    author_email="graham@skyaisoftware.com",
    description="A CLI tool to create Flaskion projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GrahamMorbyDev/flaskion",
    packages=find_packages(),
    package_data={"flaskion_cli": ["flaskion_template/**/*"]},
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "flaskion=flaskion_cli.cli:create_project",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)