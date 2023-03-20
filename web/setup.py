# run with `develop` argument
from setuptools import setup, find_packages

setup(
    name='imit webapp',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests.all_tests",
    install_requires=[
        'Flask==0.12.2',
        'Flask-WTF==0.14.2',
        'Flask-SQLAlchemy==2.3.2',
        'Flask-Migrate==2.1.1',
        'ldap3==2.4.1',
        'beautifulsoup4==4.6.0',
        'Flask-Login==0.4.1',
        'Flask-Admin==1.5.0',
        'Flask-Babel==0.11.2',
        'requests==2.18.4'
    ]
)
