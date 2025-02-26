"""""" # start delvewheel patch
def _delvewheel_patch_1_10_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyscipopt.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyscipopt-5.4.1')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-pyscipopt-5.4.1')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_10_0()
del _delvewheel_patch_1_10_0
# end delvewheel patch

from ._version import __version__

# required for Python 3.8 on Windows
import os
if hasattr(os, 'add_dll_directory'):
    if os.getenv('SCIPOPTDIR'):
        os.add_dll_directory(os.path.join(os.getenv('SCIPOPTDIR').strip('"'), 'bin'))

# export user-relevant objects:
from pyscipopt.Multidict import multidict
from pyscipopt.scip      import Model
from pyscipopt.scip      import Variable
from pyscipopt.scip      import MatrixVariable
from pyscipopt.scip      import Constraint
from pyscipopt.scip      import MatrixConstraint
from pyscipopt.scip      import Benders
from pyscipopt.scip      import Benderscut
from pyscipopt.scip      import Branchrule
from pyscipopt.scip      import Nodesel
from pyscipopt.scip      import Conshdlr
from pyscipopt.scip      import Eventhdlr
from pyscipopt.scip      import Heur
from pyscipopt.scip      import Presol
from pyscipopt.scip      import Pricer
from pyscipopt.scip      import Prop
from pyscipopt.scip      import Reader
from pyscipopt.scip      import Sepa
from pyscipopt.scip      import LP
from pyscipopt.scip      import readStatistics
from pyscipopt.scip      import Expr
from pyscipopt.scip      import MatrixExpr
from pyscipopt.scip      import MatrixExprCons
from pyscipopt.scip      import ExprCons
from pyscipopt.scip      import quicksum
from pyscipopt.scip      import quickprod
from pyscipopt.scip      import exp
from pyscipopt.scip      import log
from pyscipopt.scip      import sqrt
from pyscipopt.scip      import sin
from pyscipopt.scip      import cos
from pyscipopt.scip      import PY_SCIP_RESULT       as SCIP_RESULT
from pyscipopt.scip      import PY_SCIP_PARAMSETTING as SCIP_PARAMSETTING
from pyscipopt.scip      import PY_SCIP_PARAMEMPHASIS as SCIP_PARAMEMPHASIS
from pyscipopt.scip      import PY_SCIP_STATUS       as SCIP_STATUS
from pyscipopt.scip      import PY_SCIP_STAGE        as SCIP_STAGE
from pyscipopt.scip      import PY_SCIP_PROPTIMING   as SCIP_PROPTIMING
from pyscipopt.scip      import PY_SCIP_PRESOLTIMING as SCIP_PRESOLTIMING
from pyscipopt.scip      import PY_SCIP_HEURTIMING   as SCIP_HEURTIMING
from pyscipopt.scip      import PY_SCIP_EVENTTYPE    as SCIP_EVENTTYPE
from pyscipopt.scip      import PY_SCIP_LPSOLSTAT    as SCIP_LPSOLSTAT
from pyscipopt.scip      import PY_SCIP_BRANCHDIR    as SCIP_BRANCHDIR
from pyscipopt.scip      import PY_SCIP_BENDERSENFOTYPE as SCIP_BENDERSENFOTYPE
from pyscipopt.scip      import PY_SCIP_ROWORIGINTYPE as SCIP_ROWORIGINTYPE
from pyscipopt.scip      import PY_SCIP_SOLORIGIN as SCIP_SOLORIGIN
