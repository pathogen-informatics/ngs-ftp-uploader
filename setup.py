import glob
from setuptools import setup, find_packages

setup(
    name='ngs-ftp-uploader',
    version='0.0.1',
    description='ngs ftp file uploader',
    packages = find_packages(),
    author='Sara Sjunnebo',
    author_email='path-help@sanger.ac.uk',
    url='git@gitlab.internal.sanger.ac.uk:sanger-pathogens/ngs-ftp-uploader.git',
    scripts=glob.glob('scripts/*'),
    test_suite='nose.collector',
    tests_require=['nose >= 1.3'],
    install_requires=[],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
