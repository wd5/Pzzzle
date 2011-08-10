from setuptools import setup, find_packages

setup(
    name = "pzzzle",
    version = "0.8",
    url = 'https://github.com/glader/Pzzzle',
    license = 'BSD',
    description = "Fun puzzle site http://pzzzle.com/",
    author = 'Mikhail Polykovskij',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)