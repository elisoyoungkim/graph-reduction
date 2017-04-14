import Queue, os, reduction, fuseCycle, IterativeDDLS, robustTarjan
# from copy import deepcopy

global transitive_closure_E
transitive_closure_E = []
def recursive_reduction(mode, paths, cyclenode_list, all_paths_of_fused_graph, start_vertex, end_vertex, prob_table):
    #paths = [['a', 'b', 'e', 'f'], ['a', 'b', 'd', 'e', 'f'], ['a', 'b', 'f']]    
    elimination_set = reduction.get_elimination_nodes(all_paths_of_fused_graph, start_vertex, end_vertex)
    print('The set of relevant intermediate nodes R({0})-R+({1}) = {2}'.format(start_vertex, end_vertex, elimination_set))
    recursive_paths_list = []
    recursive_paths_list.extend(paths)
    subpath = list(reduction.group_by_three_substring(paths))
    #print 'subpath',subpath
    def recursive(recursive_paths_list, node):
        for paths in recursive_paths_list:
            if node in paths:
                paths.remove(node)
                #print 'recursive',recursive_paths_list
                subpath = list(reduction.group_by_three_substring(recursive_paths_list))
        #print(recursive_paths_list)
        return subpath
    # remove sequence nodes first
    removed_dict = {}
    removed = []
    for substring in subpath: 
        #while len(elimination_set) != 0:
        for node in elimination_set:
            degree = []
            sequence_nodes = {}
            [degree.append(substring[1]) for substring in subpath]
            [sequence_nodes.update({v:[subpath[degree.index(v)][0], subpath[degree.index(v)][2]]}) for v in degree if degree.count(v) is 1]
            if node in sequence_nodes:
                print '\nElimination node : \t{0}'.format(node)

                predecessor = sequence_nodes[node][0]
                successor = sequence_nodes[node][1]
                if node in cyclenode_list:
                    #print '\n5', [predecessor,node],[node,successor]
                    updated_prob = fuseCycle.calculate_probability([predecessor, node], 
                                                                   [node, successor], mode, prob_table, 1)
                else:
                    #print '\n6', [predecessor,node],[node,successor]
                    updated_prob = fuseCycle.calculate_probability([predecessor, node],
                                                                   [node, successor], mode, prob_table) # mode = 2
                prob_table.update({predecessor+successor:updated_prob})
                removed_dict.update({node:[predecessor,successor]})
                #print('*Note* probability({0}) = {1} is updated.'.format([predecessor,successor], updated_prob))
                if node not in removed:
                    removed.append(node)
                elimination_set.remove(node)
                #print 'E_set', elimination_set
                subpath = recursive(recursive_paths_list, node)
                #print 'E_set', elimination_set
    return (recursive_paths_list, removed, removed_dict)

def input_nodes(start_vertex, end_vertex):
    return fuseCycle.start_end_in_SCCs(start_vertex, end_vertex)

def mergeable(prob_table, not_merged_yet, mlist, cycle_node_list, all_paths_of_fused_graph, start_vertex, end_vertex, fused_graph):
    for paths in mlist:
        del not_merged_yet[0]
        for path in paths:
            edgebased_path = []
            [edgebased_path.append(path[index]+path[index+1]) for index in range(len(path)-1)]  
            reduced = []
            for index in range(len(not_merged_yet)):
                reduced.extend(not_merged_yet[index])
            for edge in reduced:
                if edge in edgebased_path:
                    if path in mlist:
                        mlist[mlist.index(paths)].remove(path)
    i = 0
    for m in mlist:
        i = i+1
        print('\nPath({0}) = {1}'.format(i,m))
        #(done, eset, removed) = recursive_reduction(2, m, fuseCycle.cyclic_node_set, all_paths_of_fused_graph, start_vertex, end_vertex, prob_table)
        recursive_reduction(2, m, fuseCycle.cyclic_node_set, all_paths_of_fused_graph, start_vertex, end_vertex, prob_table)
    return prob_table
 
def reachable_probability(prob_table, start, end):
    if start is end:
        if start in fuseCycle.cyclic_node_set:
            return prob_table[end+end]
    else:
        if start in fuseCycle.cyclic_node_set:
            start_result = prob_table[start+start]
        else:
            start_result = 1

        if end in fuseCycle.cyclic_node_set:
            end_result = prob_table[end+end]
        else:
            end_result = 1
        return start_result*prob_table[start+end]*end_result
     
def reachability(scc, graph, prob_table, start_vertex, end_vertex, mode, edge=[], tcmode=0):
    # check whether given a start node 's' and an end node 'e' are connected
    print scc
    R_s = reduction.reachable(graph, start_vertex)
    R_t = reduction.reachable(graph, end_vertex)
    (ans, depth, graph) = reduction.connectivity(graph, start_vertex, end_vertex, prob_table,  R_s, R_t, scc)
    print ans, depth
    print('\n\t The start node \"{0}\" and end node \"{1}\" are connected: {2} '.format(start_vertex, end_vertex, ans))
    print('\n Graph G: {0}'.format(graph))
    #print('\n Probability table of G: {0}'.format(prob_table))
    print('\n')
    if ans:
        gen = IterativeDDLS.iterative_search(Queue.Queue(), graph, start_vertex, end_vertex) # bfs - using queue
        bfs_path_set = set()
        while len(bfs_path_set) < depth:
            try:
                bfs_path_set.add(next(gen))
            except:
                break
        #print bfs_path_set
        os.linesep.join(map(str, bfs_path_set))
        gen = IterativeDDLS.iterative_search(IterativeDDLS.Stack(), graph, start_vertex, end_vertex, limit=depth) # dfs  - using stack 
        dfs_path_set = set()
#         limit = 1
        while len(dfs_path_set) < depth:
            try:
                dfs_path_set.add(next(gen))
            except StopIteration:
                break
#                 limit += 1
#                 print "depth limit reached, increasing depth limit to %d" % limit
#                 gen = IterativeDDLS.iterative_search(IterativeDDLS.Stack(), graph,  start_vertex, end_vertex, limit=limit)

        os.linesep.join(map(str, dfs_path_set))
        # get all paths between start and end nodes 
        all_paths = list(dfs_path_set.union(bfs_path_set))
        print 'A set of paths using IDDLS: {0}'.format(len(all_paths))
        # detect cycles in all the paths we got from IDDLS
        list_of_cyclic_paths = fuseCycle.sort_cycle(all_paths, start_vertex, end_vertex)
        #print 'cycles!!',list_of_cyclic_paths
        for cycle in list_of_cyclic_paths:
            index = 0
            zipped = []
            for node in cycle:
                if len(zipped) is 0:
                    zipped.append(node)
                else:
                    if node != cycle[index-1]:
                        zipped.append(node)
                    else:
                        continue
                index += 1
            if len(zipped) is 1:
                zipped_cycle = zipped+[zipped[0]]
            else:
                zipped_cycle = zipped
            list_of_cyclic_paths[list_of_cyclic_paths.index(cycle)] = zipped_cycle
        #print('\n\tR({0}) - R({1}) + {{{0}}}: \n\n {2}\n'.format(start_vertex, end_vertex, all_paths))
        print('The list of cycles : {0}\n'.format(list_of_cyclic_paths))
        
        fused_graph = fuseCycle.fuse_cycle(list_of_cyclic_paths, graph, start_vertex, end_vertex, mode, prob_table)
#         f_graph = fused_graph.copy()
        #print('\nThe fused graph of G, FG, containing only relevant nodes: \t{0}\n'.format(fused_graph))
        print 'A set of cyclic nodes: {0}'.format(fuseCycle.cyclic_node_set)
        
        # update start and end nodes if any changes due to SCCs fusing step
        for component in scc:
            if start_vertex in component and end_vertex in component:
                start_vertex = input_nodes(start_vertex, end_vertex)[0]
                end_vertex = input_nodes(start_vertex, end_vertex)[1]
        #print('\nA pair of Start node and End node : {0}, {1}\n'.format(start_vertex, end_vertex))
        #all_paths_of_fused_graph = reduction.find_all_paths(fused_graph, start_vertex, end_vertex) 
        #print 'FUSEd',fused_graph
        #print prob_table
        count = 0
        # for p in fused_graph:
        #     count += 1
        #     print '\nnode:',count, p, fused_graph[p]
        depth = len(fused_graph.keys())*len(fused_graph.keys())
        gen = IterativeDDLS.iterative_search(Queue.Queue(), fused_graph, start_vertex, end_vertex) # bfs - using queue
        bfs_path_set = set()
        while len(bfs_path_set) < depth:
            try:
                bfs_path_set.add(next(gen))
            except:
                break
        #print bfs_path_set      
        os.linesep.join(map(str, bfs_path_set))
        gen = IterativeDDLS.iterative_search(IterativeDDLS.Stack(), fused_graph, start_vertex, end_vertex, limit=depth) # dfs  - using stack 
        dfs_path_set = set()
#         limit = 1
        while len(dfs_path_set) < depth:
            try:
                dfs_path_set.add(next(gen))
            except StopIteration:
                break
                # limit += 1
                # print "depth limit reached, increasing depth limit to %d" % limit
                # gen = IterativeDDLS.iterative_search(IterativeDDLS.Stack(), graph,  start_vertex, end_vertex, limit=limit)
   
        os.linesep.join(map(str, dfs_path_set))
        # get all paths between start and end nodes
        all_paths_of_fused_graph = []
        for path in list(dfs_path_set.union(bfs_path_set)):
            lpath = list(path)
            all_paths_of_fused_graph.append(lpath)
        print 'A set of paths in the reduced subgraph G\' using Iterative DFS: {0}'.format(len(all_paths_of_fused_graph))
        #print 'all_paths_of_fused_Graph',all_paths_of_fused_graph
        #print('\n\t The list of relevant paths in FG: \n\n {0}\n'.format(all_paths_of_fused_graph))
        #print('\nProbablitiy table: {0}'.format(prob_table))
        if len(all_paths_of_fused_graph) is 0:
            probability = reachable_probability(prob_table, start_vertex, end_vertex)
            print('\n Probability of ({0}, {1}) is {2}.\n\n'.format(start_vertex, end_vertex, probability))
            if tcmode is 1:
                transitive_closure_E.append((edge[0], edge[1], probability))
        elif len(all_paths_of_fused_graph) is 1:
            recursive_reduction(2, all_paths_of_fused_graph, fuseCycle.cyclic_node_set, 
                                all_paths_of_fused_graph, start_vertex, end_vertex, prob_table)
            probability = reachable_probability(prob_table, start_vertex, end_vertex)
            print('\n Probability of ({0}, {1}) is {2}.\n\n'.format(start_vertex, end_vertex, probability))
            if tcmode is 1:
                transitive_closure_E.append((edge[0], edge[1], probability))
        else:        
            #relevant_neighbours = reduction.get_elimination_nodes(all_paths_of_fused_graph, start_vertex, end_vertex)
            (p, removed, removed_dict) = recursive_reduction(mode, all_paths_of_fused_graph, fuseCycle.cyclic_node_set, 
                                                             all_paths_of_fused_graph, start_vertex, end_vertex, prob_table)

            for node in removed:
                for key in fused_graph.keys():
                    if node in fused_graph[key]:
                        for succ in fused_graph[node]:
                            if succ not in fused_graph[key]:
                                fused_graph[key].extend(fused_graph.get(node))
                        fused_graph[key].remove(node)
                del fused_graph[node]

            topol_dictionary= reduction.topol_dict(fused_graph)
            print 'Topological sort dictionary: ', topol_dictionary
            sum_of_index = sum(list(topol_dictionary.values()))
            if sum_of_index is not (len(topol_dictionary)-1)*len(topol_dictionary)/2:
                v = []
                [v.append([]) for iter in range(max(topol_dictionary.values())+1)]
                
                for node in topol_dictionary.keys():
                    #print 'node',node
                    if node not in removed:
                        v[topol_dictionary[node]].append(node)
                #print 'v',v
                bridge_node = []
                for node in v:
                    if len(node) is not 1:
                        bridge_node.append(node)
            else:
                bridge_node = []
            print 'Same topological sorting node sets: ', bridge_node 
            if len(reduction.get_elimination_nodes(p, start_vertex, end_vertex)) is 0:
                probability = reachable_probability(prob_table, start_vertex, end_vertex)
                print('\n Probability of ({0}, {1}) is {2}.\n\n'.format(start_vertex, end_vertex, probability))
                if tcmode is 1:
                    transitive_closure_E.append((edge[0], edge[1], probability))
            else: 
                edge_star = reduction.generate_relevant_edges(p)   
                #print edge_star
                #edges_set = reduction.define_mergeable_edges(reduction.get_bridge_edges(edge_star, fused_graph, topol_dictionary), fused_graph, topol_dictionary)
                bridge_edge_set = reduction.get_bridge_edges(edge_star, fused_graph, topol_dictionary)
                print 'BRIDGE',bridge_edge_set
                edges_set = reduction.define_mergeable_edges(bridge_edge_set, fused_graph, topol_dictionary)    
                # if edges set is empty, it means all paths between end-points consist of basic edges
                if len(edges_set) is 0:
                    nb_of_shared_paths = 1
                else:
                    nb_of_shared_paths = len(edges_set) 
                print('\nThere is(are) {0} different path(s).'.format(nb_of_shared_paths))
                if len(edges_set) is not 0 and len(edges_set[0]) is not 0:
                    # shared_edges = reduction.get_shared_edges(edges_set, start_vertex, end_vertex, fused_graph, topol_dictionary) 
                    # print 'edge sets',edges_set
                    (shared_edges, mergeable_paths_dictionary, prob_table) = reduction.get_shared_edges(bridge_node, edges_set, start_vertex, end_vertex, fused_graph, topol_dictionary, prob_table, fuseCycle.cyclic_node_set, mode)
                    # for edge in bridge_edge_set:
                    # if edge in shared_edges:
                    # shared_edges.remove(edge)                   
                    # print 'shared edges', shared_edges, '\n', mergeable_paths_dictionary
                    if len(shared_edges) > 1:
                        print('\nA set of shared edges: {0}'.format(shared_edges))
                        if nb_of_shared_paths > 1:
                            [prob_table.update({edges[0]+edges[1]:fuseCycle.reduction_rules(4, prob_table[edges[0]+edges[1]], quantiles=nb_of_shared_paths)}) for edges in shared_edges]
                            #print('\nNote-updated probability table: {0}'.format(prob_table))
                    
                    mlist = []
                    for paths in mergeable_paths_dictionary.values():
                        mpath = []
                        for path in paths:
                            if path not in mpath:
                                mpath.append(path)
                        mlist.append(mpath)
                    #mlist = mergeable_paths_dictionary.values()
                    #print 'mlist',mlist
                    not_merged_yet = mergeable_paths_dictionary.keys()
                    #for key, value in sorted(mergeable_paths_dictionary.iteritems(), key=lambda (k,v): (v,k)): print "%s: \n%s" % (key, value)
                    mergeable(prob_table, not_merged_yet, mlist, fuseCycle.cyclic_node_set, all_paths_of_fused_graph, start_vertex, end_vertex, fused_graph)
                    
                else:
                    choice_node_set = []
                    for edge in bridge_node:
                        choice = []
                        for node in edge:
                            if reduction.vertex_degree(graph, node) > 2:
                                choice.append(node)
                        choice_node_set.append(choice)
                    print 'Choice node set: ', choice_node_set
                    
                    def eliminate_choice_node(choice_node_set, paths_dictionary):
                               
                        newest_mergeable_paths = []  
                        for path in paths_dictionary:
                            inner_mergeable_paths = []
                            for node in choice_node_set:
                                print 'chocie node should be deleted: ', node
                                if node in path:
                                    index = path.index(node)
                                    #print path
                                    #print index
                                    if node in fuseCycle.cyclic_node_set:
                                        print '\n3',[path[index-1],node], [node,path[index+1]]
                                        updated_prob = fuseCycle.calculate_probability([path[index-1],node], [node,path[index+1]], mode, prob_table, 1)
                                    else:
                                        print '\n4',[path[index-1],node], [node,path[index+1]]
                                        updated_prob = fuseCycle.calculate_probability([path[index-1],node], [node,path[index+1]], mode, prob_table) # mode = 2
                                    prob_table.update({path[index-1]+path[index+1]:updated_prob})
                                    print '*Note* probability({0}) = {1} is updated.'.format([path[index-1], path[index+1]], updated_prob)
                                    inner_mergeable_paths.extend(path[:index]+path[index+1:])
                                else:
                                    if len(set(path).intersection(set(choice_node_set))) is 0:
                                        inner_mergeable_paths.extend(path)
                                        
                            newest_mergeable_paths.append(inner_mergeable_paths)
                            
                        return newest_mergeable_paths
                    
                    if len(choice_node_set) is not 0:
                        while len(choice_node_set) is not 0:
                            newest_mergeable_path = eliminate_choice_node(choice_node_set[0], p)
                            del choice_node_set[0]
                            p = newest_mergeable_path
                    recursive_reduction(mode, p, fuseCycle.cyclic_node_set, all_paths_of_fused_graph, start_vertex, end_vertex, prob_table)
                
                probability = reachable_probability(prob_table, start_vertex, end_vertex)
                print('\n Probability of ({0}, {1}) is {2}.\n\n'.format(start_vertex, end_vertex, probability))
                if tcmode is 1:
                    transitive_closure_E.append((edge[0], edge[1], probability))
        
    else:
        all_paths = []
        print('\n Probability of ({0}, {1}) is 0.0.\n\n'.format(start_vertex, end_vertex))
        if tcmode is 1:
            transitive_closure_E.append((edge[0], edge[1], 0.0))
            
    global start_in_SCCs, removed, paths_after_merge, already_merged, fused_graph
    start_in_SCCs = False
    fused_graph = {}

    