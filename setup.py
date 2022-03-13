try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools"
    )


reqs_path = f"{HERE}/requirements.txt"
with open(reqs_path) as reqs_file:
    reqs = reqs_file.read().splitlines()

setup(
    version="0.7.0",
    url="https://github.com/datamade/parserator",
    description="Create parsers",
    name="parserator",
    packages=["parserator"],
    license="The MIT License: http://www.opensource.org/licenses/mit-license.php",
    install_requires=reqs,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    entry_points={
        "console_scripts": [
            "parserator = parserator.main:dispatch",
        ]
    },
)
