import setuptools

VERSION = "0.0.1"
with open('README.md', encoding='utf-8') as f:
    long_description = f.read().strip()

setuptools.setup(
    name='django-link-report',
    version=VERSION,
    description='Django Link Report',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Andy Baker',
    author_email='andy@andybak.net',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['requests'],
    license='MIT License',
    zip_safe=False,
    keywords='django admin link',
    classifiers=['Framework :: Django'],
)
