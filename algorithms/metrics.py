""" Provide various metrics for calculating distances between two points 
General form - metric(x, y) returns real number distance between points x and y
"""
import numpy as np

"""
################################################################################
Riemannian
################################################################################
"""
def euclidean(x, y):
    """Calculcate Euclidean distance between x and y """
    assert len(x)==len(y), 'ERROR - vectors in Euclidean metric have different lengths'
    return np.sum((np.array(x) - np.array(y))*(np.array(x) - np.array(y)))

def spherical(x_, y_):
    """Calculate distance on the surface of a d-sphere between points x and y
    
    We are using standard angular coordinates where the x[d-1] is in (0, 2*pi)
    and the other angles are in (0, pi)"""
    assert len(x_)==len(y_), 'ERROR - vectors in spherical metric have different lengths'
    x, y = angular_to_cartesian(x_), angular_to_cartesian(y_)
    cos_psi = np.dot(x,y)
    psi = np.arccos(cos_psi)
    return psi
       
def angular_to_cartesian(a):
    """Convert D angular spherical coordinates to D+1 cartesian - assume radius=1 """
    D = len(a)
    x = np.ones(D+1)
    i = 0
    for i in range(D):
        x[i] *= np.cos(a[i])
        x[i+1:] *= np.sin(a[i])
    return x

def cartesian_to_angular(a):
    """Convert d cartesian to d-1 angular spherical coordinates - assume radius=1 """
    D = len(a)
    x = np.zeros(D-1)
    for i in range(D-1):
        psi = np.arccos(a[i] / np.sqrt(np.sum((a[i:])**2)))
        x[i] = psi
    if a[-1] < 0:
        x[-1] = (2.*np.pi) - x[-1]
    return x

"""
################################################################################
Lorentzian
################################################################################
"""
def minkowski(x, y):
    """Calculate Minkowski separation between x and y using -++...+ convention"""
    assert len(x)==len(y), 'ERROR - vectors in Minkowski metric have different lengths'
    dt = x[0] - y[0]
    dt2 = dt * dt
    dx = np.array([x[i] - y[i] for i in range(1, len(x))])
    dx2 = dx * dx
    dx2sum = sum(dx2)
    return dx2sum - dt2 
      
def minkowski_periodic(x, y, L=[]):
    """Calculate Minkowski separation between x and y using -++...+ convention
       Periodic boundary conditions in spatial coordinates are given in L
       If len(L) < D-1 then assume no boundary on other spatial dimensions"""
    D = len(x)
    assert len(y) == D, 'ERROR - vectors in Minkowski metric have different lengths'
    # fill in remaining box dimensions with None
    # JC - we can probably make this more efficient later by vectorising the
    #      operation if the if L_d line
    while len(L) < (D-1):
        L.append(None)
    dt = x[0] - y[0]
    dt2 = dt * dt
    ds2 = -1 * dt2
    for d in range(1, D):
        L_d = L[d-1] # the first dimension in the coords is time so exclude it
        if L_d:
            dx2 = min((x[d]-y[d])**2, (x[d]-y[d]+L_d)**2, (x[d]-y[d]-L_d)**2)
        else:
            dx2 = (x[d]-y[d])**2
        dz2 += dx2
    return ds2

def de_sitter(x, y):
    """ Calculate de Sitter separation between x and y in conformal coordinates"""
    dt = x[0] - y[0]
    dt2 = dt*dt
    dx = spherical(x[1:], y[1:])
    dx2 = dx*dx
    return (dx2 - dt2)


"""
################################################################################
# HELPER FUNCTIONS
################################################################################
"""
def sq_separations(R, metric):
    """ Return square array of squared Minkowski separations from coords R
        c - speed of light"""
    S = np.zeros((R.shape[0], R.shape[0]))
    for i in range(R.shape[0]):
        for j in range(R.shape[0]):
            S[i, j] = metric(R[i,:], R[j,:])
    return S
    
if __name__ == "__main__":
    print __doc__
        
        
        
        
        
    
