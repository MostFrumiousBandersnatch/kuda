from setuptools import setup, find_packages
setup(
    name="ModelMapper",
    version="0.1",
    packages=find_packages(where='kuda/apps', exclude=(), include=('mapper',)),
    package_dir={'': 'kuda/apps'},
    package_data={
        'mapper': ['*.py']
    },

    install_requires=['django>=1.8'],

    author="Ivan Kondratyev",
    author_email="ivanbright@gmail.com",
    description="Mapping arbitrary data formats to django models",
    license="MIT",
    keywords="django models mapper xml sax json",
)
