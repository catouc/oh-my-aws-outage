from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author='Philipp Boeschen',
    author_email='boeschenphilipp@gmail.com',
    name='oh-my-aws-outage',
    version='0.1',
    packages=['aws_outage'],
    license='MIT',
    url='https://github.com/Deichindianer/oh-my-aws-outage',
    download_url='https://github.com/Deichindianer/oh-my-aws-outage/archive/v0.1.0.tar.gz',
    install_required=['boto3'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
