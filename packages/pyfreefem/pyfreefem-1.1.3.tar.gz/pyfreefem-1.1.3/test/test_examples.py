# This file is part of PyFreeFEM.
#
# PyFreeFEM is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# PyFreeFEM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# A copy of the GNU General Public License is included below.
# For further information, see <http://www.gnu.org/licenses/>.
import os
from pyfreefem import Preprocessor, FreeFemRunner
from pyfreefem.io import readFFArray, writeFFArray, readFFMatrix, writeFFMatrix
import numpy as np
import scipy as sp
try:
    import pymedit  
    WITH_PYMEDIT = True
except:
    WITH_PYMEDIT = False

examples_folder = os.path.split(os.path.split(__file__)[0])[0]+'/pyfreefem/examples'

def test_ex00_substitution():    
    from pyfreefem.examples.ex00_substitution import parsed
    expected ='real Re=100;\nreal bigPe=30;//Accolades needed'
    assert parsed == expected

def test_ex01_default_set():
    from pyfreefem.examples.ex01_default_set import parsed_default, config_default, parsed_variant, config_variant
    assert parsed_default == 'real Re=10;\nreal Pe=30;\nreal ratio=0.3333333333333333;\n'
    assert parsed_variant == 'real Re=100;\nreal Pe=30;\nreal ratio=3.3333333333333335;\n'
    assert config_default == {'Re': 10, 'Pe': 30, 'ratioRePe': 0.3333333333333333}  
    assert config_variant == {'Pe': 30, 'Re': 100, 'ratioRePe': 3.3333333333333335}
        
def test_ex02_set_textvar(): 
    from pyfreefem.examples.ex02_set_textvar import preproc 
    assert preproc.config['params.mmg2d']=='Parameters\n1\n \n10 Edges 0.0001 0.001 1e-05\n'
    
def test_ex03_ifeq():    
    from pyfreefem.examples.ex03_ifeq import parsed_default, parsed_P2, parsed_P1b
    expected_default = '\ncout << "Solving with P1 finite elements." << endl;\n\nmesh Th=square(30,30);\nfespace Fh(Th,P1);\nFh u,v;\nsolve laplace(u,v)=\n    int2d(Th)(dx(u)*dx(v)+dy(u)*dy(v))\n        -int2d(Th)(v)\n        +on(1,2,3,4,u=0);\n\ncout << "ORDER_OK has been set." << endl;\n'
    expected_P2 = '\n\ncout << "Solving with P2 finite elements." << endl;\n\nmesh Th=square(30,30);\nfespace Fh(Th,P2);\nFh u,v;\nsolve laplace(u,v)=\n    int2d(Th)(dx(u)*dx(v)+dy(u)*dy(v))\n        -int2d(Th)(v)\n        +on(1,2,3,4,u=0);\n\ncout << "ORDER_OK has been set." << endl;\n' 
    expected_P1b = '\n\ncout << "The specified finite element order should be P1 or P2." << endl;\n\n'  
    assert parsed_default == expected_default  
    assert parsed_P2 == expected_P2
    assert parsed_P1b == expected_P1b

def test_ex04_for(): 
    from pyfreefem.examples.ex04_for import parsed
    assert parsed == '//Create a square mesh of size 1x1\nmesh Th1 = square(10,10,[1*x,1*y]);\n\n//Create a square mesh of size 2x2\nmesh Th2 = square(10,10,[2*x,2*y]);\n\n//Create a square mesh of size 3x3\nmesh Th3 = square(10,10,[3*x,3*y]);\n\n//Create a square mesh of size 4x4\nmesh Th4 = square(10,10,[4*x,4*y]);\n\n//Create a square mesh of size 5x5\nmesh Th5 = square(10,10,[5*x,5*y]);\n\n//Create a square mesh of size 6x6\nmesh Th6 = square(10,10,[6*x,6*y]);\n\n//Create a square mesh of size 7x7\nmesh Th7 = square(10,10,[7*x,7*y]);\n\n//Create a square mesh of size 8x8\nmesh Th8 = square(10,10,[8*x,8*y]);\n\n//Create a square mesh of size 9x9\nmesh Th9 = square(10,10,[9*x,9*y]);\n\n'
        
def test_ex05_magic_comment():   
    from pyfreefem.examples.ex05_magic_comment import parsed
    assert parsed == '\n\n// Display the Reynolds number\ncout << "Re=100;" << endl;\n'
        
def test_ex06_double_backslash():    
    from pyfreefem.examples.ex06_double_backslash import parsed
    assert parsed == 'mesh Th=square(10,10);\nfespace Fh(Th,P1);\nFh u,v;\n\nsolve laplace(u,v)=\n    int2d(Th)(dx(u)*dx(v)+dy(u)*dy(v))\n        -int2d(Th)(v); \n        //This final semicolumn character will be put \n        //at the end of the last previous line\n\n'

def test_ex07_read_write_FFArray():  
    from pyfreefem.examples.ex07_read_write_FFArray import x, rets
    assert np.allclose(list(range(1,13)),x,atol=0)
    assert rets[1] == 'FreeFEM : read ex7_x2.gp \n12\t\n\t 12\t 11\t 10\t  9\t  8\n\t  7\t  6\t  5\t  4\t  3\n\t  2\t  1\t\n'
            
def test_ex08_read_write_FFMatrix(): 
    from pyfreefem.examples.ex08_read_write_FFMatrix import A, rets
    expected = np.array([[ 4/3, -5/12, -5/12,  1/6],
        [-5/12,  7/6,  0.        , -5/12],
        [-5/12,  0.        ,  7/6, -5/12],
        [ 1/6, -5/12, -5/12,  4/3]])
    assert np.allclose(A.todense(),expected,atol=0)
    assert '\n'.join(rets[1].splitlines()[2:]) == '#    n       m        nnz     half     fortran   state  \n5 5 5 0 0 0 0 \n         0         0 1\n         1         1 1\n         2         2 1\n         3         3 1\n         4         4 1\n'  

def test_ex09_freefemrunner_env():  
    from pyfreefem.examples.ex09_freefemrunner_env import result
    assert np.allclose(result,0.6666666666666695,1e-10)


def test_ex10_io_export():
    from pyfreefem.examples.ex10_io_export import exports
    assert np.allclose(exports['A'].trace(),400.5,atol=1e-10)
    assert np.allclose(exports['arr'],np.array([1,2,3,4]),atol=0)
    assert np.allclose(sum(exports['u']),121.89328045616362,atol=1e-10)
    assert np.allclose(sum(exports['f']*exports['u']),1.3121929992942643,atol=1e-10)
    assert np.allclose(exports['var'],np.pi,1e-10)
    if WITH_PYMEDIT:    
        assert exports['Th'].nv == 121
            
def test_ex11_io_import():
    from pyfreefem.examples.ex11_io_import import result
    assert result[-140:]=='     half     fortran   state  \n4 4 4 0 0 0 0 \n         0         0 1\n         1         1 2\n         2         2 3\n         3         3 4\n\n'
        
def test_hello_world_verbosities(): 
    from pyfreefem.examples.ex12_verbosity_output import runner   
    runner.execute({'message':'Hello world',\
                    'SOLVE_LAPLACE':1},verbosity=1,\
                   plot=False)
    check =  ' Load: lg_fem lg_mesh lg_mesh3 eigenvalue \n    1 : \n    2 : mesh Th=square(30,30);\n    3 : fespace Fh(Th,P1);\n    4 : Fh u,v;\n    5 : \n    6 : cout << "The value of SOLVE_LAPLACE is 1." << endl;\n    7 : solve laplace(u,v)=\n    8 :     int2d(Th)(dx(u)*dx(v)+dy(u)*dy(v))\n    9 :         -int2d(Th)(v)\n   10 :         +on(1,2,3,4,u=0);\n   11 : plot(u,cmm="Hello world");\n   12 :  sizestack + 1024 =1576  ( 552 )\n\n  -- Square mesh : nb vertices  =961 ,  nb triangles = 1800 ,  nb boundary edges 120\nThe value of SOLVE_LAPLACE is 1.\n  -- Solve : \n          min 2.20333e-63  max 0.0736069'
   
    assert '\n'.join(runner.rets[1].splitlines()[2:-3]) == check

    runner.execute({'message':'Hello world',\
                    'SOLVE_LAPLACE':1},verbosity=0,\
                   plot=False)
    assert runner.rets[1] == 'The value of SOLVE_LAPLACE is 1.\n'
    runner.execute({'message':'Hello world',\
                    'SOLVE_LAPLACE':1},\
                   plot=False)
    assert runner.rets[1] == 'The value of SOLVE_LAPLACE is 1.\n'
        
test_hello_world_verbosities()
