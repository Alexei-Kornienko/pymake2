#from distutils.core import setup
import os
from setuptools import setup
from setuptools.command.install import install

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class MyInstall(install):
    def run(self):
        install.run(self)
        #print("\n\n\n\nI did it!!!!\n\n\n\n")
        cmd = 'sudo activate-global-python-argcomplete'
        print cmd
        os.system(cmd)        

setup(
    name="pymake2",
    version = "0.5.32",
    author = "Saud Wasly",
    author_email = "saudalwasli@gmail.com",
    description = ("pymake2 is a simple Python-based make system. It brings simplicity and flexibility of Python language to makefiles."),
    license = "MIT",
    keywords = "make makefile build",
    url = "https://bitbucket.org/saudalwasly/pymake2/src",
    install_requires=["argcomplete", "sarge"],
    packages=['pymake2'],
    scripts=['pymake2/pymake2', 'pymake2/pmake2'],
    #data_files = [('', ['__init__.py', 'pymake2', 'make.py', 'utility.py', 'makefile_template.py'])] ,
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",        
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={'install': MyInstall}    
)