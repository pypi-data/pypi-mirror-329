from setuptools import setup, find_packages

setup(
    name='tccpy',
    version=0.1,
    packages=find_packages(),
    install_requirements=[
        'numpy>=2.0.0'
    ]
)