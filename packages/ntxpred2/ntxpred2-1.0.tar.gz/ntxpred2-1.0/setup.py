from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
from setuptools import setup, Extension
from pathlib import Path
# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='ntxpred2',
    version='1.0',
    description='NTxPred2: A method for predicting the neurotoxic activity of peptides and proteins.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='LICENSE.txt',
    url='https://github.com/raghavagps/NTxPred2',
    author='Anand Singh Rathore', 
    author_email='anandr@iiitd.ac.in, anandrathoreindia@gmail.com',
    packages=find_namespace_packages(where="src"),
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['ntxpred2 = ntxpred2.python_scripts.ntxpred2:main']},
    python_requires='>=3.9',

)
