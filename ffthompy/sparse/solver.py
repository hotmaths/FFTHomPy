import numpy as np
from ffthompy import Timer
from ffthompy.sparse.objects import SparseTensor
from scipy.optimize import minimize_scalar

def cheby2TERM(Afun, B, x0=None, rank=None, tol=None, par=None, callback=None):
    """
    Chebyshev two-term iterative solver

    Parameters
    ----------
    Afun : a function, represnting linear function A in the system Ax =B
    B : sparse tensor representing vector B in the right-hand side of linear system
    x0 : sparse tensor representing initial approximation of solution of linear system
    par : dict
          parameters of the method
    callback :

    Returns
    -------
    x : resulting unknown vector
    res : dict
        results
    """
    if par is None:
        par = dict()
    if 'tol' not in par:
        par['tol'] = 1e-06
    if 'maxiter' not in par:
        par['maxiter'] = 1e7
    if 'eigrange' not in par:
        raise NotImplementedError("It is necessary to calculate eigenvalues.")
    else:
        Egv = par['eigrange']

    res={'norm_res': [],
           'kit': 0}

    bnrm2 = B.norm()
    Ib = 1.0/bnrm2
    if bnrm2 == 0:
        bnrm2 = 1.0

    if x0 is None:
        x=B
    else:
        x=x0

    r = B - Afun(x)
    r0=r.norm()
    res['norm_res'].append(Ib*r0)# For Normal Residue

    if res['norm_res'][res['kit']] < par['tol']: # if errnorm is less than tol
        return x, res

    M=SparseTensor(kind=x.kind, val=np.ones(x.N.size*[3,]), rank=1) # constant field
    FM=M.fourier().enlarge(x.N)

    d = (Egv[1]+Egv[0])/2.0 # np.mean(par['eigrange'])
    c = (Egv[1]-Egv[0])/2.0 # par['eigrange'][1] - d
    v = x*0.0
    while (res['norm_res'][res['kit']] > par['tol']) and (res['kit'] < par['maxiter']):
        res['kit'] += 1
        x_prev = x
        if res['kit'] == 1:
            p = 0
            w = 1/d
        elif res['kit'] == 2:
            p = -(1/2)*(c/d)*(c/d)
            w = 1/(d-c*c/2/d)
        else:
            p = -(c*c/4)*w*w
            w = 1/(d-c*c*w/4)
        v = (r - p*v).truncate(rank=rank, tol=tol)
        x = (x_prev + w*v)
        x=(-FM*x.mean()+x).truncate(rank=rank, tol=tol) # setting correct mean
        r = B - Afun(x)

        res['norm_res'].append((1.0/r0)*r.norm())
#        print(res['kit'])
#        print("w is:",w)
#        print(res['norm_res'][res['kit']])
#        print

        if callback is not None:
            callback(x)

    if par['tol'] < res['norm_res']: # if tolerance is less than error norm
        print("Chebyshev solver does not converges!")
    else:
        print("Chebyshev solver converges.")

    if res['kit'] == 0:
        res['norm_res'] = 0
    return x, res

def richardson(Afun, B, x0=None, rank=None, tol=None, par=None, norm=None):
    if isinstance(par['alpha'], float):
        omega=1./par['alpha']
    else:
        raise ValueError()
    res={'norm_res': [],
           'kit': 0}
    if x0 is None:
        x=B*omega
    else:
        x=x0

    if norm is None:
        norm=lambda X: X.norm()

    res['norm_res'].append(norm(B))

    M=SparseTensor(kind=x.kind, val=np.ones(x.N.size*[3,]), rank=1) # constant field
    FM=M.fourier().enlarge(x.N)

    norm_res=1e15

    while (norm_res>par['tol'] and res['kit']<par['maxiter']):
        res['kit']+=1
        residuum= B-Afun(x)
        norm_res = norm(residuum)
        if par['divcrit'] and norm_res>res['norm_res'][res['kit']-1]:
            break

        if par['adap_omega'] and norm_res >= res['norm_res'][res['kit']-1]:
            beta=Afun(residuum)
            ratio= norm_res/beta.norm()  # for bounds of omega search
            def objFunc(omega):
                return (residuum - beta*omega).norm()

            omega = minimize_scalar(objFunc,method='Bounded',bounds=[-ratio,ratio]).x

        x=(x+residuum*omega)
        x=(-FM*x.mean()+x).truncate(rank=rank, tol=tol) # setting correct mean

        res['norm_res'].append(norm_res)
#        print(res['kit'])
#        print("omega is  :",omega)
#        print(res['norm_res'][res['kit']])
#        print
    return x, res

def richardson_debug(Afun, B, x0=None, rank=None, tol=None, par=None, norm=None):
    if isinstance(par['alpha'], float):
        omega=1./par['alpha']
    else:
        raise ValueError()
    res={'norm_res': [],
           'kit': 0}
    if x0 is None:
        x=B*omega
    else:
        x=x0
    x=x.truncate(rank=rank, tol=tol)


    if norm is None:
        norm=lambda X: X.norm()

    norm_res=1e15
    while (norm_res>par['tol'] and res['kit']<par['maxiter']):
        res['kit']+=1
        tic=Timer(name='Afun(x)')
        Afunx=Afun(x)
        tic.measure()
        tic=Timer(name='residuum')
        residuum=B-Afunx
        tic.measure()
        tic=Timer(name='iteration')
        x=(x+residuum*omega).truncate(rank=rank, tol=tol)
        tic.measure()
        tic=Timer(name='norm_residuum')
        norm_res=norm(residuum)
        tic.measure()
        res['norm_res'].append(norm_res)

    res['norm_res'].append(norm(B-Afun(x)))
    return x, res
