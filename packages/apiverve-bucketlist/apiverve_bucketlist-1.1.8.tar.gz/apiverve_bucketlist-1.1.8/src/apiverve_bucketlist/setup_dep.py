from setuptools import setup, find_packages

setup(
    name='apiverve_bucketlist',
    version='1.1.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Bucket List is a simple tool for getting a random bucket list item. It returns a random item from a predefined list of items.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
