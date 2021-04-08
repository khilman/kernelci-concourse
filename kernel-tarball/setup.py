from setuptools import setup

setup(name='kci_resource',
      version='0.1',
      description='KernelCI tarball resource',
      url='http://gitlab.com/khilman/kernelci-tarball-resource',
      author='Kevin Hilman',
      author_email='khilman@baylibre.com',
      license='MIT',
      packages=['kci_resource'],
      zip_safe=False,
      entry_points={
          'console_scripts': ['check=kci_resource.concourse:check',
                              'out=kci_resource.concourse:output',
                              'in=kci_resource.concourse:input']
      },
      install_requires=[
          'requests'
      ]
)
