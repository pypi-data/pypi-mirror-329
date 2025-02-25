from setuptools import setup, find_packages
import os

setup(
    name='tell_whois_who',
    version='0.2.0', # Version bump since we added functionality
    packages=find_packages(),
    install_requires=[
        'requests',  # Add 'requests' as a dependency
    ],
    entry_points={
        'console_scripts': [
            'whois=tell_whois_who.cli:main', # Command name changed to 'who_is' and entry point to main()
        ],
    },
    author='Sriharan S',
    author_email='sriharan2544@gmail.com',
    description='A simple package to tell whois who!',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)