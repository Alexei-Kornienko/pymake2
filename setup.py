#from distutils.core import setup
import os
from setuptools import setup
from setuptools.command.install import install


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

class MyInstall(install):
    def run(self):
        install.run(self)
        #print("\n\n\n\nI did it!!!!\n\n\n\n")
        cmd = 'sudo activate-global-python-argcomplete'
        print(cmd)
        os.system(cmd)        

setup(
    name="pymake2",
    version="0.5.33",
    author="Saud Wasly",
    author_email="saudalwasli@gmail.com",
    description=("pymake2 is a simple Python-based make system. It brings simplicity and flexibility of Python language to makefiles."),
    license="MIT",
    keywords="make makefile build",
    url="https://bitbucket.org/saudalwasly/pymake2/src",
    install_requires=read('requirements.txt'),
    packages=['pymake2'],
    scripts=['pymake2/pymake3'],
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",        
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={'install': MyInstall}    
)
