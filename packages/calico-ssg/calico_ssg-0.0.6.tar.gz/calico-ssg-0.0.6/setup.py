import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version:
    VERSION = version.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='calico-ssg',
    version=VERSION.strip('\t\n '),
    packages=['calico', 'picocss', 'calico_bootstrap'],
    include_package_data=True,
    license='MIT License',
    description='Django-based static site generator',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://gitlab.levitnet.be/levit/calico',
    author='LevIT SCS',
    author_email='info@levit.be',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=4.2',
        'django-distill>=3.2.4',
        'django-markdown-deux>=1.0.6',
        'dj_angles>=0.10.0',
        'django-templateyak>=0.0.1',
        'pillow==10.4.0',
        'python-frontmatter>=1.1.0',
        'readtime==3.0.0',
    ]
)
