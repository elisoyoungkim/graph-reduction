# Title:  On the Semantics of Queries over Graphs with Uncertainty

## ABSTRACT

We study the semantics of queries over uncertain graphs, which are directed graphs in which each edge is associated with a value in [0,1] representing its certainty. In this work, we consider the certainty values as probabilities and show the challenges involved in evaluating the reachability and transitive closure queries over uncertain/probabilistic graphs. As the evaluation method, we adopted graph reduction from automata theory used for finding regular expressions for input finite state machines. However, we show that different order of eliminating nodes may yield different certainty associated with the results. We then formulate the notion of "correct" results for queries over uncertain graphs, justified based on the notion of common sub-expressions, and identify common paths and avoid their redundant multiple contributions during the reduction. We identify a set of possible patterns to facilitate the reduction process. We have implemented the proposed ideas for answering reachability and transitive closure queries. We evaluated the effectiveness of the proposed solutions using a library of many uncertain graphs with different sizes and structures. We believe the proposed ideas and solution techniques can yield query processing tools for uncertain data management systems.# graph-reduction

http://spectrum.library.concordia.ca/981891/1/Kim_MSc_F2016.pdf
