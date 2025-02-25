from setuptools import setup, find_packages

setup(
    name="magento-dump",  #Package name
    version="1.0.15",
    packages=find_packages(where='src'),  # Automatically find and include all packages
    package_dir={'': 'src'},  # Tell setuptools to look in src
    install_requires=[
        "tqdm", 
        "simple-term-menu",
    ],
    entry_points={
        "console_scripts": [
            "magento-dump=magento_dump:main",  #CLI command
            "magento-dump-tool=magento_dump:main",  #Alternative CLI command
        ],
    },
    author="Yehor Shytikov",
    author_email="egorshitikov@gmail.com",
    description="Magento Database Dump & Table Analyzer Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/genakermkdir/magento-dump",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
