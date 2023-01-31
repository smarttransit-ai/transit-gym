import setuptools

setuptools.setup(name='transsim',
version='3.5',
description='transsim DSL interpreter',
url='#',
author='Daniel Gui, Himanshu Neema, Ruixiao Sun, Yuche Chen, Abhishek Dubey',
install_requires=['traci', 'dask[dataframe]', 'pandas', 'numpy', 'textx', 'openpyxl'],
author_email='rongze.gui@vanderbilt.edu',
include_package_data=True,
packages=setuptools.find_packages(),
zip_safe=False)
