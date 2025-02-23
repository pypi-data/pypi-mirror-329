from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='TopDR',
    version='0.3',
    description='Topological Dimension Reduction',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='BOYABATLI, Kenan Evren; YİĞT, Uğur',
    author_email='kbybtli@gmail.com; ugur.yigit@medeniyet.edu.tr',
    url='https://github.com/EvReN-jr/TDR_share',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'statistics'
    ],
)