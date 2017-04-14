# On the Semantics of Queries over Graphs with Uncertainty

## ABSTRACT

We study the semantics of queries over uncertain graphs, which are directed graphs in which each edge is associated with a value in [0,1] representing its certainty. In this work, we consider the certainty values as probabilities and show the challenges involved in evaluating the reachability and transitive closure queries over uncertain/probabilistic graphs. As the evaluation method, we adopted graph reduction from automata theory used for finding regular expressions for input finite state machines. However, we show that different order of eliminating nodes may yield different certainty associated with the results. We then formulate the notion of "correct" results for queries over uncertain graphs, justified based on the notion of common sub-expressions, and identify common paths and avoid their redundant multiple contributions during the reduction. We identify a set of possible patterns to facilitate the reduction process. We have implemented the proposed ideas for answering reachability and transitive closure queries. We evaluated the effectiveness of the proposed solutions using a library of many uncertain graphs with different sizes and structures. We believe the proposed ideas and solution techniques can yield query processing tools for uncertain data management systems.# graph-reduction

## The Proposed Algorithm

We present a set of patterns of paths and its corresponding rules to reduce a probabilistic graph. Our reduction algorithm is carried out through node reduction and edge aggregation in an input graph G until one edge, connecting a source node vs to
a target node vf , remains. It induces the relevant subgraph of G and finds the reachability weight as ω(vs, vf ). When the subgraph has cycles, it reduces cyclic to acyclic and then determines ω(vs, vf ).

This is done by repeatedly applying reduction rules to the reduced subgraph until no more rules can be applied to obtain the aggregated weight on a single edge (vs, vf ). The proposed solution techniques underlie the proper
order of nodes elimination based on the notion of least common sub-expressions.

### Proposed solution
The key point is to find least common sub-expressions in the final aggregated probabilities, that is, avoiding unnecessary redundant computations. On the one hand, if two or more nodes in a probabilistic graph belong to the same SCC class, then
such nodes are considered indistinguishable and hence converted into a solid node which replaces the corresponding SCC. By treating them indistinguishable, we can avoid overcomputing problems. On the other hand, we strictly regulate the order in
which nodes are eliminated. The proposed algorithm is partitioned into three phases. In the first phase, it finds the relevant subgraph of an input G if a source node vs and a target node vf in G. The second phases finds the cycles in G', if any, and reduce them into "solid" nodes in a disciplined way. This generate an acyclic graph G''. The last phase requires nodes reduction process in G''. It then computes the reachability value as ω(vs, vf ).

### PSEDOCODE
![alt tag](https://cloud.githubusercontent.com/assets/22326212/25047406/7b25678a-2104-11e7-8a19-01c898316c12.png)

#### Thesis Link: http://spectrum.library.concordia.ca/981891/1/Kim_MSc_F2016.pdf
