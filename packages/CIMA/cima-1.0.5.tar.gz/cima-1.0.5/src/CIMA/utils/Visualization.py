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


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from CIMA.maps.MapFeatures import getPointsFromMap
from CIMA.maps.DensityProprieties import calculate_map_threshold_SR
import pyvista as pv
from scipy.spatial import ConvexHull



def plotClustering2DProjections(coords, labels=None, background_coords=None, show_noise=False,
        annot=False, cmap='gist_ncar', point_size_front=0.1, point_size_back=0.1, colorbar=False, legend=False, alpha=0.1):
    '''
    *Arguments*:
    * *coords*: 3d coordinates of the points
    * *labels*: labels by which to color points. Those with label=-1 are considered noise
    * *show_noise*: if false noise points are not diplayed
    * *background_coords*: a set of coords to be displayed behind all the others and colored in gray
    * *annot*: if true the center of mass of each cluster (the set of points with the same label value) is annotated with the cluster number
    * *cmap*: the cmap for coloring the points,
    * *point_size_front*: size of the points in the foreground
    * *point_size_back*: size of the points in the background
    * *colorbar*: if true show a colorbar near each subplot
    * *legend*: whether to show the legend of colors
    * *alpha*: the transparency of points colors

    *Returns*:
    a figure containing the 3 subplots

    Creates 3 scatter plots representing the 2d projections.
    '''

    if(not (labels is None)):
        points1 = coords if show_noise else coords[labels>=0]
        if len(np.unique(labels[labels>=0])) > 1:
            colors1_full = np.ones((len(coords)))*-1
            colors1_full[labels>=0] = labels[labels>=0]
        else:
            colors1_full = labels.copy()
        colors1 = colors1_full if show_noise else colors1_full[labels>=0]
    else:
        points1 = coords
        colors1 = np.zeros((len(coords)))
    
    if(annot):
        # compute the centers of mass of the clusters for future annotation
        cluster_inds_wihout_noise = set(np.unique(labels)) - set([-1])
        coms_dict = {}
        for c in cluster_inds_wihout_noise:
            c_coords = coords[labels == c]
            coms_dict[c] = getCoM(c_coords)

    fig, axs = plt.subplots(3,1, figsize=(7,10))
    axs = iter(axs.flatten())
    axs_names = ['x','y','z']
    
    cmap = plt.get_cmap(cmap).copy()
    if(cmap is None):
        cmap = getCustomColormap() # plt.get_cmap('gist_ncar')
    cmap.set_under('gray')

    # for each projection axis ...
    for ax_sel in [[0,1],[0,2],[1,2]]:
        ax = next(axs)
        ax.set_aspect('equal')
        sc = ax.scatter(points1[:,ax_sel[0]],
                    points1[:,ax_sel[1]], c=colors1,
                    s=point_size_front, alpha=alpha, cmap=cmap, vmin=-0.1, vmax=max(1.0, max(colors1)) if len(colors1)>0 else 1.0) # , vmax=1.0
        ax.set_xlabel(axs_names[ax_sel[0]])
        ax.set_ylabel(axs_names[ax_sel[1]])
        if(annot):
            # write cluster names on their centers of mass
            for c in cluster_inds_wihout_noise:
                ax.text(coms_dict[c][ax_sel][0], coms_dict[c][ax_sel][1],c,fontdict={'size': 5})
        if(not background_coords is None):
            # plot the background points
            ax.scatter(background_coords[:,ax_sel[0]],
                background_coords[:,ax_sel[1]], c='gray',
                s=point_size_back, alpha=1, zorder=-1)
        
        if(ax_sel == [0,2]):
            if(legend):
                legend1 = ax.legend(*sc.legend_elements(num=np.unique(labels)[:10]),
                    loc="upper left", title="Label")
                ax.add_artist(legend1)
                ax.set_xmargin(0.3)
                ax.set_ymargin(0.3)
            else:
                ax.set_xmargin(0.1)
                ax.set_ymargin(0.1)
            if(colorbar): plt.colorbar(sc, ax=ax)
            
        else:
            ax.set_xmargin(0.1)
            ax.set_ymargin(0.1)

    return fig

def plotClustering3D(coords, true_labels=None, single_noise_color=True, show_noise=False, plotter=None, cmap='gist_ncar', opacity=None,
                     custom_clim=None, points_size=None, **kwargs):
    '''
    Arguments:
    * coords: 3d coordinates of the points
    * true_labels: labels by which to color points. Those with label<0 are considered noise
    * single_noise_color: whether to diplay all points with label<0 in grey or to apply cmap also on them.
        If show_noise is false this parameter has no effect
    * show_noise: if false, noise points are not diplayed,
    * plotter: if not None it will be used to plot the points,
    * cmap: the cmap for coloring the points
    * **kwargs: arguments that will be passed to pv.Plotter.add_points
    
    
    Returns:
    * a pyvista Plotter object with the coordinates plotted in it


    Creates a 3-d pyvista scatter plot of the provided coordinates.
    The result is not diplayed automatically. You need to call the show() method of the returned object to display the result.
    '''
    import pyvista as pv

    if(not true_labels is None):
        '''if(single_noise_color):
            true_cols = np.ones(true_labels.shape)*-1
            true_cols[true_labels>=0] = true_labels[true_labels>=0]
        else:
            true_cols = true_labels.copy()'''
        true_cols = true_labels.copy()
    else:
        true_cols = np.zeros((len(coords)))

    points1 = coords if show_noise else coords[true_cols>=0]
    colors1 = true_cols if show_noise else true_cols[true_cols>=0]

    if plotter is None: plotter = pv.Plotter(shape=(1,1))

    if(opacity is None):
        opacity = np.ones(len(points1), dtype='float')
    
    cmap = plt.get_cmap(cmap).copy()
    if(cmap is None):
        cmap = getCustomColormap()
    cmap.set_under('gray')
    if(len(points1)>0):
        if(points_size is not None):
            mesh = pv.PolyData(points1)
            mesh["radius"] = points_size

            # Low resolution geometry
            geom = pv.Sphere(theta_resolution=8, phi_resolution=8)

            # Progress bar is a new feature on master branch
            glyphed = mesh.glyph(scale="radius", geom=geom,) # progress_bar=True)
            args1 = {
                'mesh': glyphed,
                'scalars': np.repeat(colors1, 50),
                'cmap': cmap,
                'clim': [0.0 if single_noise_color else min(colors1),max(colors1.max(),1.0)] if custom_clim is None else custom_clim,
                'below_color': pv.Color("gray", opacity=1.0) if single_noise_color else None,
                'opacity': np.repeat(opacity, 50),
                **kwargs
            }
            args2 = {
                'mesh': glyphed,
                'opacity': np.repeat(opacity, 50),
                **kwargs
            }
            if('color' in kwargs):
                plotter.add_mesh(**args2)
            else:
                plotter.add_mesh(**args1)
        else:
            args1 = {
                'points': points1,
                'scalars': colors1,
                'cmap': cmap,
                'clim': [0.0 if single_noise_color else min(colors1),max(colors1.max(),1.0)] if custom_clim is None else custom_clim,
                'below_color': pv.Color("gray", opacity=1.0) if single_noise_color else None,
                'render_points_as_spheres': True,
                'opacity': opacity,
                **kwargs
            }
            args2 = {
                'points': points1,
                'render_points_as_spheres': True,
                'opacity': opacity,
                **kwargs
            }
            if('color' in kwargs):
                plotter.add_points(**args2)
            else:
                plotter.add_points(**args1)
    
    return plotter

def plot3DMapAsPoints(m, threshold=0.5, scalar=0, plotter=None):
    '''
    Uses a pyvista.Plotter object to plot the centers of voxels with value above the threshold, then returns the plotter

    Arguments:
    * m: Map object to plot
    * threshold: density threshold used to define the contours of the map
    * scalar: scalar assigned to the object. This allows to color different objects with different colors, according to cmap 'viridis'
    * plotter: pyvista.Plotter object to use for plotting. If None a new one will be creted and returned

    Return:
    * plotter: pyvista.Plotter object on which the object was plotted
    '''
    ps = getPointsFromMap(m, threshold)
    plotter = pv.Plotter() if plotter is None else plotter
    plotter.add_points(ps, scalars=np.ones(len(ps))*scalar)
    return plotter

def plot3DMapMarchingCubes(m, threshold=0.5, scalar=0, smooth_shading=True, cmap='viridis', plotter=None, **kwargs):
    '''
    Uses a pyvista.Plotter object to plot the polygon obtained from m via marching cubes, then returns the plotter

    Arguments:
    * m: Map object to plot
    * threshold: density threshold used to define the contours of the map
    * scalar: scalar assigned to the object. This allows to color different objects with different colors, according to the specified cmap
    * smooth_shading: whether to smooth the surface of the shown object
    * cmap: the colormap used to color the Map
    * plotter: pyvista.Plotter object to use for plotting. If None a new one will be creted and returned

    Return:
    * plotter: pyvista.Plotter object on which the object was plotted
    '''
    mapobj2 = m

    if(plotter is None):
        plotter = pv.Plotter()
    grid = pv.ImageData(dimensions=(mapobj2.box_size()[::-1]))
    grid.spacing = (mapobj2.apix,mapobj2.apix,mapobj2.apix)
    grid.origin=mapobj2.origin+np.array([mapobj2.apix/2.0]*3)

    values = mapobj2.fullMap.flatten()
    conts = grid.contour([threshold], values, method='marching_cubes')
    if(type(cmap)==str):
        cmap = plt.get_cmap(cmap)
    plotter.add_mesh(conts, smooth_shading=smooth_shading, cmap=cmap, scalars=np.ones(conts.n_faces)*scalar, **kwargs)
    # plotter.add_mesh(conts, smooth_shading=smooth_shading, **kwargs)

    return plotter

def plot3DMultipleMapsMarchingCubes(ms, threshold=0.5, scalars=None, smooth_shading=True, cmap='viridis', plotter=None, labels=None, labels_font=20):
    '''
    Uses a pyvista.Plotter object to plot the polygon obtained from m via marching cubes, then returns the plotter

    Arguments:
    * m: Map object to plot
    * threshold: density threshold used to define the contours of the map
    * scalar: scalar assigned to the object. This allows to color different objects with different colors, according to cmap 'viridis'
    * smooth_shading: whether to smooth the surface of the shown object
    * plotter: pyvista.Plotter object to use for plotting. If None a new one will be creted and returned

    Return:
    * plotter: pyvista.Plotter object on which the object was plotted
    '''
    if(scalars is None):
        scalars = [0.0]*len(ms)
    assert len(ms)==len(scalars)
    if(plotter is None):
        plotter = pv.Plotter()
    for m, s in zip(ms, scalars):
        _ = plot3DMapMarchingCubes(m, threshold=threshold, scalar=s, smooth_shading=smooth_shading, cmap=cmap, plotter=plotter)
    if(not labels is None):
        centers = np.array([getPointsFromMap(m, threshold=threshold).mean(axis=0) for m in ms])
        plotter.add_point_labels(centers, labels, font_size=labels_font)
    return plotter

def plot3DConvexHull(seg, scalar=0, smooth_shading=True, plotter=None):
    '''
    Uses a pyvista.Plotter object to plot the polygon obtained from seg via conveh hull, then returns the plotter

    Arguments:
    * seg: SegmentXYZ object to plot
    * scalar: scalar assigned to the object. This allows to color different objects with different colors, according to cmap 'viridis'
    * smooth_shading: whether to smooth the surface of the shown object
    * plotter: pyvista.Plotter object to use for plotting. If None a new one will be creted and returned

    Return:
    * plotter: pyvista.Plotter object on which the object was plotted
    '''
    if(plotter is None):
        plotter = pv.Plotter() if plotter is None else plotter
    coords = seg.Getcoord()
    hull = ConvexHull(coords)
    faces = np.column_stack((3*np.ones((len(hull.simplices), 1), dtype='int'), hull.simplices)).flatten()
    poly = pv.PolyData(hull.points, faces)
    plotter.add_mesh(poly, smooth_shading=smooth_shading, cmap='viridis', scalars=np.ones(poly.n_faces)*scalar)

    return plotter

def plot3DMapAsCubes(m, threshold=0.5, scalar=0, resolution_multiplier=0.5, plotter=None, color=None):
    '''
    Uses a pyvista.Plotter object to plot the set of voxels with value above threshold as cubes, then returns the plotter

    Arguments:
    * m: Map object to plot
    * threshold: density threshold used to define the contours of the map
    * scalar: scalar assigned to the object. This allows to color different objects with different colors, according to cmap 'viridis'
    * resolution_multiplier: multiplied by map resolution to define the side of the cubes. Values smaller than 1 make the object partially transparent allowing the user to see its inside volume
    * plotter: pyvista.Plotter object to use for plotting. If None a new one will be creted and returned

    Return:
    * plotter: pyvista.Plotter object on which the object was plotted
    '''
    assert resolution_multiplier >0.0 and resolution_multiplier <=1.0
    coords = getPointsFromMap(m, threshold)
    mesh = pv.PolyData(coords)
    geom = pv.Cube(x_length=m.apix*resolution_multiplier, y_length=m.apix*resolution_multiplier, z_length=m.apix*resolution_multiplier)
    glyphs = mesh.glyph(factor=1, geom=geom)
    pl = pv.Plotter() if plotter is None else plotter
    if(color is None):
        pl.add_mesh(glyphs, smooth_shading=False, cmap='viridis', scalars=np.repeat(m.fullMap.flatten()[m.fullMap.flatten()>threshold], 8))
    else:
        pl.add_mesh(glyphs, smooth_shading=False, color=color)
    return pl

def getCoM(points):
    '''
    Returns the center of mass of the points
    '''
    return points.mean(axis=0)

def getCustomColormap():
    '''
    Return a colormap based on gist_ncar from which the upper 5% has been removed
    '''
    interval = np.linspace(0, 0.95)
    colors = plt.cm.gist_ncar(interval)
    cmap = LinearSegmentedColormap.from_list('name', colors)
    return cmap

def addLabelsOnPlot(ax, xs,ys,names):
    for x,y,n in zip(xs,ys,names):
        ax.annotate(n, (x, y))


def plotDecodingWithSpecifiedColors(decoding_seg, def_df, plotter=None, cmap='bwr'):
    '''
    Displays localizations colored according to the value present in the column 'value' of def_df. Plots in 3D using pyvista

    
    Arguments:
    * decoding_seg: Segment containing x,y,z and clusterID columns. Each cluster should represent a genomic region
    * def_df: a DataFrame with columns name and value.
        name should contain strings composed as m%i where %i is one the clusterIDs of decoding_seg
        value should be a float in the range [0.0, 1.0] representing the value to use to color that genomic region
    * plotter: if provided the output is plotted on it
    * cmap: which colormap to use for the coloring, default is 'bwr'
    
    
    Returns:
    * plotter
    
    '''
    plotter = pv.Plotter() if plotter is None else plotter
    for lid, clus in decoding_seg.split_into_Clusters().items():
        bperc = def_df.loc[def_df['name']=='m'+str(lid), 'value'].values[0]
        _ = plotClustering3D(clus.Getcoord(),
                             true_labels=np.full(len(clus), bperc),
                             custom_clim=[0.0, 1.0],
                             cmap=cmap,
                             plotter=plotter)
    
    return plotter

def plotDecodingTrace(decoding_seg, labels_col='locusID', plotter=None, show_labels=False):
    '''
    Plots a segmented line connecting the centers of mass of the decoded loci. Plots in 3D using pyvista
    

    Arguments:
    * decoding_seg: Segment containing x,y,z and clusterID columns. Each cluster should represent a genomic region
    * plotter: if provided the output is plotted on it
    * show_labels: whether to should labels on clusters' coms

    
    Returns:
    * plotter
    '''
    centers0 = decoding_seg.atomList[['x','y','z',labels_col]].groupby(labels_col).mean()[['x','y','z']].values
    cs0 = decoding_seg.atomList[labels_col].unique()
    plotter = pv.Plotter() if plotter is None else plotter
    plotter.add_lines(centers0, color='black', connected=True)
    plotter.add_points(centers0, scalars=cs0, render_points_as_spheres=True, point_size=20, cmap='bwr')
    if(show_labels):
        plotter.add_point_labels(centers0, cs0, font_size=20)
    return plotter