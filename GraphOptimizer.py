import numpy as np

class GraphOptimizer:
    def __init__(self, adjacency_matrix: np.array):
        self.init_from_matrix(adjacency_matrix)

    def init_from_matrix(self, adjacency_matrix: np.array):
        self.A = adjacency_matrix
        self.nodes_count = self.A.shape[0]

        if self.A.shape[0] != self.A.shape[1]:
            raise ValueError('Wrong shape of adjacency_matrix. Matrix should be square')
        
        self.levels = self.sort_nodes_by_levels()
        
    def sort_nodes_by_levels(self) -> dict:
        '''
        returns dict levels = {
            <node_name: str>: (<level: int>, <row_in_level: int>)
        }
        '''

        levels = dict()

        first_nodes = np.where((self.A==0).all(axis=0))[0] + 1
        levels.update( { str(node): (0, i) for i, node in enumerate(first_nodes)} )
        current_level = 1
        while len(levels) < self.nodes_count:
            added_nodes = set()
            for j in range(self.nodes_count):
                if str(j+1) in levels.keys():
                    continue

                adj_nodes = np.where(self.A[:,j]!=0)[0] + 1
                #Если adj_nodes подмножество levels.keys()
                if set(levels.keys()) >= set( map(str, list(adj_nodes)) ):
                    added_nodes.add(str(j+1))
            
            levels.update( { str(node): (current_level, i) for i, node in enumerate(added_nodes)} )
            current_level += 1
        
        return levels
        

