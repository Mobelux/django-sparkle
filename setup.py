from setuptools import setup, find_packages
import sparkle
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.md')


setup(
    name = "django-sparkle",
    version = sparkle.__version__,
    description = 'Django-sparkle is a Django application to make it easy to publish updates for your mac application using sparkle',
    long_description = README,
    url = 'http://github.com/jemerick/django-sparkle',
    author = 'Jason Emerick',
    author_email = 'jemerick@gmail.com',
    license = 'BSD',
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)