# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import networkx as nx
# import numpy as np

import database, reduction, robustTarjan, reachability, fuseCycle, parseDataset
global start_vertex, end_vertex
import time



if __name__ == '__main__':
    pass


    stayinMenu = True
    with open("TC.txt", "w") as text_file:  
        while stayinMenu:
            start_time = time.time()
            print('\n\nWe have 39 graph examples in our database.\n Please choose one graph example between G1 and G21 in the picture')
#             image1 = mpimg.imread("database.png")
#             #image1 = mpimg.imread("graph_examples.png")
#             plt.figure(figsize=(25,9))
#             plt.imshow(image1)
#             #plt.imshow(image1, interpolation='nearest', aspect='auto')
#             plt.axis('off')
#             plt.show()
    #         image2 = mpimg.imread("2.jpg")
    #         plt.figure(figsize=(20,8))
    #         plt.imshow(image2)
    #         plt.axis('off')
    #         #plt.show()
    #         image3 = mpimg.imread("3.jpg")
    #         plt.figure(figsize=(20,8))
    #         plt.imshow(image3)
    #         #plt.imshow(image, interpolation='nearest', aspect='auto')
    #         plt.axis('off')
    #         plt.show()
            
#             example = 9
            
            example = input(''' 
                        Please enter the graph number between 1 and 39 (e.g., press 1 for graph G1 and Enter key to proceed next steps)\t''')
            (graph, global_graph) = database.graph(example)
            (prob_table, global_prob_table) = database.probTable(example)
            
            # (edges, graph, prob_table) = parseDataset.parse()
            print '|V| = {0} and |E| = {1}'.format(len(graph), len(prob_table))
            
            # np.random.seed(0)
            # fig = plt.figure(facecolor='lightgrey')  
            #      
            # G = nx.DiGraph()
            # for node, edges in graph.items():
            #     G.add_node(node)
            #     for edge in edges:
            #         G.add_edges_from([(node, edge)], weight=prob_table[node+edge])
            #    
            # edge_labels = {}
            # for edge in G.edges():
            #     l_edge = list(edge)
            #     edge_labels.update({edge:prob_table[reduce(lambda x,y:x+y, l_edge)]})
            #    
            # # There are 4 graph layouts: shell, spring, spectral, and random  
            # if len(G.nodes()) < 5:
            #     pos = nx.random_layout(G)
            # elif len(G.nodes()) >= 5 and len(G.nodes()) < 12:
            #     pos = nx.shell_layout(G)
            # else:
            #     pos = nx.shell_layout(G)
            #    
            # nx.draw_networkx_nodes(G, pos, node_size=100,nodelist=G.nodes(),node_color= 'deeppink') #mediumaquamarine
            # nx.draw_networkx_edges(G, pos, arrows = False)
            # #nx.draw_networkx_labels(G, pos, font_size=3, font_family='sans-serif')
            # #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            # #nx.draw_networkx_nodes(G,pos,node_size=800,nodelist=[start_vertex],node_color= 'green')
            # #nx.draw_networkx_nodes(G,pos,node_size=800,nodelist=[end_vertex],node_color='red')
            # #nx.draw_networkx_labels(G, pos)
            # #ax = fig.add_subplot(111)  
            # # ax.text(0.95, 0.01, 'Connectivity: {0}'.format(ans),
            # #         verticalalignment='bottom', horizontalalignment='right',
            # #         transform=ax.transAxes,
            # #         color='green', fontsize=15)
            # plt.axis('off')
            # plt.show() 
            ans = input('''\nMenu 
            1. Edges in the transitive closure of G
            2. Find strongly connect components (SCCs) of G
            3. Find reachability probability given a pair of target nodes by user
                     ''')
#             ans = 3
            if ans is 1:
                (component_graph, scc, selfloop) = robustTarjan.robust_topological_sort(graph)
                (graph, scc_dict) = robustTarjan.get_reduced_graph(component_graph, scc)
                transitive_closure_edges = robustTarjan.transitive_closure_nx(graph)
                tc = []
                for edge in transitive_closure_edges:
                    pre = []
                    succ = []
                    pre.append(edge[0])
                    succ.append(edge[1])
                    if tuple(pre) in scc_dict or tuple(succ) in scc_dict:
                        if tuple(pre) in scc_dict and tuple(succ) in scc_dict:
                            for pre_node in scc_dict[tuple(pre)]:
                                for succ_node in scc_dict[tuple(succ)]:
                                    tc.append((pre_node,succ_node))
                        elif tuple(pre) in scc_dict and tuple(succ) not in scc_dict:
                            for pre_node in scc_dict[tuple(pre)]:
                                tc.append((pre_node, edge[1]))
                        elif tuple(pre) not in scc_dict and tuple(succ) in scc_dict:
                            for succ_node in scc_dict[tuple(succ)]:
                                tc.append((edge[0], succ_node))
                                
                    else:
                        tc.append(edge)
                [tc.append((node,node)) for node in selfloop]

                scc = [x for x in scc if len(x)>1] 
                for sameclass in scc:
                    for component_1 in sameclass:
                        for component_2 in sameclass:
                            tc.append((component_1, component_2))
                #E_star = set(tc)
                #print tc
                # for x in tc:
                #     print tc.index(x), x
                #print tc
                print 'There are {0} edges in E*'.format(len(set(tc)))
            elif ans is 0:
                #transivie_closure_edges = reduction.transitive_closure(parseDataset.edges)
                transitive_closure_edges = reduction.transitive_closure(reduction.generate_edges(graph))
                #(transitive_closure_edges, scc, selfloop) = robustTarjan.robust_topological_sort(graph)
                #(component_graph, scc, selfloop) = robustTarjan.robust_topological_sort(graph)
                # scc = [x for x in scc if len(x)>1] 
                # print scc
                # for sameclass in scc:
                #     for component_1 in sameclass:
                #         for component_2 in sameclass:
                #             transitive_closure_edges.append((component_1, component_2))
                #transitive_closure_edges = reduction.transitive_closure(reduction.generate_edges(graph))
            
                
                for x in transitive_closure_edges:
                    print   x
                print 'There are {0} edges in E*'.format(len(transitive_closure_edges))
            elif ans is 2:
                (transitive_closure, scc, selfloop) = robustTarjan.robust_topological_sort(graph)
                print scc
                print 'There are {0} SCCs in G'.format(len(scc))
            elif ans is 3: 
#                 tc = 1 
                tc = input('''
                        1. Single pair of nodes
                        2. Multi pair of nodes 
                        3. Full Transitive closure edges   
                        ''')  
                 
                if tc is 1:
                    mode = input('''
                                      Please choose disjunction function: f(x,y) = x + y
                                      1. Max: f(x,y) = max(x,y)
                                      2. Independent: f(x,y) = x + y -xy \t''')
                            
                    start_vertex = raw_input('''
                              Please choose a pair of nodes that you want to check the reachability probability.
                              First enter the start node in V: ''')
                    end_vertex = raw_input('''
                              Then, enter the end node in V: ''')
#                     mode = 2
#                     start_vertex = 'a'
#                     end_vertex = 'h'
#                     stayinMenu = False
                    #print('\n\tV in G{0} is {1}'.format(example, list(set(graph.keys()+reduce(lambda x,y: x+y,graph.values())))))
                    scc = []
                    reachability.reachability(scc, graph, prob_table, start_vertex, end_vertex, mode)
                    
                elif tc is 2:
                    print 'in the process'
                elif tc is 3:
                    
                    reachability.transitive_closure_E = []
                    count = 0
                    def tc_computation(edge, graph, prob_table, start, end, mode, tcmode=1):
                        reachability.reachability(scc, graph, prob_table, start, end, mode, list(edge), 1)
                    
                    # (transitive_closure_edges, scc) = robustTarjan.robust_topological_sort(graph)


                    (component_graph, scc, selfloop) = robustTarjan.robust_topological_sort(graph)
                    (graph, scc_dict) = robustTarjan.get_reduced_graph(component_graph, scc)
                    transitive_closure_edges = robustTarjan.transitive_closure_nx(graph)
                    print len(transitive_closure_edges)
                    tc = []
                    print scc_dict
                    for edge in transitive_closure_edges:
                        pre = []
                        succ = []
                        pre.append(edge[0])
                        succ.append(edge[1])
                        if tuple(pre) in scc_dict or tuple(succ) in scc_dict:
                            if tuple(pre) in scc_dict and tuple(succ) in scc_dict:
                                for pre_node in scc_dict[tuple(pre)]:
                                    for succ_node in scc_dict[tuple(succ)]:
                                        #print '\n1',(pre_node,succ_node)
                                        tc.append((pre_node,succ_node))
                            elif tuple(pre) in scc_dict and tuple(succ) not in scc_dict:
                                for pre_node in scc_dict[tuple(pre)]:
                                    #print '\n3',(pre_node, edge[1])
                                    tc.append((pre_node, edge[1]))
                            elif tuple(pre) not in scc_dict and tuple(succ) in scc_dict:
                                for succ_node in scc_dict[tuple(succ)]:
                                    #print '\n2',(edge[0], succ_node)
                                    tc.append((edge[0], succ_node))
                                
                        else:
                            tc.append(edge)
                    [tc.append((node,node)) for node in selfloop]

                    scc = [x for x in scc if len(x)>1] 
                    print scc
                    for sameclass in scc:
                        for component_1 in sameclass:
                            for component_2 in sameclass:
                                tc.append((component_1, component_2))

                    # scc = [x for x in scc if len(x)>1] 
                    # for sameclass in scc:
                    #     for component_1 in sameclass:
                    #         for component_2 in sameclass:
                    #             transitive_closure_edges.append((component_1, component_2))
                    #for edge in reduction.transitive_closure(reduction.generate_edges(graph)):
                    #print '%%%%%%%',transitive_closure_edges
                    for edge in tc:
                        fuseCycle.cyclic_node_set = []
                        global removed
                        removed = []
                        #start_vertex = edge[0]
                        #end_vertex = edge[1]
                        mode = 2
#                         input_graph = global_graph.copy()
#                         input_prob_table = global_prob_table.copy()
                        (input_graph,x) = database.graph(example)
                        (input_prob_table,y) = database.probTable(example)
                        print 'No==',tc.index(edge)
                        tc_computation(edge, input_graph, input_prob_table, edge[0], edge[1], mode, tcmode=1)
                        
                        
                        
#                     for edge in reduction.transitive_closure(parseDataset.edges):
#                     #for edge in reduction.transitive_closure(reduction.generate_edges(graph)):
# #                                            
#                         count += 1
#                         print count
#                         print 'Global',len(global_graph)
#                         print 'Global',len(global_prob_table)
#                         #prob_table = database.probTable(example)
#                         fuseCycle.cyclic_node_set = []
#                         global removed
#                         removed = []
#                         start_vertex = edge[0]
#                         end_vertex = edge[1]
#                         mode = 2
#                             
#                         #print('\n\tV in G{0} is {1}'.format(example, list(set(graph.keys()+reduce(lambda x,y: x+y,graph.values())))))
#                         reachability.reachability(global_graph, global_prob_table, start_vertex, end_vertex, mode, list(edge), tcmode=1)
                            
                    print reachability.transitive_closure_E
                    count = 0
                    
                 
                    #text_file.write('G{0}\n'.format(example))
                    text_file.write('G{0}\n')
                    for tup in set(reachability.transitive_closure_E):
                        count += 1
                        #print '{0}:\t {1}:\t{2}\n'.format(transitive_closure_E.index(tup)+1, tup[:-1], tup[2])
                        print '{0}.\t {1}  {2}:\t{3}\n'.format(count, tup[0], tup[1], tup[2])   
                        text_file.write('{0}.\t {1}  {2}:\t{3}\n'.format(count, tup[0], tup[1], tup[2]))                   
                    
                    
                    
                    
            else:
                print('Wrong number, please choose again!\n\n')
            print("--- %s seconds ---" % (time.time() - start_time))

    text_file.close()
            

    
