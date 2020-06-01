
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='srimulatorcore',  
     version='0.2',
     author="Lorena B Bassani",
     author_email="lorenabassani12@gmail.com",
     description="Core of Sobot Rimulator by Nick McCrea",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/LBBassani/sobot-rimulator-core",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 2",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
         "Operating System :: OS Independent",
         "Development Status :: 2 - Pre-Alpha",
     ],
     python_requires='>=2.6',
 )
