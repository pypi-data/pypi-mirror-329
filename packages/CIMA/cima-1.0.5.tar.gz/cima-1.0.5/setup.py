import sys, os,shutil
from distutils.core import setup

if os.path.exists('build')==True:
	print("build exists")
	shutil.rmtree('./build')

try:
    import numpy
except ImportError:
    sys.stderr.write('numpy is not installed, you can find it at: '
                     'http://numpy.scipy.org\n')
    sys.exit()

#control version
if [int(dgt) for dgt in numpy.__version__.split('.')[:2]] < [1, 6]:
    sys.stderr.write('CIMA tools requires numpy v1.6 or later, you can find it at: '
                     'http://numpy.scipy.org\n')
    sys.exit()


try:
    import skimage
except ImportError:
    sys.stderr.write('skimage is not installed, you can find it at: ')
    sys.exit()

if [int(dgt) for dgt in skimage.__version__.split('.')[:2]] < [0, 2]:
    sys.stderr.write('CIMA tools requires skimage v0.2 or later, you can find it at: '
                     'http://scikit-image.org\n')
    sys.exit()

#Scipy>=???
try:
    import scipy
except ImportError:
    sys.stderr.write('Scipy is not installed, you can find it at: '
                     'http://www.scipy.org/\n')
    sys.exit()

if [int(dgt) for dgt in scipy.__version__.split('.')[:2]] < [0, 1]:
    sys.stderr.write('CIMA  requires Scipy v0.1 or later, you can find it at: '
                     'http://www.scipy.org/\n')
    sys.exit()

# Make sure I have the right Python version.
if sys.version_info[:2] < (3, 1):
    print("CIMA  requires Python 3.1 or better. Python %d.%d detected" % \
        sys.version_info[:2])
    print("Please upgrade your version of Python.")
    sys.exit(-1)


setup(
    name='CIMA',
    version='1.0.5',
    author='Irene Farabella',
    author_email='irene.farabella@iit.it',
    zip_safe=False,
packages=['CIMA','CIMA.parsers','CIMA.segments','CIMA.assessment','CIMA.utils','CIMA.patches','CIMA.maps','CIMA.detection'],
    license_files=["LICENSE.txt"],
    url='https://github.com/FarabellaLab/CIMA',
    description='',
#    long_description=open('README.txt').read(),
    package_dir = {'CIMA':'src/CIMA'},
    package_data = {'CIMA': ['CIMA_data/*']},
    requires=['NumPy (>=1.6)', 
        "Scipy (>= 0.1)", " Skimage (>= 0.2)"],
)
