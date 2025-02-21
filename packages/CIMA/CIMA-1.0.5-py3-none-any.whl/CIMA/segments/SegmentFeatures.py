#===============================================================================
#     This file is part of CIMA.
#     
#     CIMA is a software designed to help the user in the manipulation 
#     and analyses of genomic super resolution localisation data. 
#     
#      Copyright  2019-2023 
#
#                Authors: Irene Farabella
# 
#     
#     
#===============================================================================

from scipy.spatial import ConvexHull
import numpy as np

from numpy import  array, int32, float32, zeros, real, argwhere, diag, histogram, dot, matrix, amin, arange,\
                   indices, ravel, all as all_points, delete, transpose, searchsorted, newaxis, where, meshgrid,\
                   ma, sum as numsum,median,sqrt as srt, digitize, nonzero, floor, ceil, amax, mean as npmean,\
                   std as npstd, square as npsquare, tanh as np_tanh,set_printoptions
                
import glob
from CIMA.maps.MapParser import MapParser
from CIMA.maps.VQ import *
from CIMA.maps.ScoringFunctions import ScoringFunctions
import numpy as np 
from scipy.stats import kurtosis, skew
import CIMA.utils.Vector  as Vector
from CIMA.maps import  DensityProprieties as DS
from CIMA.segments import SegmentFeatures as SF
from math import pi
from scipy.spatial import cKDTree

#fraction-of-overlap=
#Numer ij pairs d<=200nm / Ni x Nj.


def get_rgyration(segment):
    """
    Calculate the radius of gyration for a given segment.

    Args:
    * segment (Segment): An object representing the segment for which the radius of gyration is to be calculated. 

    Returns:
    * float: The radius of gyration of the segment.
    """
    vc = segment.calculate_centre_of_mass()
    dist_vecs = segment.atomList[['x','y','z']].values - np.array(list(vc)).reshape(1,-1)
    dists = np.linalg.norm(dist_vecs, axis=1)
    return np.sqrt(np.mean(dists**2))


def _getFittedEllipsoid(segment,tolerance=0.01,modeDOF='', return_vecs=False):
    """
    Fits a minimum volume enclosing ellipsoid around a set of 3D coordinates.

    This function computes the parameters of an ellipsoid that minimally encloses the coordinates 
    within a given Segment object. It offers options for different degrees of freedom (DOF) in the 
    ellipsoid fitting process, based on an adaptation of Yury Petrov's MATLAB ellipsoid fitting 
    function.

    Args:
        segment (Segment): The Segment object containing the coordinates to be enclosed.
        tolerance (float, optional): Tolerance level for the fitting process. Defaults to 0.01.
        modeDOF (str, optional): Specifies the degree of freedom mode for fitting:
                                 - '' (default): 9-DOF mode, full fitting with rotations.
                                 - 0: 6-DOF mode, constrained fitting without rotation.
        return_vecs (bool, optional): If True, returns eigenvectors representing the orientation of 
                                      the ellipsoid. Defaults to False.

    Returns:
        tuple: A tuple containing:
            - centre (ndarray): The (x, y, z) coordinates of the ellipsoid's center.
            - orderradii (ndarray): The lengths of the ellipsoid's principal semi-axes.
            - ellipVol (float): The volume of the fitted ellipsoid.
            - evecs (ndarray, optional): The orientation vectors of the ellipsoid's axes (only if `return_vecs` is True).

    Note: this function is based on https://github.com/marksemple/pyEllipsoid_Fit adaptation of Yury Petrov's ellipsoid_fit function for MATLAB.
    """
    coord=segment.Getcoord()
    X = coord[:, 0]
    Y = coord[:, 1]
    Z = coord[:, 2]
    # AlGEBRAIC EQUATION FOR ELLIPSOID, from CARTESIAN DATA
    if modeDOF == '':  # 9-DOF MODE
        D = np.array([X * X + Y * Y - 2 * Z * Z,
                      X * X + Z * Z - 2 * Y * Y,
                      2 * X * Y, 2 * X * Z, 2 * Y * Z,
                      2 * X, 2 * Y, 2 * Z,
                      1 + 0 * X]).T
    elif modeDOF == 0:  # 6-DOF MODE (no rotation)
        D = np.array([X * X + Y * Y - 2 * Z * Z,
                      X * X + Z * Z - 2 * Y * Y,
                      2 * X, 2 * Y, 2 * Z,
                      1 + 0 * X]).T
    # THE RIGHT-HAND-SIDE OF THE LLSQ PROBLEM
    d2 = np.array([X * X + Y * Y + Z * Z]).T #d2 = x .* x + y .* y + z .* z; % the RHS of the llsq problem (y's)
    # SOLUTION TO NORMAL SYSTEM OF EQUATIONS #u = ( D' * D ) \ ( D' * d2 );  % solution to the normal equations
    u = np.linalg.solve(D.T.dot(D), D.T.dot(d2))
    # chi2 = (1 - (D.dot(u)) / d2) ^ 2
    # CONVERT BACK TO ALGEBRAIC FORM
    if modeDOF == '':  # 9-DOF-MODE
        a = np.array([(u[0] + 1) * (u[1] - 1)])
        b = np.array([(u[0] - 2) * (u[1] - 1)])
        c = np.array([(u[1] - 2) * (u[0] - 1)])
        v = np.concatenate([a, b, c, u[2:, :]], axis=0).flatten()
    elif modeDOF == 0:  # 6-DOF-MODE
        a = u[0] + 1 * u[1] - 1
        b = u[0] - 2 * u[1] - 1
        c = u[1] - 2 * u[0] - 1
        zs = np.array([0, 0, 0])
        v = np.hstack((a, b, c, zs, u[2:, :].flatten()))
    else:
        pass
    # PUT IN ALGEBRAIC FORM FOR ELLIPSOID
    A = np.array([[v[0], v[3], v[4], v[6]],
                  [v[3], v[1], v[5], v[7]],
                  [v[4], v[5], v[2], v[8]],
                  [v[6], v[7], v[8], v[9]]])
    # FIND CENTRE OF ELLIPSOID
    centre = np.linalg.solve(-A[0:3, 0:3], v[6:9])
    # FORM THE CORRESPONDING TRANSLATION MATRIX
    T = np.eye(4)
    T[3, 0:3] = centre
    # TRANSLATE TO THE CENTRE, ROTATE #% translate to the center R = T * A * T';
    R = T.dot(A).dot(T.T)
    # SOLVE THE EIGENPROBLEM
    evals, evecs = np.linalg.eig(R[0:3, 0:3] / -R[3, 3])
    #order = np.argsort(evals)
    # CALCULATE SCALE FACTORS AND SIGNS
    radii = np.abs(np.sqrt(1 / abs(evals)))
    #sgns = np.sign(evals)
    #radii *= sgns
    #print ("radii",radii)
    order = np.argsort(-radii)
    # orderradii = -np.sort(-radii)
    orderradii = radii[order]
    #print ("orderradii:",orderradii)
    ellipVol=np.abs(np.round(4./3.*np.pi*radii[0]*radii[1]*radii[2]))
    if(return_vecs):
        return (centre, orderradii, ellipVol, evecs[order])
    return (centre, orderradii, ellipVol)

def _principal_axes(P):

	# center of the ellipse
	center = np.mean(P, 0)
	coord = P - center
	inertia = np.dot(coord.transpose(), coord)#AT*A
	e_values, e_vectors = np.linalg.eig(inertia)
	order = np.argsort(e_values)
	eval3, eval2, eval1 = e_values[order]
	axis3, axis2, axis1 = e_vectors[:, order].transpose()

	return eval1, eval2, eval3,axis3, axis2, axis1


def GetEllipticity(segment,verbose=False):
    """
    Calculate the ellipticity of a given segment based on its 3D coordinates.

    Args:
    * segment:  An object representing the segment for which the ellipticity is to be calculated.
    * verbose (bool, optional): If True, returns additional principal axis information. Defaults to False.

    Returns:
    * float: ellipticity.
    * tuple: If verbose is True, returns a tuple containing:
        * - float: The ellipticity.
        * - float: The maximum eigenvalue.
        * - float: The intermediate eigenvalue.
        * - float: The minimum eigenvalue.
        *  - ndarray: The principal axis corresponding to the minimum eigenvalue.
        * - ndarray: The principal axis corresponding to the intermediate eigenvalue.
        * - ndarray: The principal axis corresponding to the maximum eigenvalue.
    """
    coordin = segment.atomList[['x','y','z']].values
    eval_max, eval_intermediate, eval_min ,axis3, axis2, axis1=_principal_axes(coordin)
    if verbose:
        return (eval_intermediate/eval_max), eval_max, eval_intermediate, eval_min ,axis3, axis2, axis1
    else:
        return (eval_intermediate/eval_max)

        
def GetEccentricity(segment,verbose=False):
    """
    Calculate the Eccentricity of a given segment based on its 3D coordinates.

    Args:
    * segment:  An object representing the segment for which the Eccentricity is to be calculated.
    * verbose (bool, optional): If True, returns additional principal axis information. Defaults to False.

    Returns:
    * float: Eccentricity.
    * tuple: If verbose is True, returns a tuple containing:
        * - float: The Eccentricity.
        * - float: The maximum eigenvalue.
        * - float: The intermediate eigenvalue.
        * - float: The minimum eigenvalue.
        *  - ndarray: The principal axis corresponding to the minimum eigenvalue.
        * - ndarray: The principal axis corresponding to the intermediate eigenvalue.
        * - ndarray: The principal axis corresponding to the maximum eigenvalue.
    """
    coordin = segment.atomList[['x','y','z']].values
    eval_max, eval_intermediate, eval_min ,_, _, _=SF._principal_axes(coordin)
    if verbose:
        return (eval_min/eval_intermediate), eval_max, eval_intermediate, eval_min
    else:
        return (eval_min/eval_intermediate)


def getMVEE(P, tolerance=0.1, max_iterations=100):
    '''
    Computes the Minimum Volume Enclosing Ellipsoid (MVEE) for a set of points.

    This function calculates the smallest ellipsoid, by volume, that can enclose a given set of 
    points in a d-dimensional space. The iterative algorithm adjusts weights assigned to each 
    point until convergence is achieved within the specified tolerance.

    Arguments:
    * P (numpy.ndarray): An (N, d)-shaped numpy array with each row representing a coordinate in 
                           d-dimensional space.
    * tolerance (float, optional): Convergence tolerance for the iterative algorithm. Defaults to 0.1.
    * max_iterations (int, optional): Maximum number of iterations for the algorithm. Defaults to 100.

    Returns:
    * c (numpy.ndarray): A (d,)-shaped array representing the center of the ellipsoid.
    * V (numpy.ndarray): A (d, d)-shaped array where each column represents the eigenvector of the 
                           ellipsoid's principal axis directions.
    * rs (numpy.ndarray): A (d,)-shaped array containing the lengths of the ellipsoid's radii along 
                            the principal axes, sorted in descending order.
    
    Both `V` and `rs` are sorted in order of decreasing radius length.

    References:
    - Moshtagh, N. (2005). Minimum volume enclosing ellipsoid. Convex optimization, 111(January), 1-9.
    - https://stackoverflow.com/questions/1768197/bounding-ellipse/1768440#1768440
    '''

    # Dimension of the points
    d = P.shape[1]
    # Number of points
    N =P.shape[0]  
    Q = np.concatenate([P.T,np.ones((1,N))], axis=0)
    count = 1
    err = 1
    u = (1/N) * np.ones(N)       
    it=-1
    while (err > tolerance and it<max_iterations):
        it+=1
        X = (Q @ np.diag(u)) @ Q.T # d x d
        M = np.diag((Q.T @ np.linalg.inv(X)) @ Q) # N
        maximum = max(M)
        j = np.argmax(M)
        step_size = (maximum - d -1)/((d+1)*(maximum-1))
        new_u = (1 - step_size)*u
        new_u[j] = new_u[j] + step_size
        err = np.linalg.norm(new_u - u)
        count = count + 1
        u = new_u
    U = np.diag(u) # N x N
    A = (1/d) * np.linalg.inv(((P.T @ U) @ P) - (P.T @ u.reshape(-1,1))@(P.T @ u.reshape(-1,1)).T )
    c = (P.T @ u.reshape(-1,1)).flatten()
    # return A,c
    U, q, V = np.linalg.svd(A)
    rs = 1/np.sqrt(q)
    return c, V, rs

def getMVEEEllipticity(segment):
    '''
    Returns ellipticity (intermidiate radius over largest = elongation) of the MVEE of segment
    Based on T. Zingg classification (Beitrag Zur Schotteranalyse ETH Zurich, Switzerland (1935) Ph.D. thesis)
    Angelidakis, V., Nadimi, S., & Utili, S. (2022). Elongation, flatness and compactness indices to characterise particle form. Powder Technology, 396, 689-695.
    '''
    c, V, rs = getMVEE(segment.Getcoord())
    return rs[1]/rs[2]

def getMVEEEccentricity(segment):
    '''
    Returns eccentricity (smallest radius over intermidiate = flatness) of the MVEE of segment
    Based on T. Zingg classification (Beitrag Zur Schotteranalyse ETH Zurich, Switzerland (1935) Ph.D. thesis)
    Angelidakis, V., Nadimi, S., & Utili, S. (2022). Elongation, flatness and compactness indices to characterise particle form. Powder Technology, 396, 689-695.
    '''
    c, V, rs = getMVEE(segment.Getcoord())
    return rs[0]/rs[1]