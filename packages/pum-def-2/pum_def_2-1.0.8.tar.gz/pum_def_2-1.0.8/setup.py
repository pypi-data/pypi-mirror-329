from setuptools import setup, find_packages
# import os

# os.system("rd dist /s /q")
# os.system("rd build /s /q")
# os.system("rd pum_def_2.egg-info /s /q")

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='pum_def_2',
    version='1.0.8',
    author='USEC',
    author_email='karasevich.evg903@gmail.com',
    description='Utilities for PUM',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='',
    project_urls={

    },
    python_requires='>=3.11'
)
