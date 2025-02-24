from setuptools import setup, find_packages

setup(
    name='pyweber',
    version='0.1.7',
    packages=find_packages(include=['pyweber', 'pyweber.*']),
    install_requires=[
        'websockets',
        'watchdog',
        'typer'
    ],
    entry_points={
        'console_scripts': [
            'pyweber=pyweber.utils.pyweber_cli:app',
        ],
    },
    author='DevPythonMZ',
    author_email='zoidycine@egmail.com',
    description='A lightweight Python framework for building and managing web applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://pyweber.readthedocs.io/en/latest',
    project_urls={
        'Documentation': 'https://pyweber.readthedocs.io/en/latest',
        'Source Code': 'https://github.com/webtechmoz/pyweber',
        'Issue Tracker': 'https://github.com/webtechmoz/pyweber/issues',
        'PyPI': 'https://pypi.org/project/pyweber/',
        'Youtube': 'https://youtube.com/@devpythonMZ'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)