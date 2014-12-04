try:
    from setuptools import setup
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")

setup(
    version='0.1',
    url='https://github.com/datamade/parserator',
    description='Create parsers',
    name='parserator',
    packages=['parserator'],
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    install_requires=['python-crfsuite>=0.7',
                      'lxml'],
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
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis'],
    entry_points={
        'console_scripts': [
            'parserator = parserator.main:dispatch',
        ]
    }
)
