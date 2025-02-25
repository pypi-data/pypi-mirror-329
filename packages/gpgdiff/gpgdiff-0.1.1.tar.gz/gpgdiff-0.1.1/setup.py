from setuptools import setup, find_packages

setup(
    name="gpgdiff",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ]
    },
    entry_points={
    'console_scripts': [
            'gpgdiff=gpg_diff.gpgdiff:main',
        ],
    },
    package_data={
        'gpgdiff': [],
    },
    author="ubuntupunk",
    author_email="ubuntupunk@gmail.com",
    description="A gpg diff utility",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ubuntupunk/gpgdiff",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
)
