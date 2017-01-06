from distutils.core import setup

setup(
    name='cards',
    version='1.0.0',
    packages=[''],
    url='http://www.bankys.com',
    license='BSD',
    author='bankeys',
    author_email='weizhigang@bankeys.com',
    description='check bankcard info'
)

install_requires = [
    'Flask>=0.2',
    'pandas>=0.9.1'
]
