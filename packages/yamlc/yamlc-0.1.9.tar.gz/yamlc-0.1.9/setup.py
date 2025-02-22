from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yamlc',
    version='0.1.9',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
    ],
    author='陌北v1',
    author_email='hongen.me@gmail.com',
    description='A simple YAML configuration loader',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hongenge/yamlc',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    license='MIT',
)
