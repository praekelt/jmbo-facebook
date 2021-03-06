from setuptools import setup, find_packages

setup(
    name='jmbo-facebook',
    version='0.1.3',
    description='Fetch facebook page updates.',
    long_description=(open('README.rst', 'r').read() +
                        open('AUTHORS.rst', 'r').read() +
                        open('CHANGELOG.rst', 'r').read()),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/jmbo-facebook',
    packages = find_packages(),
    install_requires = [
        'jmbo-foundry>=0.4',
    ],
    include_package_data=True,
    tests_require=[
        'django-setuptest',
        'coverage',
    ],
    test_suite="setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
