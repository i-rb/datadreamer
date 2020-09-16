from setuptools import setup

setup(
    name='datadreamer',
    url='https://github.com/i-rb/datadreamer',
    author='David Alonso Martinez and Ivan Rendo Barreiro',
    author_email='irendo@yahoo.es',
    packages=['datadreamer'],
    install_requires=['numpy','pandas'], #more
    version='0.1',
    license='MIT',
    description='A package for cohort analysis',
    long_description=open('README.md').read(),
)
