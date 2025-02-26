import setuptools

setuptools.setup(
    name='pyupdog',
    version='1.2.4',
    author='Joseph Halstead',
    author_email='josephhalstead89@gmail.com',
    description='Python program for calculating UPD',
    long_description='Python program for calculating UPD',
    long_description_content_type='text/markdown',
    url='https://github.com/josephhalstead/pyvariantfilter',
    packages=setuptools.find_packages(),
    scripts= ['UPDog.py'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
   'pysam>=0.22.1',
   'pandas>=2.2',
   'seaborn>=0.13',
   'scipy>=1.14',
   'pyvariantfilter>=2.1.0',
],
)
