""" The Strongly Connected Components of a directed graph are subsets of nodes such that each node within a subset
    can be reached from each other node. Tarjan's algorithm can identify these components efficiently"""

from pyswip import *
from random import choice
from pyswip import Functor, Variable, Query
import networkx as nx

def strongly_connected_components(graph):
    """ Find the strongly connected components in a graph using Tarjan's algorithm.
        graph should be a dictionary mapping node names to lists of successor nodes."""
    
    result = [ ]
    stack = [ ]
    low = { }
    selfloop = []   
    def visit(node):
        if node in low: return
        
        
        num = len(low)
        low[node] = num
        stack_pos = len(stack)
        stack.append(node)
        for successor in graph[node]:
            if node is successor:
                selfloop.append(node)
            visit(successor)
            low[node] = min(low[node], low[successor])
        
        if num == low[node]:
            component = tuple(stack[stack_pos:])
            del stack[stack_pos:]
            result.append(component)
            for item in component:
                low[item] = len(graph)
    
    for node in graph:
        visit(node)
    
    return (result, selfloop)


def topological_sort(graph):
    count = { }
    for node in graph:
        count[node] = 0
    for node in graph:
        for successor in graph[node]:
            count[successor] += 1

    ready = [ node for node in graph if count[node] == 0 ]
    
    result = [ ]
    while ready:
        node = ready.pop(-1)
        result.append(node)
        
        for successor in graph[node]:
            count[successor] -= 1
            if count[successor] == 0:
                ready.append(successor)
    return result


def robust_topological_sort(graph):
    """ First identify strongly connected components,
        then perform a topological sort on these components. """

    (components, selfloop) = strongly_connected_components(graph)

    node_component = { }
    for component in components:
        for node in component:
            node_component[node] = component

    component_graph = { }
    for component in components:
        component_graph[component] = [ ]
    
    for node in graph:
        node_c = node_component[node]
        for successor in graph[node]:
            successor_c = node_component[successor]
            if node_c != successor_c:
                if successor_c not in component_graph[node_c]:
                    component_graph[node_c].append(successor_c)     
    return (component_graph, topological_sort(component_graph), selfloop)

def get_reduced_graph(component_graph, scc):
    scc = [x for x in scc if len(x)>1]
    scc_dict = {}
    for component in scc:
        solid_node = []
        solid_node.append('ps' + str(scc.index(component)))
        #print solid_node
        scc_dict.update({tuple(solid_node):list(component)})
        #print 'I need to know',component_graph[component], '\n', scc_dict

        component_graph.update({tuple(solid_node):component_graph[component]})
        for node in component_graph:
            if component in component_graph[node]:
                component_graph[node].remove(component)
                component_graph[node].append(tuple(solid_node))
        del component_graph[component]
    return (component_graph, scc_dict)


def transitive_closure_nx(graph):
    def generate_edges(graph):
        edges = []
        for node in graph:
            for neighbor in graph[node]:
                edges.append(node+neighbor)
                
        return edges

    edges = generate_edges(graph)
    G = nx.DiGraph()
    for v in edges:
        G.add_edge(v[0], v[1])

    edges = list(G.edges())
    print edges

    def transitive_closure(G):
        TC = nx.DiGraph()
        TC.add_nodes_from(G.nodes_iter())
        TC.add_edges_from(G.edges_iter())
        count = 0
        for v in G:
            count += 1
            print count
            TC.add_edges_from((v, u) for u in nx.dfs_preorder_nodes(G, source=v)
                              if v != u)
        return TC

    return list(transitive_closure(G).edges())

def transitive_closure_of_edges(graph):
    def generate_edges(graph):
        edges = []
        for node in graph:
            for neighbor in graph[node]:
                print '\n',node, neighbor
                edges.append(node+neighbor)  
                
        return edges

    gen_edges = generate_edges(graph)
    # start a Prolog interpreter instance
    p = Prolog()

    # load the ontology specification
    assertz = Functor('assertz', 1)
    edge = Functor('edge', 2)
    p.assertz('(path(X,Y) :- edge(X,Y))')
    p.assertz('(path(X,Y) :- edge(X,Z), path(Z,Y))')

    for link in gen_edges:
        print link[0], link[1]
        call(assertz(edge(link[0],link[1])))
    # construct look up tables of common facts 
    

    paths = list(p.query('path(X,Y)'))

    tc_edges = []
    for edge in paths:
        if (edge['X'], edge['Y']) not in tc_edges:
            tc_edges.append((edge['X'], edge['Y']))

    return tc_edges

#     print robust_topological_sort(graph)
#     scc = [x for x in robust_topological_sort(graph) if len(x)>1] 
#     print scc
