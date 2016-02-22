# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import time
import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph3 import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!

## step-1: read in the first 2 values in each line of the file and initialize Nodes for each building
## step2: read in the file again, and construct edges from each line
#
def printPath(path):
    # a path is a list of nodes
    result = ''
    for i in range(len(path)):
        if i == len(path) - 1:
            result = result + str(path[i])
        else:
            result = result + str(path[i]) + '->'
    return result

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print "Loading map from file..."
    infile = open(mapFilename, 'r')
    
    graph = WeightedDigraph()
    
    # add nodes
    for line in infile: # each line in file
        line = line.strip() # strip "\n" from line
        line = line.split(' ')
        node1, node2 = line[0], line[1] # take nodes
        #print node1, node2, type(node1), type(node2)
        try:
            graph.addNode(Node(node1)) # note: add a node, not a string!
        except ValueError as e: #node 1 already exist
            pass
        try: 
            graph.addNode(Node(node2))
        except ValueError as e: # node 2 already exist
            pass

    infile.close()
  
      
    # add edges
    infile = open(mapFilename, 'r')
    for line in infile: # each line in file
        line = line.strip() # strip "\n" from line
        line = line.split(' ')
        node1, node2 = Node(line[0]), Node(line[1]) # take nodes
        totDist, outDist = int(line[2]), int(line[3])
    
        edge = WeightedEdge(node1, node2, totDist, outDist)

        graph.addEdge(edge)
   
    return graph

    
mitMap = load_map("./mit_map.txt")
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def timeit(func):

    def _timeit(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except ValueError:
            raise
        else:
            return result
        finally:
            duration = time.time() - start
            print '{0} ran for: {1:0.5f} secs.'.format(func.__name__, duration)

    return _timeit

def calc_total_distance(path):
    return sum(int(edge.total_distance) for edge in path)


def calc_distance_outdoors(path):
    return sum(int(edge.outdoors_distance) for edge in path)


def is_node_visited(node, path):
    for edge in path:
        if node in (edge.getSource(), edge.getDestination()):
            return True

    return False


def get_node_list(path):
    visited = [str(edge.getSource()) for edge in path]
    visited.append(str(path[-1].getDestination()))
    return visited

@timeit
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDisOutdoors.

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
   
    # get all edges from starting node
    stack = [[edge] for edge in digraph.childrenOf(Node(start))]
    
    valid_paths = []

    # while there are still edges on the stack
    while stack:
        path = stack.pop(-1) #take one path (or edge)

        is_end_reached = path[-1].getDestination().getName() == end # if the edge leads to the end
        
        if is_end_reached and calc_distance_outdoors(path) <= maxDistOutdoors:
            valid_paths.append(path)
            continue

        for edge in digraph.childrenOf(path[-1].getDestination()): # get all the edges going out of the edge(destination node) that we popped off the stack
            if not is_node_visited(edge.getDestination(), path): # if we haven't yet visted the target of the this edge
                new_path = path + [edge]
                # "...consider first finding all valid paths that satisfy
                # the max distance outdoors constraint,..."
                if calc_distance_outdoors(new_path) <= maxDistOutdoors:
                    stack.append(new_path) # at it to the end of the stack to check again if valid

    shortest, min_distance = None, maxTotalDist
    for path in valid_paths:
        # "... and then going through those paths and returning the shortest,
        # rather than trying to fulfill both constraints at once..."
        distance = calc_total_distance(path)
        if distance < min_distance:
            shortest, min_distance = path, distance

    if shortest is None:
        raise ValueError()

    return get_node_list(shortest)
        
        
def timeit(func):

    def _timeit(*args, **kwargs):
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except ValueError:
            raise
        else:
            return result
        finally:
            duration = time.time() - start
            print '{0} ran for: {1:0.5f} secs.'.format(func.__name__, duration)

    return _timeit    

#mitMap = load_map("./mit_map.txt")
#allPaths = getAllPaths(mitMap, Node('32'), Node('8'))
#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
@timeit
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
    not exceed maxDisOutdoors.

    Parameters:
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    stack = [[edge] for edge in digraph.childrenOf(Node(start))]

    while stack:
        path = stack.pop(-1)

        is_end_reached = path[-1].getDestination().getName() == end
        if (is_end_reached and
                calc_distance_outdoors(path) <= maxDistOutdoors and
                calc_total_distance(path) <= maxTotalDist):
            return get_node_list(path)

        for edge in digraph.childrenOf(path[-1].getDestination()):
            if not is_node_visited(edge.getDestination(), path):
                new_path = path + [edge]
                if (calc_distance_outdoors(new_path) <= maxDistOutdoors and
                        calc_total_distance(new_path) <= maxTotalDist):
                    stack.append(new_path)

    raise ValueError()




# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
#     Test cases
     mitMap = load_map("mit_map.txt")
#     print isinstance(mitMap, Digraph)
#     print isinstance(mitMap, WeightedDigraph)
#     print 'nodes', mitMap.nodes
#     print 'edges', mitMap.edges


     LARGE_DIST = 1000000

     #Test case 1
     print "---------------"
     print "Test case 1:"
     print "Find the shortest-path from Building 32 to 56"
     expectedPath1 = ['32', '56']
     brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
     dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
     print "Expected: ", expectedPath1
     print "Brute-force: ", brutePath1
     print "DFS: ", dfsPath1
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
     print "---------------"
     print "Test case 2:"
     print "Find the shortest-path from Building 32 to 56 without going outdoors"
     expectedPath2 = ['32', '36', '26', '16', '56']
     brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
     dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
     print "Expected: ", expectedPath2
     print "Brute-force: ", brutePath2
     print "DFS: ", dfsPath2
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
     print "---------------"
     print "Test case 3:"
     print "Find the shortest-path from Building 2 to 9"
     expectedPath3 = ['2', '3', '7', '9']
     brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
     dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
     print "Expected: ", expectedPath3
     print "Brute-force: ", brutePath3
     print "DFS: ", dfsPath3
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
     print "---------------"
     print "Test case 4:"
     print "Find the shortest-path from Building 2 to 9 without going outdoors"
     expectedPath4 = ['2', '4', '10', '13', '9']
     brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
     dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
     print "Expected: ", expectedPath4
     print "Brute-force: ", brutePath4
     print "DFS: ", dfsPath4
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
     print "---------------"
     print "Test case 5:"
     print "Find the shortest-path from Building 1 to 32"
     expectedPath5 = ['1', '4', '12', '32']
     brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
     dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
     print "Expected: ", expectedPath5    
     print "Brute-force: ", brutePath5
     print "DFS: ", dfsPath5
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
     print "---------------"
     print "Test case 6:"
     print "Find the shortest-path from Building 1 to 32 without going outdoors"
     expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
     brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
     dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
     print "Expected: ", expectedPath6
     print "Brute-force: ", brutePath6
     print "DFS: ", dfsPath6
     print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
     print "---------------"
     print "Test case 7:"
     print "Find the shortest-path from Building 8 to 50 without going outdoors"
     bruteRaisedErr = 'No'
     dfsRaisedErr = 'No'
     try:
         bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
     except ValueError:
         bruteRaisedErr = 'Yes'
    
     try:
         directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
     except ValueError:
         dfsRaisedErr = 'Yes'
    
     print "Expected: No such path! Should throw a value error."
     print "Did brute force search raise an error?", bruteRaisedErr
     print "Did DFS search raise an error?", dfsRaisedErr

     #Test case 8
     print "---------------"
     print "Test case 8:"
     print "Find the shortest-path from Building 10 to 32 without walking"
     print "more than 100 meters in total"
     bruteRaisedErr = 'No'
     dfsRaisedErr = 'No'
     try:
         bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
     except ValueError:
         bruteRaisedErr = 'Yes'
    
     try:
         directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
     except ValueError:
         dfsRaisedErr = 'Yes'
    
     print "Expected: No such path! Should throw a value error."
     print "Did brute force search raise an error?", bruteRaisedErr
     print "Did DFS search raise an error?", dfsRaisedErr
