from setuptools import setup

setup(name='marantz_receiver',
      version='0.0.1',
      description='Library to interface with Marantz receivers through RS232 and TCP',
      url='https://github.com/andrewpc/marantz_receiver',
      download_url='https://github.com/joopert/nad_receiver/archive/0.0.1.tar.gz', #
      author='andrewpc',
      license='MIT',
      packages=['marantz_receiver'],
      install_requires=['pyserial==3.2.1'],
      zip_safe=True)
