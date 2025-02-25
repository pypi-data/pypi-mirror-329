from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="gpgdiff",
    version="0.1.2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
       'rich',
       'difflib',
       'argparse',
       're',
       'subprocess',
       'tempfile',
        ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/gpgdiff",
    author="David Robert Lewis",
    author_email="ubuntupunk@gmail.com",
    keywords='revoke, gpg, diff',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ],
    entry_points={
    'console_scripts': [
            'gpgdiff=gpg_diff.gpgdiff:main',
        ],
     },   
    python_requires=">=3.6",
)
