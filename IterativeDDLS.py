class Stack():

    def __init__(self):
        self.stack = []

    def get(self):
        return self.stack.pop(0)

    def put(self, item):
        self.stack.insert(0, item)

    def empty(self):
        return len(self.stack) == 0


def iterative_search(data_structure, graph, start, end, limit=None):
    # initialize generator
    data_structure.put((graph, start, end,[]))

    while not data_structure.empty():
        graph, current, end, path = data_structure.get()

        # make solution depth limited
        # makes it iterative - for DFS to use all paths
        if limit and len(path) > limit:
            continue

        if current == end:
            # route done - yield result
            yield tuple(path + [current])

        if current in graph:
            # skip neighbor-less nodes
            for neighbor in graph[current]:
                # store all neighbors according to data structure
                data_structure.put(
                    (graph, neighbor, end, path + [current])
                )
#     
#     import os
#     
#     
#     # bfs - using queue
#     gen = iterative_search(Queue.Queue(), graph,  start_vertex, end_vertex)
#     print "BFS"
#     # get only 10 first paths
#     bfs_path_set = set()
#     while len(bfs_path_set) < 10:
#         bfs_path_set.add(next(gen))
#     
#     print os.linesep.join(map(str, bfs_path_set))
#     
#     print "Iterative DFS"
#     # dfs  - using stack
#     gen = iterative_search(Stack(), graph, start_vertex, end_vertex, limit=5)
#     
#     # get only 10 first paths
#     dfs_path_set = set()
#     limit = 1
#     while len(dfs_path_set) < 10:
#         try:
#             dfs_path_set.add(next(gen))
#         except StopIteration:
#             limit += 1
#             print "depth limit reached, increasing depth limit to %d" % limit
#             gen = iterative_search(
#                 Stack(), graph, start_vertex, end_vertex, limit=limit
#             )
#     
#     print os.linesep.join(map(str, dfs_path_set))
#     
#     print "difference BFS - DFS: %s" % str(bfs_path_set - dfs_path_set)
#     print "difference DFS - BFS: %s" % str(dfs_path_set - bfs_path_set)              
#     all_paths = list(dfs_path_set.union(bfs_path_set))
#     print 'A set of paths using IDDLS: {0}'.format(all_paths)   
#     print len(all_paths)
#     return all_paths

#graph = {'p9605033': set(['p9612105']), 'p9912204': set(['p9605033']), 'p9612105': set(['p208020']), 'p208020':set(['p9605033'])}

#print list(bfs_paths(graph, 'p9605033', 'p208020'))






# import Queue, os
# 
# class Stack():
# 
#     def __init__(self):
#         self.stack = []
# 
#     def get(self):
#         return self.stack.pop(0)
# 
#     def put(self, item):
#         self.stack.insert(0, item)
# 
#     def empty(self):
#         return len(self.stack) == 0
# 
# 
# def iterative_search(data_structure, graph, start, end, limit=None):
#     # initialize generator
#     data_structure.put((graph, start, end,[]))
# 
#     while not data_structure.empty():
#         graph, current, end, path = data_structure.get()
# 
#         # make solution depth limited
#         # makes it iterative - for DFS to use all paths
#         if limit and len(path) > limit:
#             continue
# 
#         if current == end:
#             # route done - yield result
#             yield tuple(path + [current])
# 
#         if current in graph:
#             # skip neighbor-less nodes
#             for neighbor in graph[current]:
#                 # store all neighbors according to data structure
#                 data_structure.put(
#                     (graph, neighbor, end, path + [current])
#                 )
# 
# gen = iterative_search(Queue.Queue(), graph, start_vertex, end_vertex)
# print "BFS"
# bfs_path_set = set()
# while len(bfs_path_set) < 10:
#     bfs_path_set.add(next(gen))
# print os.linesep.join(map(str, bfs_path_set))
# print "Iterative DFS"
# gen = iterative_search(Stack(), graph, start_vertex, end_vertex, limit=5)
# dfs_path_set = set()
# limit = 1
# while len(dfs_path_set) < 10:
#     try:
#         dfs_path_set.add(next(gen))
#     except StopIteration:
#         limit += 1
#         print "depth limit reached, increasing depth limit to %d" % limit
#         gen = iterative_search(Stack(), graph, start_vertex, end_vertex, limit=limit)
# print os.linesep.join(map(str, dfs_path_set))
# print "difference BFS - DFS: %s" % str(bfs_path_set - dfs_path_set)
# print "difference DFS - BFS: %s" % str(dfs_path_set - bfs_path_set)    
# all_paths = list(dfs_path_set.union(bfs_path_set))
# print 'A set of paths using IDDLS: {0}'.format(all_paths)   
# 
# # 
# 
# class Stack():
# 
#     def __init__(self):
#         self.stack = []
#     def get(self):
#         return self.stack.pop(0)
#     def put(self, item):
#         self.stack.insert(0,item)
#     def empty(self):
#         return len(self.stack) == 0
# 
# def iterative_search(data_structure, graph, start, end, limit=None):
#     # initialize generator
#     print graph, start, end
#     data_structure.put((graph, start, end, []))
#     print data_structure
#     while not data_structure.empty():
#         graph, current, end, path = data_structure.get()
#         print current
#         print path
#         # make solution depth limited
#         # makes it iterative - for DFS to use all paths
#         if limit and len(path) > limit:
#             continue    
#         if current == end:
#             # route done - yield result
#             print 'path',path
#             yield tuple(path+[current])   
#         if current in graph:
#             # skip neighbor-less nodes
#             for neighbor in graph[current]:
#                 # store all neighbors according to data structure
#                 data_structure.put((graph, neighbor, end, path+[current]))