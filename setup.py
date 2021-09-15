from setuptools import find_packages, setup

def dependencies(requirements='requirements.txt'):
    with open(requirements, 'r') as file:
        packages = []
        for package in file.read().split():
            packages.append(package.split(sep='==', maxsplit=2)[0])
    return packages


setup(
    name='app',
    version='beta_0.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=dependencies(),
)