import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='twitter',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
        'Delorean',
        'oauthlib',
        'requests[security]',
        'requests-oauthlib',
        'psycopg2',
    ],
    license='BSD License',
    description='A Python/Django Twitter client for REST & stream APIs and models for Twitter content',
    long_description=README,
    url='https://onurmatik.github.io/',
    author='@onurmatik',
    author_email='onurmatik@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
