from setuptools import setup, find_packages

setup(
    name='apiverve_babynamegenerator',
    version='1.1.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Baby Name Generator is a simple tool for generating baby names. It returns a list of baby names.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
