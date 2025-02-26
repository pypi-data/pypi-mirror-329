from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Ossarth',
    version='0.1.1',
    description='A customizable Ossarth AI-powered open-source operating system toolkit',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Siddharth Magesh',
    author_email='siddharthmagesh007@gmail.com',
    url='https://github.com/Siddharth-magesh/Ossarth',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'flask'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
