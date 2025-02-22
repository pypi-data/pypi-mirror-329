from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name="askoclics",
    version='0.0.8',
    description="Askomics CLI",
    author="Mateo Boudet",
    author_email="mateo.boudet@inrae.fr",
    url="https://github.com/mboudet/askoclics",
    install_requires=requires,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    entry_points='''
        [console_scripts]
        askoclics=askoclics.cli.cli:askoclics
    ''',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.7",
    ]
)
