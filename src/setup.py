import setuptools

setuptools.setup(name='transsim',
version='0.1',
description='transsim DSL interpreter',
url='#',
author='Daniel Gui, Himanshu Neema, Ruixiao Sun, Yuche Chen',
install_requires=['traci', 'dask[dataframe]', 'pandas', 'numpy', 'textx'],
author_email='rongze.gui@vanderbilt.edu',
packages=setuptools.find_packages(),
zip_safe=False)