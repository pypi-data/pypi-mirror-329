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
from numpy import array,  zeros, real,sqrt,exp, mgrid, transpose,median, mean as npmean
#from scipy.fftpack import fftn, ifftn
#from scipy.ndimage import fourier_gaussian,gaussian_filter,uniform_filter
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay
from CIMA.segments import SegmentInfo as SI


class TransformConvex:
    """

    A class to generates alpha_shape and convex hull from a Segment instance.

    """

    def __init__(self):
        pass

    def SR_ConvexHull_array(self,segment,filename=''):
        """
        return a matrix for the hull.
        flood fill hull
        """
        hull=self.SR_ConvexHull(segment)
        deln = Delaunay(points[hull.vertices])
        points=SI.Getcoord(segment)

        len_points=np.shape(points)
        idx = np.stack(np.indices(len_points, axis = -1))
        fill_map = np.nonzero(deln.find_simplex(idx) + 1)
        # (todo) why do we need deln if we don't use it?
        fill_map = np.zeros(len_points)
        fill_map[fill_map] = 1
        # to do rray to map
        #newMap.fullMap = fill_map
        #newMap.filename=filename
        #to modify it for mrc file

        return fill_map


    def SR_ConvexHull(self,segment):

        """

        Returns a Map instance based on a Convex Hull rapresentation of a segment.

        Arguments:
        * *Segment*
                array of Localisation objects
        """
        points=segment.Getcoord()
        hull = ConvexHull(points)
        volume = hull.volume
        return hull,points,volume

#TO pas to filled array
    def alpha_shape_3D(self,segment, alpha):
        """
        Compute the alpha shape (concave hull) of a set of 3D points.
        Arguments:
        * *Segment*
                array of Localisation objects
        * *alpha* - alpha value.
        * Note: Alpha shape and concave hull are generalizations of convex hull.
            An Alpha shape with alpha set to 0 is the convex hull.

        return
            outer surface vertex indices, edge indices, and triangle indices
        """
        pos=segment.Getcoord()
        tetra = Delaunay(pos)
        # Find radius of the circumsphere.
        # By definition, radius of the sphere fitting inside the tetrahedral needs
        # to be smaller than alpha value
        # http://mathworld.wolfram.com/Circumsphere.html
        tetrapos = np.take(pos,tetra.vertices,axis=0)
        normsq = np.sum(tetrapos**2,axis=2)[:,:,None]
        ones = np.ones((tetrapos.shape[0],tetrapos.shape[1],1))
        a = np.linalg.det(np.concatenate((tetrapos,ones),axis=2))
        Dx = np.linalg.det(np.concatenate((normsq,tetrapos[:,:,[1,2]],ones),axis=2))
        Dy = -np.linalg.det(np.concatenate((normsq,tetrapos[:,:,[0,2]],ones),axis=2))
        Dz = np.linalg.det(np.concatenate((normsq,tetrapos[:,:,[0,1]],ones),axis=2))
        c = np.linalg.det(np.concatenate((normsq,tetrapos),axis=2))
        r = np.sqrt(Dx**2+Dy**2+Dz**2-4*a*c)/(2*np.abs(a))

        # Find tetrahedrals
        tetras = tetra.vertices[r<alpha,:]
        # triangles
        TriComb = np.array([(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)])
        Triangles = tetras[:,TriComb].reshape(-1,3)
        Triangles = np.sort(Triangles,axis=1)
        # Remove triangles that occurs twice, because they are within shapes
        TrianglesDict = defaultdict(int)
        for tri in Triangles:TrianglesDict[tuple(tri)] += 1
        Triangles=np.array([tri for tri in TrianglesDict if TrianglesDict[tri] ==1])
        #edges
        EdgeComb=np.array([(0, 1), (0, 2), (1, 2)])
        Edges=Triangles[:,EdgeComb].reshape(-1,2)
        Edges=np.sort(Edges,axis=1)
        Edges=np.unique(Edges,axis=0)

        Vertices = np.unique(Edges)
        return Vertices,Edges,Triangles
