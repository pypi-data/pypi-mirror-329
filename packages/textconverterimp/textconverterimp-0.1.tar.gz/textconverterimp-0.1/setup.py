from setuptools import setup, find_packages

setup(
    name='textconverterimp',
    version='0.1',
    packages=find_packages(),
    description='A library to convert text into different formats.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='improve',
    author_email='vlasav227@mail.ru',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)