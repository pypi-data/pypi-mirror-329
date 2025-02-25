from setuptools import setup, find_packages

setup(
    name='phonestore',  # Replace with your project name
    version='0.1',  # Replace with your version
    packages=find_packages(),
    install_requires=[
        'django',  # Add your project dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
