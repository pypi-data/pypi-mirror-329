from setuptools import setup, find_packages

setup(
    name='pyoche',
    version='0.1.1',
    description='This will help you mine the good stuff, and use it for ML/DL pipelines',
    author='Jean F',
    author_email='jean.fesquet@isae-supaero.fr',
    packages=find_packages(include=['pyoche']),
    install_requires=['numpy', 'matplotlib', 'h5py', 'pathlib', 'tqdm'],
    license='MIT License',
    license_files=('LICENSE',)
)