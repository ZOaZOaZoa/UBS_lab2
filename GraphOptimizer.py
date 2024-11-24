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

        self.first_nodes = np.where((self.A==0).all(axis=0))[0] + 1
        levels.update( { str(node): (0, i) for i, node in enumerate(self.first_nodes)} )
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
        
        self.max_level = current_level - 1
        return levels
        
    def min_tracks_from(self, node_from_name: str):
        #tracks_info = { <узел>: (<расстояние>, <путь>) }
        self.tracks_info: dict = { node_name: (np.inf, '') for node_name in self.levels.keys() }
        self.tracks_info[node_from_name] = (0, node_from_name)

        for level in range(self.max_level):
            for node_name, placement in self.levels.items():
                if placement[0] != level:
                    continue

                node_ind = int(node_name) - 1
                adj_node_inds = np.where(self.A[node_ind,:] != 0)[0]
                for adj_node_ind in adj_node_inds:
                    price_of_way = self.tracks_info[str(node_ind+1)][0] + self.A[node_ind, adj_node_ind]
                    way = self.tracks_info[str(node_ind+1)][1] + f'-{adj_node_ind+1}'

                    if price_of_way < self.tracks_info[str(adj_node_ind+1)][0]:
                        self.tracks_info[str(adj_node_ind+1)] = (price_of_way, way)

    def min_tracks_info_str(self):
        column1 = 8
        column2 = 10
        column3 = 20
        res = f"{'Узел':>{column1}}  {'Расстояние':>{column2}}  {'Кратчайший путь':>{column3}}\n"
        print(self.tracks_info)
        for node_name, info in sorted(self.tracks_info.items(), key=lambda x: int(x[0])):
            price = info[0]
            min_track = info[1]
            if price < np.inf:
                res += f'{node_name:>{column1}}  {price:>{column2}}  {min_track:>{column3}}\n'  

        print(res)
        return res          

