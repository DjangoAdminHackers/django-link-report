import setuptools
from link_report.version import Version


setuptools.setup(name='django-link-report',
                 version=Version('0.0.1').number,
                 description='Django Link Report',
                 long_description=open('README.md').read().strip(),
                 author='Andy Baker',
                 author_email='andy@andybak.net',
                 py_modules=[],
                 install_requires=['requests'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='django admin link',
                 classifiers=['Packages'])
