from setuptools import setup, find_packages

setup(
    name='ncpcs_common',
    version='3.9.0',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'pymysql',
        'python-dateutil',
        'pytest',
        'cryptography'
    ]
)