from setuptools import setup

setup(
    name='pyoche',
    version='0.1.2',
    description='Standardisation of the data structure for ML/DL for engineering applications.',
    author='Jean F',
    author_email='jean.fesquet@isae-supaero.fr',
    packages=['pyoche', 'pyoche.ml', 'pyoche.structures', 'pyoche.utils'],
    install_requires=['numpy', 'matplotlib', 'h5py', 'pathlib', 'tqdm'],
    license='MIT License',
    license_files=('LICENSE',)
)