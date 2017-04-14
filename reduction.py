import Queue, os, fuseCycle, IterativeDDLS

def flatten(listinlist):
    out = []
    for item in listinlist:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out
  
def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbor in graph[node]:
            edges.append((node, neighbor))  
    return edges

def transitive_closure(edges):
    closure = set(edges)
    count = 0
    new_path = []
    while True:
        count += 1
        new_path = set((x, w) for x, y in closure for q, w in closure if q == y)
        closure_until_now = closure | new_path
        if closure_until_now == closure:
            break
        closure = closure_until_now
        
    return closure

def generate_relevant_edges(paths):
    edges = []
    for path in paths:
        for index in range(len(path) - 1):
            if (path[index], path[index + 1]) not in edges:
                edges.append((path[index], path[index + 1]))   
    return edges

def vertices(graph):
    nodes = graph.keys()
    successors = reduce(lambda x,y: x+y, graph.values())
    nodes.extend(successors)
    return set(nodes)

def vertex_degree(graph, vertex):
    #adj_dict = reduce(lambda x,y: x+y, graph.values())
    adj_dict = flatten(graph.values())
    degree = len(graph[vertex]) + adj_dict.count(vertex)
    return degree

def find_all_paths_with_IDDLS(fused_graph, start_vertex, end_vertex):
    depth = len(fused_graph.keys())*2
    gen = IterativeDDLS.iterative_search(Queue.Queue(), fused_graph, start_vertex, end_vertex) # bfs - using queue
    bfs_path_set = set()
    while len(bfs_path_set) < depth:
        try:
            bfs_path_set.add(next(gen))
        except:
            break
    os.linesep.join(map(str, bfs_path_set))
    gen = IterativeDDLS.iterative_search(IterativeDDLS.Stack(), fused_graph, start_vertex, end_vertex, limit=depth) # dfs  - using stack 
    dfs_path_set = set()
    while len(dfs_path_set) < depth:
        try:
            dfs_path_set.add(next(gen))
        except StopIteration:
            break
   
    os.linesep.join(map(str, dfs_path_set))
    # get all paths between start and end nodes 
    all_paths_of_fused_graph = []
    for path in list(dfs_path_set.union(bfs_path_set)):
        lpath = list(path)
        all_paths_of_fused_graph.append(lpath)
    return all_paths_of_fused_graph

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def get_elimination_set(graph, start_vertex,end_vertex):
    elimination_set = sorted(list(vertices(graph) - set([start_vertex]) - set([end_vertex])))
    return elimination_set

def reachable(graph,node):
    return reachablity(graph,node,seen = None)

def reachablity(graph,node,seen = None):
    seen = seen or []
    seen.append(node)
    reached = []
    reached.append(node)
    intermediate = graph.get(node)  
    count = 0
    if intermediate:
        count += 1
        reached.extend(intermediate)
        reached = list(set(reached))
        for subnode in intermediate:
            if subnode in intermediate:
                if subnode not in seen:
                    reached.extend(reachablity(graph, subnode, seen))
    return list(set(reached))
def connectivity(graph, start, end, prob_table, R_s, R_t, scc):
    if len(scc) is 0:
        longestscc = 0
    else:
        longestscc = len(reduce(lambda x,y: x+y, scc))
    if end not in R_s:
        return (False, 0, graph)
    else:
        if start == end:
            relevant_nodes = R_s
            anypath = []
            if start+end in prob_table:
                answer= (True, 2*longestscc+len(reduce(lambda x,y: x+y, R_s))+len(reduce(lambda x,y: x+y, R_t)), graph)
            else:
                if start in graph.keys():
                    for source in graph[start]:
                        anypath.extend(find_all_paths(graph, source, end))
                    if len(anypath) != 0:
                        answer = (True, 2*longestscc+len(reduce(lambda x,y: x+y, R_s))+len(reduce(lambda x,y: x+y, R_t)), graph)
                    else:
                        answer = (False, 0, graph)  
                else:
                    answer = (False, 0, graph)
            for component in scc:
                if end in component:
                    [relevant_nodes.append(node) for node in component if node not in relevant_nodes]
            print('\nR({0})+ - R({1}): {2}'.format(start, end, len(relevant_nodes)))
            
            for node in graph.keys():
                if node not in relevant_nodes:
                    del graph[node]
            
            for node in relevant_nodes:
                keep = []
                for succ in graph[node]:
                    if end in reachable(graph,succ):
                        keep.append(succ)
                graph[node] = keep 
        
            print '|V| in subgraph G\': ',len(graph)
            print('\nR({0})+ - R({1}): {2}'.format(start, end, len(relevant_nodes)))
            return answer
        else:
            if R_s == R_t:
                relevant_nodes = R_s
            else:   
                relevant_nodes = set(R_s).difference(set(R_t))
                relevant_nodes = list(relevant_nodes)+[end]
                not_reached = []
                for node in relevant_nodes:
                    if end not in reachable(graph, node):
                        not_reached.extend([node])
                
                for node in not_reached:
                    del graph[node]
                
                relevant_nodes = list(set(relevant_nodes).difference(set(not_reached)))
            for component in scc:
                if end in component:
                    [relevant_nodes.append(node) for node in component if node not in relevant_nodes]
            print('\nR({0})+ - R({1}): {2}'.format(start, end, len(relevant_nodes)))
            
            for node in graph.keys():
                if node not in relevant_nodes:
                    del graph[node]
            
            for node in relevant_nodes:
                keep = []
                for succ in graph[node]:
                    if end in reachable(graph,succ):
                        keep.append(succ)
                graph[node] = keep 
        
            print '|V| in subgraph G\': ',len(graph)
            print('\nR({0})+ - R({1}): {2}'.format(start, end, len(relevant_nodes)))
            return (True, longestscc+len(graph.keys()), graph)

def topol_dict(graph):
    global topol_ictionary
    topol_dictionary = {}
    def f(nodeinList):
        return reduce(lambda x,y:x+y, nodeinList) 
    topological_sort = map(lambda x:list(x), fuseCycle.sort_topologically_stackless(graph))
    topological_sort.reverse()
    for key_node in topological_sort:
        if len(key_node) == 1:
            topol_dictionary.update({f(key_node):topological_sort.index(key_node)})
        else:
            [topol_dictionary.update({f(node):topological_sort.index(key_node)}) for node in key_node]
    return topol_dictionary

def get_bridge_edges(edges, graph, topol_dictionary): 
    def get_index(node, graph):
        return topol_dictionary[node]
    morethan_length_one_edges = []
    for edge in edges:
        if abs(get_index(edge[0], graph)-get_index(edge[1], graph)) > 1:
            morethan_length_one_edges.append(edge)
    return morethan_length_one_edges

def define_mergeable_edges(edges, graph, topol_dictionary):
    edges = map(lambda x:list(x), edges)
    mergeable_edges_list = []
    def get_index(node):
        return topol_dictionary[node]
    while len(edges) is not 0:
        mergeable_edges = []
        for edge in edges:
            if len(mergeable_edges) is 0:
                mergeable_edges.append(list(edge))
            else:
                count = 0
                for medges in mergeable_edges:
                    # 13|24 12|34 12|23
                    m0 = get_index(medges[0])
                    e0 = get_index(edge[0])
                    m1 = get_index(medges[1])
                    e1 = get_index(edge[1])
                    # if get_index(medges[0]) < get_index(edge[0]) < get_index(medges[1]) or get_index(medges[0]) < get_index(edge[1]) < get_index(medges[1]):
                    if m0 < e0 < m1 or m0 < e1 < m1:
                    #if m0 < e0 is between m0 and m1 or, e1 is between m0 and m1:
                        count = count
                        print 'Edge {0} and edge {1} are not mergeable'.format(edge[0]+edge[1], medges[0]+medges[1])
                    else:
                        count += 1
                        print 'Edge {0} and edge {1} are mergeable'.format(edge[0]+edge[1], medges[0]+medges[1])

                if count is len(mergeable_edges):
                    mergeable_edges.append(list(edge))
        new_edges = []
        [new_edges.append(edge) for edge in edges if edge not in mergeable_edges]
        
        edges = new_edges
        mergeable_edges_list.append(mergeable_edges)
    return mergeable_edges_list

def get_shared_edges(bridge, edges_set, start_vertex, end_vertex, graph, topol_dictionary, prob_table, cyclenode_list, mode):
    shared_edges_paths = []
    #f = lambda x:x[0]
    def get_index(node):
        return topol_dictionary[node]
    def relevent_node_set(start, end, depth):
        return set(reduce(lambda x,y:x+y, find_all_paths(graph, start, end)))
        #return set(reduce(lambda x,y:x+y, find_all_paths_with_IDDLS(graph, start, end)))
    def get_edges(path):
        edges = []
        for x in range(0, len(path)-1):
            edges.append((path[x], path[x+1]))
        return edges
    #bridge_edges = [[('2','5'),('3','5')],[('2','4'),('4','6'),('2','6')],[('1','5')]]
    relevant_paths = []
    all_paths = find_all_paths(graph, start_vertex, end_vertex)
    #all_paths = find_all_paths_with_IDDLS(graph, start_vertex, end_vertex)
    print 'allPATHS',len(all_paths)
    for path in all_paths:
        relevant_paths.append(get_edges(path))
     
    mergeable_paths_dictionary = {}
    key_to_dict = []
    mergeable_paths = []
    mergeable = []
    
    for edges in edges_set:   
        mpaths = []
        temp_rpath = []
        rpath = []
        key = []
        print 'mergeable keys : ',edges
        for edge in edges:
            key.extend([edge[0]+edge[1]])
            # [rpath.append(all_paths[relevant_paths.index(path)]) for path in relevant_paths if edge in path]
            for path in relevant_paths:
                # and any(bridge not in path for bridge in bridge_node)
                temp = []
                if tuple(edge) in path:
                    # temp_rpath.append(all_paths[relevant_paths.index(path)])
                    # print 'added\n',all_paths[relevant_paths.index(path)]
                    temp.append(all_paths[relevant_paths.index(path)])
                    #print 'added\n',all_paths[relevant_paths.index(path)]
                    
                correct_path = True
                for link in get_edges(temp):
                    if abs(get_index(link[0])-get_index(link[1])) > 1:
                        if (link[0], link[1]) != (edge[0], edge[1]):
                            correct_path = False
                if correct_path:
                    rpath.append(temp)     
                # path = [(start-edge[0]), (edge[0]-edge[1]), (edge[1]-end)] = [(part_two), (part_one), (part_three)]
            walk_path = []
            temp_part_one = []
            bridge_paths = []
            final_paths = []
            #[temp_part_one.append(paths) for paths in find_all_paths_with_IDDLS(graph, edge[0], edge[1])]
            [temp_part_one.append(paths) for paths in find_all_paths(graph, edge[0], edge[1])]
            nb_of_longest_paths = 0
            for path_one in temp_part_one:
                correct_path = True
                for link in get_edges(path_one):
                    if abs(get_index(link[0])-get_index(link[1])) > 1:
                        if (link[0], link[1]) != (edge[0], edge[1]):
                            correct_path = False
                    
                if correct_path:
                    nb_of_longest_paths = nb_of_longest_paths + 1
                    bridge_paths.append(path_one)

            for wpath in bridge_paths:
                walk_part_two = []
                temp_part_two = []
                if edge[0] is not start_vertex:
                    #[temp_part_two.append(paths) for paths in find_all_paths_with_IDDLS(graph, start_vertex, edge[0])]
                    [temp_part_two.append(paths) for paths in find_all_paths(graph, start_vertex, edge[0])]
                    for path_two in temp_part_two:
                        interval_part_two = 0
                        for edge_part_two in get_edges(path_two):
                            interval_part_two += abs(get_index(edge_part_two[0])-get_index(edge_part_two[1]))
                        if interval_part_two is len(path_two)-1:
                            walk_part_two.append(path_two)
                            #print '\np2',path_two    
                    for path in walk_part_two:
                        walk_path.append(path[:-1] + wpath)
                else:
                    walk_path.append(wpath)
            
            for wpath in walk_path:
                walk_part_three = []
                temp_part_three = []
                if edge[1] is not end_vertex:
                    #[temp_part_three.append(paths) for paths in find_all_paths_with_IDDLS(graph, edge[1], end_vertex)]
                    [temp_part_three.append(paths) for paths in find_all_paths(graph, edge[1], end_vertex)]
                    for path_three in temp_part_three:
                        interval_part_three = 0
                        for edge_part_three in get_edges(path_three):
                            interval_part_three += abs(get_index(edge_part_three[0])-get_index(edge_part_three[1]))
                        if interval_part_three is len(path_three)-1:
                            walk_part_three.append(path_three)
                    for path in walk_part_three:
                        final_paths.append(wpath + path[1:])
                else:
                    final_paths.append(wpath)
                # if len(final_paths) >1 :
                #     print '\nnewest',final_paths[-1]
            for path in final_paths:
                if path not in mpaths:
                    mpaths.append(path)        
        key_to_dict.append(tuple(key))
        mergeable_paths_dictionary.setdefault(tuple(key), [])
        mergeable_paths.extend(mpaths)
        mergeable_paths_dictionary[tuple(key)].extend(mpaths)
        
        for paths in mergeable_paths:
            [mergeable.append((paths[n],paths[n+1])) for n in range(0,len(paths)-1) if abs(get_index(paths[n])-get_index(paths[n+1])) is 1]
        shared_edges_paths.append(set(mergeable))
    print 'l(E) = {0}'.format(key_to_dict)
    choice_node_set = []
    
    for edge in bridge:
        choice = []
        for node in edge:
            #print vertex_degree(graph, node)
            if vertex_degree(graph, node) > 2:
                choice.append(node)
        choice_node_set.append(choice)
    print 'Choice node set: ', choice_node_set

    def eliminate_choice_node(choice_node_set, mergeable_paths_dictionary):  
        newest_mergeable_dict = {}    
        for k in mergeable_paths_dictionary:
            v = mergeable_paths_dictionary[k]
            newest_mergeable_paths = []
            done = []
            for node in choice_node_set:
                for path in v:
                    if node in path:  
                        print '\n *******chocie node should be deleted: ', node, '*********'  
                        index = path.index(node)
                        #print path, '\n', path[:index]+path[index+1:], '\n'
                        if node in cyclenode_list:
                            if path[index-1]+path[index+1] not in done:
                                #print '\n1',[path[index-1],node], [node,path[index+1]]
                                #reduction_rules(rule, alpha, beta=0, mode=0, quantiles=0)
                                updated_prob = fuseCycle.calculate_probability([path[index-1],node], [node,path[index+1]], mode, prob_table, 1)
                        else:
                            if path[index-1]+path[index+1] not in done:
                                #print '\n2',[path[index-1],node], [node,path[index+1]]
                                updated_prob = fuseCycle.calculate_probability([path[index-1],node], [node,path[index+1]], mode, prob_table) # mode = 2
                        
                        prob_table.update({path[index-1]+path[index+1]:updated_prob})
                        done.append(path[index-1]+path[index+1])
                        print('*Note* probability({0}) = {1} is updated.'.format([path[index-1], path[index+1]], updated_prob))
                        
                        newest_mergeable_paths.append(path[:index]+path[index+1:])
                    else:
                        if len(set(path).intersection(set(choice_node_set))) is 0:
                            newest_mergeable_paths.append(path)
                            
            newest_mergeable_dict.update({k:newest_mergeable_paths})
        return newest_mergeable_dict

    if len(choice_node_set) is not 0:
        while len(choice_node_set) is not 0:
            print "choice node set (len -1)",choice_node_set[0]
            newest_mergeable_dict = eliminate_choice_node(choice_node_set[0], mergeable_paths_dictionary)
            del choice_node_set[0]
            mergeable_paths_dictionary = newest_mergeable_dict
    return (set.intersection(*shared_edges_paths), mergeable_paths_dictionary, prob_table)

def group_by_three_substring(paths):
    substring = []
    [substring.append((path[n], path[n+1], path[n+2])) for path in paths for n in range(0, len(path)-2)]
    return set(substring)

def get_elimination_nodes(paths, start, end):
    return list(set(reduce(lambda x,y:x+y, paths)).difference(set([start]).union(set([end]))))

global paths_after_merge, already_merged
paths_after_merge = {}
already_merged = []
 