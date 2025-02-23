# kaede-api-creation/setup.py

from setuptools import setup, find_packages
import os

setup(
    name='kaede-api-creation',
    version='0.2.0', # Updated version to 0.2.0 (consistent with protocol manager)
    packages=find_packages(),
    install_requires=['kaede-protocol-manager'],
    description='Package to create APIs with custom protocols managed by kaede-protocol-manager.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Kaede Dev Kento Hinode',
    author_email='cleaverdeath@gmail.com',
    url='https://github.com/darsheeegamer/kaede-api-creation', # Replace with your actual repo URL
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)