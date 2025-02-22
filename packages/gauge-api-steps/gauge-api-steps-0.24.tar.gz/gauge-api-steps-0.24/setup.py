from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description = long_description.replace('./docs/', 'https://github.com/IBM/gauge-api-steps/tree/master/docs/')

setup(
    name='gauge-api-steps',
    version='0.24',
    description='Provides steps for a Gauge project, that runs tests against APIs',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/IBM/gauge-api-steps',
    author='Tobias Lehmann',
    author_email='derdualist1@gmail.com',
    license='MIT',
    packages=['gauge_api_steps'],
    install_requires=[
        'diff-match-patch==20241021',
        'getgauge',
        'jsonpath-ng==1.7.0',
        'lxml==5.3.0',
        'numexpr==2.10.2',
        'colorama==0.4.6',
    ],
    zip_safe=False
)
