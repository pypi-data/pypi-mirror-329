import setuptools

from quantverse.version import __version__

# ---------------------------------------------------------------------------------------------------------
# GENERAL
# ---------------------------------------------------------------------------------------------------------


__name__ = "quantverse"
__author__ = "Julian Blank"
__url__ = "https://anyoptimization.com/projects/quantverse/"

data = dict(
    name=__name__,
    version=__version__,
    author=__author__,
    url=__url__,
    python_requires='>=3.7',
    author_email="blankjul@outlook.com",
    description="quantverse: Quantitative Finance in Python",
    license='GNU AFFERO GENERAL PUBLIC LICENSE (AGPL)',
    keywords="quantitative, finance, stocks, options, ",
    install_requires=["pandas>=2.2"],
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics'
    ]
)


# ---------------------------------------------------------------------------------------------------------
# METADATA
# ---------------------------------------------------------------------------------------------------------


# update the readme.rst to be part of setup
def readme():
    with open('README.rst') as f:
        return f.read()


def packages():
    return ["quantverse"] + ["quantverse." + e for e in setuptools.find_packages(where='quantverse')]


data['long_description'] = readme()
data['packages'] = packages()

setuptools.setup(**data)
