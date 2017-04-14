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
    data_structure.put((graph, start, end, []))

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
                data_structure.put((graph, neighbor, end, path + [current]))
