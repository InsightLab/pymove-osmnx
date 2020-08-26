# PyMove OSM NetworkX (OSMncx)

## What is PyMove and OSMnx

PyMove is a Python library for processing and visualization of trajectories and other spatial-temporal data. OSMnx is a Python package to retrieve, model, analyze, and visualize street networks from OpenStreetMap. Users can download and model walkable, drivable, or bikeable urban networks with a single line of Python code, and then easily analyze and visualize them.

---

## Main Features

PyMove-OSMnx **proposes**:

-   A familiar and similar syntax to Pandas;
-   Clear documentation;
-   Extensibility, since you can implement your main data structure by manipulating other data structures such as Dask DataFrame, numpy arrays, etc., in addition to adding new modules;
-   Flexibility, as the user can switch between different data structures;
-   Fast map-matching of points, routes, or trajectories to nearest graph edges or nodes;
-   Operations for data preprocessing, pattern mining and data visualization.

---

## Creating a Virtual Environment

It is recommended to create a virtual environment to use pymove-osmnx. Requirements: Anaconda Python distribution installed and accessible

1.  In the terminal client enter the following where `yourenvname` is the name you want to call your environment, and replace `x.x` with the Python version you wish to use. (To see a list of available python versions first, type conda search "^python$" and press enter.)
    -   `conda create -n <yourenvname> python=x.x`
    -   Press y to proceed. This will install the Python version and all the associated anaconda packaged libraries at `path_to_your_anaconda_location/anaconda/envs/yourenvname`

2.  Activate your virtual environment. To activate or switch into your virtual environment, simply type the following where yourenvname is the name you gave to your environment at creation.
    -   `conda activate <yourenvname>`

3.  Now install the package from either `conda`

---

## [Conda](https://anaconda.org/conda-forge/pymove-osmnx) instalation

1.  `conda install -c conda-forge pymove`
