# Visibility Graph
*Project for Computational Geometry course at university*


## Problem
This project implements and visualizes the algorithm that solves following problem:
> Given a set of disjoint simple polygons in the plane find all pairs of points that can 'see' each other.
> Two points 'see' each other if the segment connecting them does not intersect the interior of any polygon.

## Solution
The algorithm for every point *p* (of all points in all polygons) finds all the points *q* that are visible from that point in *O(nlogn)* time. The key is sorting the points by the angle segment [p,q] creates with positive X-axis and using sweeping algorithm to traverse each point q only once. That yields *O(n^2logn)* solution for creating whole graph (n - number of points).
For in-depth analysis see [this book](https://books.google.pl/books/about/Computational_Geometry.html?id=_vAxRFQcNA8C&redir_esc=y).

## App usage
The program is easy and intuitive to use:
* run `main.py`
* either import the set of polygons from `tests/test.json` file by pressing *Import* button or enter them in the app by pressing *Add polygon* button and marking consecutive points on the screen. (__NOTE: the points of each polygon have to be given in counter-clockwise order__)
* When the set of polygons is visible on the screen hit *Run* and then navigate through particular steps of the algorithm using *Next step* and *Previous step* buttons.

## Screenshots
![Algorithm in work](https://github.com/Mozarek/VisibilityGraph/blob/master/presentation/screenshot1.PNG)
![Final results](https://github.com/Mozarek/VisibilityGraph/blob/master/presentation/screenshot2.PNG)
