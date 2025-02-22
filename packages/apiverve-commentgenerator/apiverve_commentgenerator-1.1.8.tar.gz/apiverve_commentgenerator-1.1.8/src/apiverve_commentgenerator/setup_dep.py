from setuptools import setup, find_packages

setup(
    name='apiverve_commentgenerator',
    version='1.1.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'setuptools'
    ],
    description='Comment Generator is a simple tool for generating comments for social media. It returns a list of comments based on the input parameters.',
    author='APIVerve',
    author_email='hello@apiverve.com',
    url='https://apiverve.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
