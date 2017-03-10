import sys
from setuptools import setup, find_packages


with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
    if not install_requirements:
        print('Unable to read requirements from the requirements.txt file')
        sys.exit(1)

setup(
    name='update-wrapper',
    version='1.1.0',
    description='Simplify applying updates on multiple servers by wrapping the update process and logging the output.',
    keywords='update wrapper linux debian ansible djdch',
    url='https://github.com/EpicScriptTime/update-wrapper',
    author='DjDCH',
    author_email='coding@djdch.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    install_requires=install_requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'update-wrapper=updatewrapper:main',
        ],
    },
)
