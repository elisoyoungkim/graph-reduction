from collections import defaultdict
from itertools import takewhile, count
from itertools import groupby
from operator import itemgetter

global cyclic_node_set, start, end
cyclic_node_set = []
start_in_SCCs = False

def notification(combinee, combiner):
    print 'Start node \'{0}\' and end node \'{1}\' are SCCs with a combined node \'{1}\'.'.format(combinee, combiner)
    
def detect_cycle(path):
    set_of_cyclic_paths = []
    for vertex in set(path):
        if path.count(vertex) >= 2: # detect cycle form (i, .., i)
            cycle = []
            unseen = True
            for node in path:
                if node == vertex:
                    cycle.append(node)
                    if unseen:
                        unseen = False
                    else:
                        set_of_cyclic_paths.append(tuple(cycle)[cycle.index(node):]) 
                        break
                else:
                    cycle.append(node)
    cyclic_paths_list = []
    [cyclic_paths_list.append(cycle) for cycle in set_of_cyclic_paths if set(cycle) not in cyclic_paths_list]
    #print('clc', cyclic_paths_list)
    return cyclic_paths_list

def start_end_in_SCCs(start, end):
    if start_in_SCCs is True:
        notification(start, end)
        start = end
    return start, end

# def sort_cycle(all_paths, start, end):
#     if len(all_paths) == 0:
#         return []
#     sorted_cycle = []
#     # make a list of cycle paths
#     [sorted_cycle.extend(detect_cycle(path)) for path in all_paths if detect_cycle(path) not in sorted_cycle]
#     sorted_cycle_list = list(set(sorted_cycle))
#     sorted_cycle_list.sort(key=len) # sort the list in an ascending order of the length
#       
#     cyclicPaths_list = []
#     processing_duplicates = []
#     # eliminate duplicates in cyclicPaths list
#     [processing_duplicates.append(list(set(cycle))) for cycle in sorted_cycle_list if list(set(cycle)) not in processing_duplicates]
#       
#     for cycle in sorted_cycle_list:
#         if list(set(cycle)) in processing_duplicates:
#             cyclicPaths_list.append(cycle)
#             del processing_duplicates[processing_duplicates.index(list(set(cycle)))]
#     print 'm', cyclicPaths_list
#     return reshape_cycles(cyclicPaths_list, start, end)
 
def sort_cycle(all_paths, start, end):
    if len(all_paths) is 0:
        return []
    # make a list of cycle paths
    cycles = {tuple(set(cycle)):cycle for path in all_paths for cycle in detect_cycle(path)}    
    cycle_list = map(lambda x:list(x), cycles.values())
    cycle_list.sort(key=len) # sort the list in an ascending order of the length
    return reshape_cycles(cycle_list, start, end)


def reshape_cycles(paths, start, end):
    # paths = all the elementary cycles in a graph
    reshaping_cycles = {}
    elementary_cycle_paths = []
    if len(paths) is 0:
        return elementary_cycle_paths   
    [reshaping_cycles.setdefault(node, []) for node in list(set(reduce(lambda x,y:x+y, paths)))]
    for cycle in paths:
        #print paths
        if start in cycle or end in cycle:
            if start in cycle and end in cycle:
                reshaping_cycles[end].append(cycle)
                global start_in_SCCs
                start_in_SCCs = True
            elif start in cycle:
                reshaping_cycles[start].append(cycle)
            else:
                reshaping_cycles[end].append(cycle)
        else:
            reshaping_cycles[cycle[0]].append(list(cycle))
    for key in reshaping_cycles:
        for value in reshaping_cycles[key]:
            if key is not list(value)[0]:
                reshaped = list(value)[list(value).index(key):]+list(value)[1:list(value).index(key)]
                reshaped.extend([key])
                reshaping_cycles[key][reshaping_cycles[key].index((value))] = reshaped
            else:
                continue
#     if start or end in reshaping_cycles.keys():
#         if end in reshaping_cycles.keys():
#             temporary_list = [walk for walk in reshaping_cycles.get(end)]
#         else:
#             temporary_list = [walk for walk in reshaping_cycles.get(start)]
#         elementary_cycle_paths.extend(temporary_list)    
#     reshaping_cycles.pop(start, None)
#     reshaping_cycles.pop(end, None)
    for value in reshaping_cycles.values():
        if len(value) is not 0:
            temporary_list = [walk for walk in value]
            elementary_cycle_paths.extend(temporary_list)
    return elementary_cycle_paths

def reduction_rules(rule, alpha, beta=0, mode=0, quantiles=0): # reduction rules: 1.chain 2.choice 3.cycle 4.complex
    if rule == 1:
        return alpha*beta
    elif rule == 2:
        if mode == 1:
            return max(alpha, beta)
        else:
            return round(alpha+beta-alpha*beta, 5)
    elif rule == 3:
        if alpha == 1:
            return 1
        else:
            return round(pow(alpha, int(1/(1-alpha))), 5)
    elif rule == 4:
        if alpha == 1:
            return 1
        else:
            return round((1-pow((1-alpha), quantiles))/quantiles, 5)
            #return round(alpha/(alpha*alpha - alpha  + 1), 5)

def calculate_probability(edge_x, edge_y, mode=0, prob_table={}, cycle=0):
    # edge_x = [i,k] edge_y = [k,j]
    #print '\n', edge_x, edge_y
    def glue(edge):
        return reduce(lambda x,y:x+y, edge)
    print glue(edge_x),'\' :',prob_table[glue(edge_x)], glue(edge_y),'\' :', prob_table[glue(edge_y)]

    if edge_x[0]+edge_y[1] not in prob_table:
        print 'Not in', edge_x[0]+edge_y[1]
        if cycle is 0:
            print glue(edge_x), glue(edge_y)
            result = reduction_rules(1, prob_table[glue(edge_x)], prob_table[glue(edge_y)])
        else:
            result = reduction_rules(1, prob_table[glue(edge_x)]*prob_table[edge_x[1]+edge_y[0]], prob_table[glue(edge_y)])
    else:
        print 'Yes in', prob_table[edge_x[0]+edge_y[1]]
        if cycle is 0:
            result = reduction_rules(2, prob_table[glue(edge_x)]*prob_table[glue(edge_y)], prob_table[edge_x[0]+edge_y[1]], mode)
        else:
            result = reduction_rules(2, prob_table[glue(edge_x)]*prob_table[edge_x[1]+edge_y[0]]*prob_table[glue(edge_y)], prob_table[edge_x[0]+edge_y[1]], mode)
    prob_table.update({edge_x[0]+edge_y[1]:result})
    print 'Probability of \"{0}{1}\" is updated as w({0},{1}): {2}.'.format(edge_x[0], edge_y[1], result)
    return result

def fuse_cycle(path, graph, start, end, mode, prob_table):
    if len(path) == 0:
        return graph
    def groupby_in_path(walk, paths):
        empty_nodes_in_cycle_path = []
        while len(walk) > 2: # delete intermediate nodes in a cycle: (i, .., i) becomes (i, i), which is length of cycle is 2
            for node in walk:
                if node in empty_nodes_in_cycle_path:
                    del walk[walk.index(node)]
            try:
                print 'WALK = ',walk
                print '\n00',walk[0], walk[1]
                updated_prob = calculate_probability([walk[0],walk[1]], [walk[1],walk[2]], mode, prob_table)
                prob_table.update({walk[0]+walk[2]:updated_prob})
                
                #print 'Probability of {0}{1} is updated as w({0},{1}): {2}'.format(walk[0], walk[2], updated_prob)
                empty_nodes_in_cycle_path.append(walk[1])
                
            except IndexError:
                pass  
        print '''Nodes {0} are same SCCs meaning \'indistinguishable\' and combined as a solid representative node \'{1}\' \n'''.format(empty_nodes_in_cycle_path, walk[0])
        prob_table.update({walk[0]+walk[1]:reduction_rules(3, prob_table[walk[0]+walk[1]])})
        print 'Probability of \"{0}{1}\" is updated as w({0},{1}): {2}.'.format(walk[0], walk[1], prob_table[walk[0]+walk[1]])
        if walk[0] not in cyclic_node_set:
            cyclic_node_set.append(walk[0])
        #print 'updated', walk[0]+walk[1]
        for each_cycle in paths:
            vertex_index = 0
            for vertex in each_cycle:
                if vertex in empty_nodes_in_cycle_path:
                    del each_cycle[vertex_index]
                    each_cycle.insert(vertex_index, walk[0]) 
                vertex_index += 1
        fusing = []
        eliminate_duplicates = []
        #print 'p', paths
        fused = True
        for each_cycle in paths:            
            fusing = map(itemgetter(0), groupby(each_cycle))
            while fused:
                if start in fusing and end in fusing:
                    if end in fusing[1:-1]:
                        notification(start, end)
                        global start_in_SCCs
                        start_in_SCCs = True
                        fusing = fusing[fusing.index(end):] + fusing[1:fusing.index(end)]
                        fusing.extend(end)
                fused = False
            if len(fusing) > 2 and each_cycle not in eliminate_duplicates:
                eliminate_duplicates.append(fusing)

        paths = eliminate_duplicates  

        # 1.replace a set of empty nodes in a cycle path with a single sold node 
        # 2.update probabilities in prob_table
        combined_node= walk[0]
        #print '!!!!!!!', graph
        #print 'Empty nodes{0}'.format(empty_nodes_in_cycle_path)
        for key in graph.keys(): # walk[0] is a combined solid node
            graph.setdefault(key, [])
            # case 1: key in graph dictionary is in a empty set of nodes
            if key in empty_nodes_in_cycle_path:
                for successor in graph[key]:
                    #and successor not in graph[combined_node]
                    #if successor not in empty_nodes_in_cycle_path and successor != combined_node:
                    if successor not in empty_nodes_in_cycle_path and successor != combined_node:
                        graph[combined_node].append(successor)
                        if combined_node+successor in prob_table:
                            prob_table.update({combined_node+successor:reduction_rules(2, prob_table[combined_node+successor], prob_table[key+successor], mode)})
                            #print 'Graph {0}:'.format(graph)
                            print 'Probability of \"{0}{1}\" is updated as w({0},{1}): {2}.'.format(combined_node, successor, prob_table[combined_node+successor])
                        else:
                            prob_table.update({combined_node+successor:prob_table[key+successor]}) 
                            #print 'Graph {0}:'.format(graph)
                            print 'Probability of \"{2}{3}\" is updated as w({2},{3}): {4} from edge {0}{1}.'.format(key, successor, combined_node, successor, prob_table[combined_node+successor])
                    else:
                        if successor is key:
                            prob_table.update({combined_node+combined_node:reduction_rules(2, prob_table[combined_node+combined_node], prob_table[key+key], mode)})
                            #print 'Graph {0}:'.format(graph)
                            print 'Probability of \"{2}{3}\" is updated as w({2},{3}): {4} from edge {0}{1}.'.format(key,key, combined_node,combined_node, prob_table[combined_node+combined_node])
                            graph[combined_node].append(combined_node)
                        else:
                            graph[combined_node].append(combined_node)
                combined_succ = []
                [combined_succ.append(node) for node in graph.get(combined_node) if node not in combined_succ]
                graph.update({combined_node:combined_succ})
                #graph.update({combined_node:list(set(graph.get(combined_node)))})
                del graph[key]
                
                #print '**************',graph
            # case 2: key in graph dictionary is a combined solid node
            
            elif key == combined_node:
                #print '====', graph
                for node in empty_nodes_in_cycle_path:
                    if node in graph[key]:
                        graph[key].remove(node)
                        graph[key].append(combined_node)
                         
#                 try:
#                     graph[key].remove(combined_node)
#                 except ValueError:
#                     pass
                #print '$$$$$$$$$$$$$$$', graph.get(combined_node) 
                #print graph
                combined_succ = []
                [combined_succ.append(node) for node in graph.get(combined_node) if node not in combined_succ]
                graph.update({combined_node:combined_succ})
                #print '@@@@@@@@@@@@@@@@'
                #print graph
                #graph.update({combined_node:list(set(graph.get(combined_node)))})
                #updated_adj = []
#                 for vertex in graph[key]:
#                     if vertex not in empty_nodes_in_cycle_path:
#                         updated_adj.append(vertex)
#                 graph.update({combined_node:updated_adj})
#                 print('Graph {0}:'.format(graph))
            # case 3: key in graph dictionary is neither a combined solid node nor a empty node
            elif key not in empty_nodes_in_cycle_path and key != combined_node:
                deletion = []
                addition = []
                for successor in graph[key]:
                    if successor in empty_nodes_in_cycle_path:
                        deletion.append(successor)
                        addition.append(combined_node)
                        #print 'Graph {0}:'.format(graph)
                        if key+combined_node in prob_table:
                            prob_table.update({key+combined_node:reduction_rules(2, prob_table[key+combined_node], prob_table[key+successor], mode)})
                            #print 'Graph {0}:'.format(graph) 
                            print 'Probability of \"{0}{1}\" is updated as w({0},{1}): {2}.'.format(key, combined_node, prob_table[key+combined_node])
                        else:
                            prob_table.update({key+combined_node:prob_table[key+successor]})
                            #print 'Graph {0}:'.format(graph)
                            print 'Probability of \"{2}{3}\" is updated as w({2},{3}): {4} from edge {0}{1}.'.format(key,successor, key,combined_node, prob_table[key+combined_node])
                [graph[key].remove(succ) for succ in deletion if succ in graph[key]]
                [graph[key].append(succ) for succ in addition]
                
#                 combined_succ = []
#                 [combined_succ.append(node) for node in graph.get(combined_node) if node not in combined_succ]
#                 graph.update({key:combined_succ})
                graph.update({key:list(set(graph.get(key)))})
        #print 'Paths', paths
        return paths
    def updated_paths(paths):
        
        while len(paths) is not 0:
            print 'PATHS ==== ',paths
            changed = []
            paths = groupby_in_path(paths[0], paths)
            for path in paths:
                if start in path and end in path:
                    if end != path[0]:
                        #print('path:', path)
                        reshaped = reshape(end, path)
                        changed.append(reshaped)
                        #print(changed)
                        #print(reshaped)
#                         if start+start in prob_table:
#                             prob_table.update({end+end:prob_table[start+start]})
#                             print('The probability of cycle edge {0}{0} is updated: {1} \n\n'.format(end, prob_table[end+end]))
#                         
                    else:
#                         if start+start in prob_table:
#                             prob_table.update({end+end:prob_table[start+start]})
#                             print('The probability of cycle edge {0}{0} is updated: {1} \n\n'.format(end, prob_table[end+end]))
                        changed.append(path)
                    
                elif start in path or end in path:
                    if start in path and start != path[0]:
                        reshaped = reshape(start, path)
                        changed.append(reshaped)
                        
                    elif end in path and end != path[0]:
                        reshaped = reshape(end, path)
                        changed.append(reshaped)
                    else:
                        changed.append(path)
                    
                else:
                    changed.append(path)
            paths = changed
            slicing = []
            for path in paths:
                count = path.count(path[0])
                if count > 2:
                    idx = []
                    [idx.append(x[0]) for x in list(enumerate(path)) if path[0] in x]
                    #[idx.extend([x[0]]) for x in list(enumerate(path)) if path[0] in x]
                    print('index', idx)
                    for n in [[idx[y],idx[y+1]] for y in range(len(idx)-1)]:
                        print('n{0}'.format(n))
                        temp = path[n[0]:n[1]]
                        print('temp{0}'.format(temp))
                        temp.extend([path[0]])
                        slicing.append(temp)
                        print('slicing', slicing)
                        
                else:
                    slicing.append(path)
                print('slicing', slicing)
            paths = []
            [paths.append(path) for path in slicing if path not in paths]
            print(paths)
            paths = slicing
            
            print(slicing)
            print('paths {0}'.format(paths))   
  
                    
        return paths
    updated_paths(path)
    #print(graph)
    #print 'cnodeset',cyclic_node_set
    for cycle_vertex in cyclic_node_set:
        if cycle_vertex in graph.keys() and cycle_vertex in graph[cycle_vertex]:
            graph[cycle_vertex].remove(cycle_vertex)
            #print graph
    #[graph[cycle_vertex[0]].remove(cycle_vertex[0]) for cycle_vertex in cyclic_node_set if cycle_vertex[0] in graph.keys() and cycle_vertex[0] in graph[cycle_vertex[0]]]

    return graph

def reshape(vertex, path):
    reshaped = path[path.index(vertex,0):]+path[1:path.index(vertex,0)]
    reshaped.append(vertex)
    return reshaped

def sort_topologically_stackless(graph):
    depths_by_node = {}
    nodes_by_depth = defaultdict(set)

    def add_depth_to_node(node, depth):
        depths_by_node[node] = depth
        nodes_by_depth[depth].add(node)

    def walk_depth_first(node):
        stack = [node]
        while(stack):
            node = stack.pop()
            if node in depths_by_node:
                continue
            if node not in graph or not graph[node]:
                depth = 0
                add_depth_to_node(node, depth)
                continue
            children = graph[node]
            children_not_calculated = [child for child in children if child not in depths_by_node]
            if children_not_calculated:
                stack.append(node)
                stack.extend(children_not_calculated)
                continue
            depth = 1 + max(depths_by_node[lnode] for lnode in children)
            add_depth_to_node(node, depth)
    [walk_depth_first(node) for node in graph]

    return list(takewhile(lambda x: x is not None, (nodes_by_depth.get(i, None) for i in count())))
