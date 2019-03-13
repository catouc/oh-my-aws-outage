from distutils.core import setup
from aws_outage import __version__

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

package_url = 'https://github.com/Deichindianer/oh-my-aws-outage'
download_url = f'{package_url}/archive/{__version__}.tar.gz'

setup(
    author='Philipp Boeschen',
    author_email='boeschenphilipp@gmail.com',
    name='oh-my-aws-outage',
    version=__version__,
    packages=['aws_outage'],
    license='MIT',
    url='https://github.com/Deichindianer/oh-my-aws-outage',
    download_url=download_url,
    install_requires=['boto3'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
