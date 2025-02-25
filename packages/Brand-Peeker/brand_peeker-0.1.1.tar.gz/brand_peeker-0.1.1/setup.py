from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Brand_Peeker',
    version='0.1.1',
    packages=find_packages(),
    install_requires=requirements,
    author='Gaz_Butane',
    description='A python library that allows you to scrape information about a brand, such as its logo or website',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/GazButane/Brand_Peeker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)