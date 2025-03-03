# Voronoi_Clustering_Python

This code generates clusters of point-pattern data using Voronoi tesselations in super-resolution muicroscopy. The code follows descriptions provided in: https://www.nature.com/articles/srep24084

Run the python code "voronoi_clustering.py" as an example of the method described above.

1) The first line generates random scattered points in 2-D: 
points = np.random.random([number_of_points,2]); where number_of_points is selected as an example to be 1000 points.

2) The second line generates the voronoi tesselations by calculating each voronoi cell coordinates along with each voronoi cell area
voronoi_areas, voronoi_cells =  find_voronoi(points)  

3) The third line calculates the area_threshold based on the area of all individual voronoi cells (for this example area_threshold = 40th percentile, i.e., voronoi cells with areas bigger than area_threshold will be discarded from the clustering analysis):
area_threshold = np.percentile(voronoi_areas,area_threshold) 
