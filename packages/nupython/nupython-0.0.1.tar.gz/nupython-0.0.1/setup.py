from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nupython',
    version='0.0.1',
    packages=find_packages(include=['src', 'src.*']),
    entry_points={
        'console_scripts': [
            'npy=src.cli.__main__:main',
        ],
    },
    install_requires=[
    ],
    python_requires='>=3.6',
    author='Pedro Luis Dias',
    author_email='luisp.diias@gmail.com',
    description='NuPython is a superset of Python that compiles to clear Python output.',
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/diaslui/nupython',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)