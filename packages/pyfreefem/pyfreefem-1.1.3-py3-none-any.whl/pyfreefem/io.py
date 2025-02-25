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
"""PyFreeFEM input/output functions."""
    
import os
import scipy.sparse as sp
import numpy as np
import time
import sys
import struct
import subprocess
import threading
import queue
import inspect
    


try:
    import colored as col

    def colored(text, color=None, attr=None):
        if color:
            text = col.stylize(text, col.fg(color))
        if attr:
            text = col.stylize(text, col.attr(attr))
        return text
except:
    def colored(text, color=None, attr=None):
        return text


def display(message, level=0, debug=0, color=None, attr=None, end='\n',
            flag=None):
    """A function for displaying messages with a flexible tunable level of verbosity.


    :param message:  Text to be printed.
    :param level:   Level of importance of the message which will be actually 
                       printed if ``debug >= level`` or if ``flag`` is ``stdout`` or ``stderr``.
    :type level: int
    :param debug: Desired level of verbosity; the higher and the more information will  
                  be displayed.
    :type debug: int
    :param color: Color of the displayed message. Follows the convention of the     
                  `colored <https://pypi.org/project/colored/>`_ package.
    :param attr:  Formatting of the displayed message. Follows the  
                  convention of the     
                  `colored <https://pypi.org/project/colored/>`_ package.

    :param end:   character appended to the end of a message. Will remove the   
                  final line carriage return if ``end=''``.  

    :param flag:  an indicator to use to indicate if the argument ``message`` comes     
                  from ``stdout`` or ``stderr`` pipe. 
    
    .. note::   
        
       For advanced projects, it can be useful to override :func:`pyfreefem.io.display`,  
       for instance to redirect messages to a file.
    """
    if color or attr:
        message = colored(message, color, attr)
    if debug >= level or flag in ['stdout','stderr']:
        print(message, end=end, flush=True)

    
# check if stdbuf is available
def is_command_available(command):
    try:
        # Try to execute the command with `--version` to check if it is available
        result = subprocess.run([command, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # If the command runs successfully, it's available
        return result.returncode == 0
    except FileNotFoundError:
        # If the command is not found, it raises a FileNotFoundError
        return False
WITH_STDBUF = is_command_available('stdbuf')
if not WITH_STDBUF: 
    display("[PyFreeFEM] Warning, the command stdbuf is not available. Standard output capturing may not work as expected.",color="orange_4a")

tclock = dict()
def tic(ref=0):
    global tclock
    tclock[ref] = time.time()

def toc(ref=0):
    global tclock
    return format(time.time()-tclock[ref],"0.2f")+"s"

class ExecException(Exception):
    """ An exception raised when a FreeFem++ subprocess fails"""
    def __init__(self, message, returncode, stdout, stderr, mix):
        super().__init__(message)
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.mix = mix

def readFFArray(ffarray : str, binary = False):
    """
    Read an FreeFEM array stored in a file ``ffarray``. 
        
    For instance, if the following ``.edp`` file is executed:

    .. code:: freefem

       real[int] table = [1, 2, 3, 4, 5];
       {
           ifstream f("file.gp");
           f << table;
       }

    Then
        
    .. code:: python

       readFFArray("file.gp") 

    returns the numpy array [1, 2, 3, 4, 5].    
        
    :param ffarray: file name of a FreeFEM array stored with ``ifstream``.
    :return: numpy array identical to ``ffarray``.
    """
    if binary:
        with open(ffarray, 'rb') as f:
            # Read the number of rows (n) and columns (m)
            n = struct.unpack('q', f.read(8))[0]  # 8 bytes for int64_t

            # Read the entire matrix data into a flat list of values
            num_elements = n 
            flat_data = struct.unpack(f'{num_elements}d', f.read(num_elements * 8))  # 'd' is for double (float64)

            # Convert the flat data to a numpy array and reshape it into an (n, m) matrix
            array = np.array(flat_data)
    else:
        with open(ffarray, "r") as f:
            return np.asarray([float(x) for line in f.readlines()[1:]
                               for x in line.split()])
    return array


def writeFFArray(A: np.ndarray, fileName: str, binary = False):
    """
    Store a numpy array into a FreeFEM array file that can be read with ``ofstream``.

    :param A:  a `numpy.array <https://numpy.org/doc/stable/reference/generated/numpy.array.html>`_ data structure
    :param fileName: an output file name to save the array ``A``.   
    """
    if binary:
        n = len(A)  
        
        with open(fileName, 'wb') as f:
            # Write the dimensions (n and m) as 64-bit integers
            f.write(struct.pack('q', n))  # Using 'q' for signed long long (64-bit)
            
            # Write the matrix data as a flat array
            f.write(struct.pack(f'={n}d', *A))  # 'd' -> float64
    else:
        text = f"{len(A)}\t\n"
        lines = [A[5*k:5*(k+1)] for k in range(0, int(np.ceil(len(A)/5)))]
        for line in lines:
            text += ''.join([f"\t  {x}" for x in line])+"\n"
        text = text[:-1]+"\t"
        with open(fileName, "w") as f:
            f.write(text)

def writeFF2DArray(A, filename):
    """
    Save a dense matrix into a FreeFEM matrix file (a real[int,int]) that can be read with ``ofstream``. 

    :param A: A `scipy.sparse.csc_matrix <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html>`_  
              or a `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ dense matrix.
    :param fileName: output file name for saving the matrix ``A``.  
    """ 
    # Ensure the matrix is of type float64 (similar to FreeFEM's default)
    # Get matrix dimensions
    n, m = A.shape
    
    with open(filename, 'wb') as f:
        # Write the dimensions (n and m) as 64-bit integers
        f.write(struct.pack('qq', n, m))  # Using 'q' for signed long long (64-bit)
        
        # Write the matrix data as a flat array
        f.write(struct.pack(f'={n * m}d', *A.ravel(order='F')))  # 'd' -> float64

def writeFFMatrix(A, fileName):
    """
    Save a dense or a sparse matrix into a FreeFEM matrix file that can be read with ``ofstream``. 

    :param A: A `scipy.sparse.csc_matrix <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html>`_  
              or a `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_ dense matrix.
    :param fileName: output file name for saving the matrix ``A``.  
    """
    if isinstance(A,np.ndarray):
        preamble = " ".join(map(str,A.shape))+"\t\n"
        preamble += "\n".join(["\t   "+"   ".join(map(str,line)) for line in A.tolist()])
        preamble += "\n\t"
    else:
        (I, J, V) = sp.find(A)
        (n, m) = A.shape
        nnz = A.nnz
        preamble = f"#  HashMatrix Matrix (COO) 0x2d90200\n"
        preamble += "#    n       m        nnz     half     fortran   state  \n"
        preamble += f"{n} {m} {nnz} 0 0 0 0 \n"

        lines = [f"     {i}     {j} {d}" for (i, j, d) in zip(I, J, V)]
        preamble = preamble+"\n".join(lines)
        preamble += "\n"
    with open(fileName, "w") as f:
        f.write(preamble)

def readFF2DArray(filepath):  
    """
    Read a matrix file generated by a FreeFEM script (a `real[int,int]`).         
    If the matrix stored by the FreeFEM script is a sparse matrix,  
    then :func:`pyfreefem.io.readFFMatrix`   
    returns a   
    `scipy.sparse.csc_matrix <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html>`_.

    If it is a dense matrix ,   
    then :func:`pyfreefem.io.readFFMatrix` returns a `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_.
        
    :param filepath: file name of a FreeFEM matrix stored with ``ifstream``.
    :return: A `numpy.ndarray` matrix if `ffmatrix` contains a dense matrix, or a `scipy.sparse.csc_matrix` if  
             `ffmatrix` contains a sparse matrix.   
             """
    with open(filepath, 'rb') as f:
        # Read the number of rows (n) and columns (m)
        n = struct.unpack('q', f.read(8))[0]  # 8 bytes for int64_t
        m = struct.unpack('q', f.read(8))[0]  # 8 bytes for int64_t

        # Read the entire matrix data into a flat list of values
        num_elements = n * m
        flat_data = struct.unpack(f'{num_elements}d', f.read(num_elements * 8))  # 'd' is for double (float64)

        # Convert the flat data to a numpy array and reshape it into an (n, m) matrix
        matrix = np.array(flat_data).reshape((n, m),order='F')
    return matrix

def readFFMatrix(ffmatrix : str):
    """
    Read a matrix file generated by a FreeFEM script. For instance,     
    if the following ``.edp`` file is run:  
        
    .. code:: freefem

       matrix table = [[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]];
       {
           ifstream f("file.gp");
           f << table;
       }
    
    Then
        
    .. code:: python

       readFFMatrix("file.gp") 

    returns the numpy matrix [[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]]. 
        
    If the matrix stored by the FreeFEM script is a sparse matrix, then :func:`pyfreefem.io.readFFMatrix`   
    returns a `scipy.sparse.csc_matrix <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csc_matrix.html>`_.

    If it is a dense matrix, then :func:`pyfreefem.io.readFFMatrix` returns a `numpy.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`_.
        
    :param ffmatrix: file name of a FreeFEM matrix stored with ``ifstream``.
    :return: A `numpy.ndarray` matrix if `ffmatrix` contains a dense matrix, or a `scipy.sparse.csc_matrix` if  
             `ffmatrix` contains a sparse matrix.

    """
    with open(ffmatrix, 'r') as f:
        lines = f.readlines()
    i = []
    j = []
    data = []
    if lines[0].startswith('#  HashMatrix'):
        shape = tuple([int(x) for x in lines[2].strip().split()[:2]])
        if len(lines)>3:
            matrix = np.loadtxt(lines[3:])  
            I = matrix[:,0].astype(int) 
            J = matrix[:,1].astype(int) 
            data = matrix[:,2]
            indices = np.where(np.abs(data)>1e-15)[0]
            I, J, data = I[indices], J[indices], data[indices]
        else:
            I, J= [], []
        return sp.csc_matrix((data, (I,J)),shape=shape)
    elif len(lines[0].strip().split())==2:
        shape = tuple([int(x) for x in lines[0].strip().split()])
        data = [line.strip().split() for line in lines[1:shape[0]+1]]
        return np.asarray(data, dtype=float)
    else:
        for (k, line) in enumerate(lines[4:]):
            i.append(int(line.split()[0])-1)
            j.append(int(line.split()[1])-1)
            data.append(float(line.split()[2]))
    return sp.csc_matrix((data, (i, j)))

def enqueue_stream(stream, queue, type):
    if not WITH_STDBUF:
        for line in iter(stream.readline, ''):
            queue.put(str(type)+ line)
    else:
        for line in iter(stream.readline, b''):
            queue.put(str(type) + line.decode('utf-8', errors='replace'))
    stream.close()


def enqueue_process(process, queue):
    process.wait()
    queue.put('x')

    
def exec2(cmd, debug=0, level=1, silent=True):
    """Interface with `subprocess.Popen <https://docs.python.org/fr/3/library/subprocess.html>`_.   
       Execute a shell command ``cmd`` and pass standard output and standard errors 
       to the function :func:`pyfreefem.io.display`.
        
       :param cmd: A shell command. For instance ``cmd="FreeFem++ script.edp -v 1 -wg"``.
       :type cmd: str
        
       :param debug: An input ``debug`` parameter, tuning the desired level of verbosity.   
                     The command ``cmd`` will be displayed if ``debug>=level``
       :type debug: int

       :param level: Degree of importance of the executed ``command``.
                     The command ``cmd`` will be displayed if ``debug>=level``
       :type level: int
        
       :param silent: If set to ``True``, no standard output will be displayed.
       :type silent: boolean
        
       .. note::    
            
          By default, the standard output is displayed whatever the value of level and  
          debug because :func:`pyfreefem.io.display` prints ``stdout`` and ``stderr``   
          by watching its ``flag`` argument. Use a custom :func:`pyfreefem.io.display`    
          function to change this behaviour.

    """
    display(colored(cmd, color="indian_red_1a"), level=level, debug=debug, end='',
            flag='shell')
    # Put a line break to separate from the stdout 
    if not silent:
        display("",level=level,debug=debug,flag='')
    tic(121)
    if not WITH_STDBUF: 
        proc = subprocess.Popen(cmd,shell=True,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                universal_newlines = True,
                                bufsize = 1
                                )
    else:
        proc = subprocess.Popen("stdbuf -oL "+cmd,shell=True,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE
                                )
    q = queue.Queue()
    to = threading.Thread(target=enqueue_stream, args=(proc.stdout, q,1))
    te = threading.Thread(target=enqueue_stream, args=(proc.stderr, q,2))
    tp = threading.Thread(target=enqueue_process, args=(proc, q))
    te.start()
    to.start()
    tp.start()

    stdout = "" 
    stderr = "" 
    mix = "" 
    while True:
        line = q.get()
        if line[0] == 'x':
            break
        if line[0] == '1':
            line = line[1:]
            stdout += line
            mix += line 
            if not silent:
                display(line,level=level+1,debug=debug,end='',flag='stdout')
        if line[0] == '2':
            line = line[1:]
            stderr += line
            mix += line 
            if not silent:
                display(line,level=level+1,debug=debug,attr="dim",end='',flag='stderr')
    tp.join()
    te.join()
    to.join()
    if mix and not silent:
        if not mix.endswith('\n'):
            display("",level,debug)
        display("Finished in",level,debug,color="cyan",end="",flag="")
    display(' ('+toc(121)+')', level=level, debug=debug,color="cyan",
            flag="time")

    if proc.returncode != 0:
        raise ExecException('Error : the process "'
                        + colored(cmd, "red")
                        + '" failed with return code '+str(proc.returncode)
                        + ".",proc.returncode,stdout,stderr,mix)
    return proc.returncode, stdout, stderr, mix
    
def make_dictionary(*args):
    frame = inspect.currentframe().f_back  # Get the caller's frame
    names = {id(v): k for k, v in frame.f_locals.items()}  # Map object ids to variable names
    return {names.get(id(arg), f'unknown_{i}'): arg for i, arg in enumerate(args)}

def extract(d, *keys):  
    if len(keys)==1:    
        return d[keys[0]]
    else:
        return tuple(d[k] for k in keys)

def get_root(): 
    file = inspect.stack()[1][1]
    return os.path.dirname(file)

def tic(ref=0):
    global tclock
    tclock[ref] = time.time()


def toc(ref=0):
    global tclock
    return format(time.time()-tclock[ref], "0.2f")+"s"
