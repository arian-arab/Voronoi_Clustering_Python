# Voronoi_Clustering_Python

This code generates clusters of point-pattern data using Voronoi tessellations in super-resolution microscopy. It follows the methodology described in this article: https://www.nature.com/articles/srep24084

To see the implementation in action, run the Python script "voronoi_clustering.py", which demonstrates the method.

The key steps are as follows:

**1) Generate Random Points:**
The first line creates a set of randomly scattered points in 2D space:  points = np.random.random([number_of_points,2]).  Here, number_of_points is set to 1000 as an example.

**2) Compute Voronoi Tessellations:**
The second line computes the Voronoi diagram, extracting the coordinates of each Voronoi cell along with their corresponding areas:  voronoi_areas, voronoi_cells =  find_voronoi(points)

![image](https://github.com/user-attachments/assets/23085af4-3654-4ebe-b474-be03a9ba047f)

**3) Determine the Area Threshold:**
The third step defines an area_threshold based on the distribution of Voronoi cell areas. In this example, the threshold is set to the 40th percentile, meaning that Voronoi cells with areas exceeding this value will be excluded from the clustering analysis.

![image](https://github.com/user-attachments/assets/263874ae-2c8a-4b3b-9a43-a63a423349f4)

**4) Cluster Detection:**
The remaining code identifies connected Voronoi cells and filters out clusters containing fewer than min_number_of_localizations cells. In this example, min_number_of_localizations is set to 10, ensuring that clusters with fewer than 10 cells are discarded.

![image](https://github.com/user-attachments/assets/e7923076-b287-49ef-a324-30b01bbc9e99)
