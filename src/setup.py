import setuptools

setuptools.setup(name='transsim',
version='3.2',
description='transsim DSL interpreter',
url='#',
author='Daniel Gui, Himanshu Neema, Ruixiao Sun, Yuche Chen',
install_requires=['traci', 'dask[dataframe]', 'pandas', 'numpy', 'textx'],
author_email='rongze.gui@vanderbilt.edu',
include_package_data=True,
packages=setuptools.find_packages(),
zip_safe=False)
