from setuptools import setup, find_packages

setup(
    name='asro_preprocessing',
    version='0.1.5',
    author='Asro',
    author_email='asro@rahrja.info',
    description='Library untuk preprocessing teks dan menampilkan profil pengguna.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'asro_preprocessing': ['data/*'],
    },
    install_requires=[
        'pandas',
        'nltk',
        'Pillow',
        'openpyxl'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
