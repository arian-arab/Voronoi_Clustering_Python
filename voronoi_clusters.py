import numpy as np
from scipy.spatial import Voronoi
from scipy.spatial import Delaunay
from itertools import compress
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from matplotlib import cm
import math

number_of_points = 500
area_threshold = 40
min_number_of_localizations = 5
points = np.random.random([number_of_points,2])

def delauny_vertex_attachments(points):  
    dt = Delaunay(points)
    vertices = dt.vertices
    vertices_hstack = np.hstack(vertices)
    vertices_hstack_sorted = np.argsort(vertices_hstack)    
    idx = []
    vertices_sorted = []
    for i in vertices_hstack_sorted:
        idx.append(vertices[divmod(i,3)[0],divmod(i,3)[1]])
        vertices_sorted.append(vertices[divmod(i,3)[0],:])

    u, indices = np.unique(idx , return_index=True)
    neighbors = []
    for i in range(len(u)):
        if i<len(u)-1:
            neighbors.append(vertices_sorted[indices[i]:indices[i+1]])
        else:
            neighbors.append(vertices_sorted[indices[i]:len(vertices_sorted)+1])    
    neighbors = [np.unique(np.concatenate(i)) for i in neighbors]
    neighbors = [list(i) for i in neighbors]
    [i.remove(counter) for counter,i in enumerate(neighbors)]    
    return neighbors

def get_voronoi(points):
    vor = Voronoi(points)
    point_to_cell_index = list(vor.point_region)
    max_bound = vor.max_bound
    min_bound = vor.min_bound 
    regions = vor.regions
    infinity_index = [regions.index(i) for i in regions if -1 in i]
    vertices = vor.vertices
    voronoi_cells = []
    for i in regions:
        if len(i) != 0:
            voronoi_cells.append(vertices[i])
        else:
            voronoi_cells.append([])
    voronoi_cells_corr = []
    for i in voronoi_cells:
        if len(i) != 0:
            voronoi_cells_corr.append(np.vstack((i[1:,:],i[0,:])))
        else:
            voronoi_cells_corr.append([])
    voronoi_areas = []
    for i,j in zip(voronoi_cells, voronoi_cells_corr):
        if len(i) != 0:
            voronoi_areas.append(np.abs(np.sum(np.multiply((j[:,0]-i[:,0]),(j[:,1]+i[:,1])))*0.5))
        else:
            voronoi_areas.append(math.inf)
    for i in infinity_index:
        voronoi_areas[i] = math.inf
    return voronoi_cells, voronoi_areas, point_to_cell_index, min_bound, max_bound

def plot_voronoi(points,voronoi_cells,voronoi_areas,min_bound,max_bound):
    fig, ax = plt.subplots()
    patches = []
    for counter,i in enumerate(voronoi_cells):
        if voronoi_areas[counter] != math.inf:            
            plt.text(np.mean(i[:,0]),np.mean(i[:,1]),counter,color = 'r')
            patches.append(Polygon(i))            
    collection = PatchCollection(patches, alpha = 0.1, edgecolor = 'r', cmap=cm.hot)     
    collection.set_array(np.array((voronoi_areas)))
    ax.add_collection(collection)
    fig.colorbar(collection, ax=ax)
    plt.scatter(points[:,0], points[:,1], s=1, color = 'b')
    plt.show()
    plt.xlim(min_bound[0],max_bound[0])
    plt.ylim(min_bound[1],max_bound[1])
    
def find_clusters(keep_points,neighbors):
    used_points = [False]*len(keep_points)
    clusters = []
    for i in range(len(keep_points)):
        if keep_points[i] and not used_points[i]:
            seed = []
            idx = []
            seed = list(compress(neighbors[i],[keep_points[j] for j in neighbors[i]]))
            if seed:
                while True:
                    size_one = len(seed)
                    idx = list(np.unique(np.concatenate([neighbors[i] for i in seed])))
                    idx = list(compress(idx,[keep_points[j] for j in idx]))
                    seed  = list(np.unique(np.asarray(seed+idx)))
                    size_two = len(seed)
                    if size_one==size_two:
                        break
            else:
                seed = [i]
            for j in seed:
                used_points[j] = True
            clusters.append(seed)
    return clusters
   
def find_correct_neighbors(neighbors,point_to_cell_index):
    neighbors_corrected = []
    for i in neighbors:
        neighbors_corrected.append([point_to_cell_index[k] for k in i])
    final = [0]*(len(neighbors)+1)
    for i in range(len(neighbors)):
        final[point_to_cell_index[i]] = neighbors_corrected[i]
    return final    

def plot_clusters(clusters_voronoi_cells,clusters_voronoi_areas):
    fig, ax = plt.subplots()
    patches = []
    color = []
    for counter,i in enumerate(clusters_voronoi_cells):
        color.append([counter]*len(i))
        for j in i:
            patches.append(Polygon(j))
    color = np.asarray([np.asarray(i) for i in color])
    color = np.hstack(color)
    collection = PatchCollection(patches, alpha = 1, edgecolor = 'b', cmap=cm.hot)
    collection.set_array(color)
    # collection.set_clim(cmin, cmax)
    ax.add_collection(collection)
    fig.colorbar(collection, ax=ax)
    plt.show()
    plt.xlim(min_bound[0],max_bound[0])
    plt.ylim(min_bound[1],max_bound[1])  

[voronoi_cells, voronoi_areas, point_to_cell_index, min_bound, max_bound] = get_voronoi(points)
neighbors = delauny_vertex_attachments(points)
# plot_voronoi(points,voronoi_cells,voronoi_areas,min_bound,max_bound)
neighbors = find_correct_neighbors(neighbors,point_to_cell_index)
area_threshold = np.percentile(voronoi_areas,area_threshold)    
keep_points = [True if i<=area_threshold else False for i in voronoi_areas]
clusters = find_clusters(keep_points,neighbors)
clusters = list(filter(lambda x: len(x)>=5,clusters))

clusters_voronoi_cells = [[voronoi_cells[k] for k in i] for i in clusters]
clusters_voronoi_areas = [[voronoi_areas[k] for k in i] for i in clusters]
plot_clusters(clusters_voronoi_cells,clusters_voronoi_areas)