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

#### Finding the Relevant Subgraph
The first phase of the reduction algorithm is to get the relevant subgraph. We first obtain the set R(vs) of nodes that are reachable from vs. To get the set V' of nodes are only relevant to (vs, vf ), for a node v in R(vs), if v is contributing to vf the v
is included in V , that is the subgraph of G = (V,E) induced by V' ⊆ V, which is
G' = (V', {(i, j)|(i, j) ∈ E, for i, j ∈ V'}).
3.1.2 Reducing Cycles in the Relevant Subgraph
The second phase detects cycles and reduces them in the relevant subgraph G'. The
nodes that are on a cyclic path form a strongly connected component, we then replace
them by a single solid node. This phase can be omitted if G' is acyclic.

#### Reducing Nodes in the Reduced Relevant Subgraph
Eliminate all the relevant nodes in G but vs and vf , using the reduction rules/patterns.
This phase eliminates all the nodes but vs and vf one by one until one single edge
remains connecting vs to vf . Finally we get the reachability weight as ω(vs, vf ).

### Types of Nodes
We have two considerations on classifying node types in the presence of cycles in an
input graph G. Suppose G = (V,E) has cycles. If a node v ∈ V is involved in a
cyclic path, we say that v is a cyclic node. Now consider a graph G that does not
include any cycles. Here we denote the number of incoming and outgoing edges of a
node v by deg−(v) and deg+(v), respectively. Depending on the number of incident
edges on a node, we classify the node in an input graph G into five types: source,
sink, isolated, sequence, and split. A source node is a node without any incoming
edges, while a sink node is a node without outgoing edges. An isolated node is a
node having no incident edges. A node is called a sequence node if it has exactly one
incoming and one outgoing edge. Otherwise, a node v is called a split node, that is
deg−(v) + deg+(v) > 2. More specifically, when the summation of incoming edges
and outgoing edges of v is greater than 2, we call node v "split" for deg−(v) ≥ 1 and
deg+(v) ≥ 1. Note that phase 1 removes all the "isolated" nodes since isolated node
is not connected with any node in G while phase 2 removes all "cyclic" nodes.
We use this categories of nodes to classify the types of paths for defining patterns
in that each pattern has its own corresponding rule.
19
3.3 Types of Patterns and Rules
There are five patterns and its corresponding rules to compute the weight of each
pattern of path: chain, choice, cycle, merge, and mesh as following.
(a) Rule 1: ω(i, j) = a*b (b) Rule 2: ω(i, j) = a ⊕ b (c) Rule 3: ω(j, j) = b^* = b'1
1−b
(d) Rule 4: (a'b'⊕ c)d' ⊕ a'(b'd' ⊕ e) (e) Rule 5: (a'c ⊕ b'f)g ⊕ (a'e ⊕ b'd)h
Figure 3.1: Basic node reduction rules: chain, choice, cycle, merge, and mesh.
Rule 1: Chain Rule. The chain rule has higher priority over rule 2. If a node
has exactly one incoming and outgoing edge, we can remove such node by aggregating
incident edges on that node with the considered conjunction function , shown in
3.1(a).
Rule 2: Choice Rule. When there are more than one of paths between two
nodes in parallel, weights on such paths are aggregated with the considered disjunction
function ⊕ to be a single edge connecting two endpoints, shown in 3.1(b).
20
Rule 3: Cycle Rule. The cycle rule defines a weight computation for a cyclic
path. Computing the weight of a cyclic path can be complicated when the input
graph includes nested cycles. Nodes involved in any cyclic path are reduced to a solid
self-loop in a disciplined way by chain and choice rules. Once a single self-loop node
remains we apply the cyclic equation for length-one path. The proposed formula in
3.1(c) is used to compute ω(j, j) by applying geometric sequence summation equation,
explained in Section 3.2.
After applying the reduction rules mentioned above, to get ω(vs, vf ) in G, there
are no more of sequence nodes. From that, vs is a source node, vf is a sink node, and
the remaining nodes are split. In such case, more than one node should be eliminated
in a single node reduction phase. There are two cases: one with a unique topological
sort, and the other with multiple topological sort in nodes.
Rule 4: Merge Rule. The merge rule handles the first case where all nodes
are removed together at once. It combines parallel paths correctly under different
possible scenarios, shown in 3.1(d).
Rule 5: Mesh Rule. The mesh rule is applied in the other case when "there
are more than one of topological sort", shown in 3.1(e).
By iteratively applying these reduction rules above, we develop a reduction algorithm
that computes the weight associated with every pair of path ω(i, j) in the
graph without any overcomputation.

## PSEDOCODE ##
![alt tag](https://cloud.githubusercontent.com/assets/22326212/25047053/be52f88a-2102-11e7-93ab-ff1d941b7025.png)

http://spectrum.library.concordia.ca/981891/1/Kim_MSc_F2016.pdf
