
from setuptools import setup, find_packages
import os

setup(
    name='kaede_protocol_manager',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'kaede-protocol-manager=kaede_protocol_manager.cli:main',
        ],
    },
    description='CLI tool to manage custom API protocols for Kaede API Creation package.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    author='Kaede Dev Kento Hinode',
    author_email='cleaverdeath@gmail.com',
    url='https://github.com/darsheeegamer/kaede-protocol-manager', 
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