try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(<requirements_path>)

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

setup(
    version='0.3',
    url='https://github.com/datamade/parserator',
    description='Create parsers',
    name='parserator',
    packages=['parserator'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=['python-crfsuite>=0.7',
                      'lxml',
                      'unidecode'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    entry_points={
        'console_scripts': [
            'parserator = parserator.main:dispatch',
        ]
    }
)
