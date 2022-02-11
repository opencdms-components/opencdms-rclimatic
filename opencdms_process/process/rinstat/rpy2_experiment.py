# This file is a personal reference to better understand rpy2
# See https://rpy2.github.io/doc/v3.4.x/html/introduction.html

from typing import Final, Tuple
from numpy import NaN
from rpy2.robjects import r, packages, vectors, globalenv
from rpy2.robjects.vectors import StrVector

def naflex_na_omit_if(data: Tuple, prop = None, n = None, consec = None, n_non = None, prop_strict = False) -> Tuple:

    # Install the required R packages
    R_NAFLEX: str = 'naflex'
    R_PACKAGE_DIR: str = '~/local/R_libs'
    r_package_names = (R_NAFLEX, )
    r_packages_to_install = [x for x in r_package_names if not packages.isinstalled(x, lib_loc = R_PACKAGE_DIR)]
    if len(r_packages_to_install) > 0:
        r_utils = packages.importr('utils')
        r_utils.chooseCRANmirror(ind=1) # select the first mirror in the list
        r_utils.install_packages(StrVector(r_packages_to_install), lib = R_PACKAGE_DIR)

    # execute R function and return result
    r_naflex = packages.importr(R_NAFLEX)    
    return_values = r_naflex.na_omit_if(vectors.FloatVector(data), prop = prop)
    len_return_values = len(return_values)
    return tuple(return_values)
    
def simple_rpy2_example() -> str:
    
    '''
    @lloyddewit's personal notes on rpy2
    rpy2 contains several pacakages. The developers recommend `robjects` for general use.
    If we need more flexibility/performance we can potentially use `rinterface`.

    robjects.r represents the R environment.
    It is a singleton. The same R environment is used for all R calls. The R environment is stateful.

    Each object in the R environment has an equivalent Python object with the same name (warning: '.' 
            in R name cause problems for Python).
        plot = robjects.r.plot
    Python object will persist, even if R object is deleted.
    Get R representation of Python object:
        plot.r_repr()

    The R environment can be accessed as a Python dictionary (key is name of object, value is object).
        robjects.globalenv["a"] = 123
    rpy2 has functions to iterate through keys/object, find objects, pop objects (return and remove), 
            and clear environments.

    We can call R functions in packages:
        from rpy2.robjects.packages import importr
        base = importr('base')
        stats = importr('stats')
        graphics = importr('graphics')

        plot = graphics.plot
        rnorm = stats.rnorm
        plot(rnorm(100), ylab="random")
    If we need to specify the R environment, we can use `rcall`:
        from rpy2.robjects.packages import importr
        base = importr('base')
        stats = importr('stats')
        graphics = importr('graphics')

        plot = graphics.plot
        rnorm = stats.rnorm

        # import R's "GlobalEnv" to evaluate the function
        from rpy2.robjects import globalenv

        # build a tuple of 2-tuple as arguments
        args = (('x', rnorm(100)),)

        # run the function in globalenv
        plot.rcall(args, globalenv)
    We can get details of a function's parameters from the R environment:
        from rpy2.robjects.packages import importr
        stats = importr('stats')
        rnorm = stats.rnorm
        rnorm.formals()
            <Vector - Python:0x8790bcc / R:0x93db250>
        tuple(rnorm.formals().names)
            ('n', 'mean', 'sd')
    
    We can find the attributes in an R object (see https://stackoverflow.com/questions/59462337/importing-any-function-from-an-r-package-into-python/59462338#59462338):
        bnlearn = importr('bnlearn')
        bnlearn.__dict__['_rpy2r']
            ...
            'bn_boot': 'bn.boot',
            'bn_cv': 'bn.cv',
            'bn_cv_algorithm': 'bn.cv.algorithm',
            'bn_cv_structure': 'bn.cv.structure',
            'bn_fit': 'bn.fit',
            'bn_fit_backend': 'bn.fit.backend',
            ...
        bn_fit = bnlearn.bn_fit

    We can convert between Python and R object types (below may not be needed, conversion may be implicit)
        # Allow conversion
        import rpy2.robjects as ro
        from rpy2.objects import pandas2ri
        pandas2ri.activate()# Convert to R dataframe
        r_dt = ro.conversion.py2rpy(dt) # dt is a pd.DataFrame object# Convert back to pandas DataFrame        
        pd_dt = ro.conversion.rpy2py(r_dt)

    We can import packages
        from rpy2.robjects.packages import importr
        utils = importr("utils")
    We can install R packages from Cran
        import rpy2.robjects.packages as rpackages
        utils = rpackages.importr('utils')

        utils.chooseCRANmirror(ind=1) # select the first mirror in the list
        packnames = ('ggplot2', 'hexbin')
        from rpy2.robjects.vectors import StrVector
        utils.install_packages(StrVector(packnames))
    TODO: if it is inefficient to always install the package, then we could first check if package(s) 
            are installed, maybe use the following functions:
        rpy2.robjects.packages.isinstalled(name: str, lib_loc=None)
        class rpy2.robjects.packages.InstalledPackages(lib_loc=None)
    We can also use code from '.r' files but the developers recommend not to do this.
            If we do, then we have to copy/paste the code into a Python string and then use the 
            SignatureTranslatedAnonymousPackage function

    '''

    # Import the R package into the embedded R, and expose all R objects in that package as Python objects
    # rpy2 also has methods to install R packages.
    # But for this example, I'm assuming that the required packages are already installed in the R environment

    # import R's "base" package
    base = packages.importr('base')

    # import R's "utils" package
    utils = packages.importr('utils')

    # 'r' is a singleton, we can pass R script to 'r'.
    # It executes the script in the R Global Environment and returns vector of length 1
    pi = r('pi')
    print(f'pi[0] {pi[0]}') # should print 3.14159265358979

    # declare an R function
    r('''
        # create a function `f`
        f <- function(r, verbose=FALSE) {
            if (verbose) {
                cat("I am calling f().\n")
            }
            2 * pi * r
        }
        # call the function `f` with argument value 3
        f(3)
        ''')
    
    """
    Get function definition. Should return:
    
        function (r, verbose = FALSE)
        {
            if (verbose) {
                cat("I am calling f().\n")
            }
            2 * pi * r
        } 
    """
    r_f = globalenv['f']
    print(r_f.r_repr())

    # call the function just like a Python function
    print(r_f(3, True))

    """ 
    Get the string representation of an R object.
    Should return:
    "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z" 
    """
    letters = r['letters']
    rcode = 'paste(%s, collapse="-")' %(letters.r_repr())
    res = r(rcode)
    print(res)
    
    return "a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r-s-t-u-v-w-x-y-z"
