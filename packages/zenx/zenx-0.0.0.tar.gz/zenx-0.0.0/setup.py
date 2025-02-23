
from setuptools import setup, find_packages

setup(
    name='zenx',  
    version='0.0.0',
    description='ZenX: Text data Optimizer',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Rishi Chaitanya Sri Prasad Nalluri',
    author_email='rishichaitanya888@gmail.com',
    packages=find_packages(),
    install_requires=[     
        'tensorflow>=2.10.0',
        'keras>=2.10.0',
        'loglu>=1.1.2'
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research', 
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.6',
)
