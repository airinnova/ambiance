import setuptools
from src.ambiance.ambiance import __version__
version = __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ambiance",
    version=__version__,
    author="Aaron Dettmann",
    author_email="dettmann@kth.se",
    description="A full implementation of the ICAO standard atmosphere 1993",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aarondettmann/ambiance/",
    include_package_data=True,
    package_dir={'': 'src/'},
    license='Apache License 2.0',
    packages=['ambiance'],
    python_requires='>=3.6',
    install_requires=['numpy'],
    # See: https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
)
