# Voronoi_Clustering_Python

This code generates clusters of point-pattern data using Voronoi tesselations in super-resolution muicroscopy. The code follows descriptions provided in: https://www.nature.com/articles/srep24084

Run the python code "voronoi_clustering.py" as an example of the method described above.

The first line generates random scattered points in 2-D: 
points = np.random.random([number_of_points,2]); where number_of_points is selected as an example to be 1000 points.

The second line generates the voronoi tesselations by calculating each voronoi cell coordinates along with each voronoi cell area
voronoi_areas, voronoi_cells =  find_voronoi(points)  

The third line calculates the threshold on the area of the voronoi cells based on the area_threshold selected (in this case 40th percentile):
area_threshold = np.percentile(voronoi_areas,area_threshold) 
Any voronoi cell which its area is above the area_thereshold calculated above, will be discarded in the clustering analysis.
