from setuptools import setup, find_packages

setup(
    name='tccpy',
    version=0.17,
    description='A Python implementation of the Target Confusability Competition (TCC) memory model',
    packages=find_packages(),
    install_requirements=[
        'numpy>=2.0.0'
    ],
    url='https://github.com/ilabsweden/tccpy'
)