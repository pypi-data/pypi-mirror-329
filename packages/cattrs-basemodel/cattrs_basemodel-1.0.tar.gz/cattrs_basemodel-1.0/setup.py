from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='cattrs_basemodel',
    version='1.0',
    author='dail45',
    description='BaseModel for cattrs package which provide (un)structure methods to your models',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url="https://github.com/dail45/cattrs_basemodel",
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='attrs cattrs basemodel json serialize deserialize',
    python_requires='>=3.6',
    requires=[
        "cattrs"
    ]
)
