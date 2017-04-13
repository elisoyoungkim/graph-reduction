# # '''
# # Created on Jun 4, 2016
  
# # @author: SoyoungKim
# # '''
# import random
# from copy import deepcopy
  
# # # This prints a random floating point number in the range [0, 1) 
# for x in range(10):
#     print x, round(random.random(),2)
  
# if __name__ == '__main__':
#     pass
  
# def parse():
#     graph = {}
#     prob_table = {}
#     edges = []
#     count = 0
#     #with open('cit2(100n).txt') as cgraph:
#     # with open('cit3(500n).txt') as cgraph:
#     with open('HepTH.txt') as cgraph:
#         for line in cgraph:
#             #parse=line.replace('-',' ').replace('_',' ')
#             nodes = line.split()
#             count += 1
#             #print count, nodes
#             edges.append(('p'+nodes[0], 'p'+nodes[1]))
#             if 'p'+nodes[0] in graph:
#                 graph['p'+nodes[0]].append('p'+nodes[1])
#             else:
#                 graph.update({'p'+nodes[0]:['p'+nodes[1]]})
                   
#             if 'p'+nodes[1] not in graph:
#                 graph.setdefault('p'+nodes[1], [])
#             prob_table.update({'p'+nodes[0]+'p'+nodes[1]:round(random.random(),2)})
#     # for node in graph:
#     #     print node, graph[node]
#     #for prob in prob_table:
#         #print prob, prob_table[prob]
#     print len(prob_table)
#     print len(graph)
#     #print graph
#     #print prob_table
#     cgraph.close()
      
#     global_graph = graph.copy()
#     global_prob_table = prob_table.copy()
      
#     return (edges, graph, prob_table)
# # parse()
