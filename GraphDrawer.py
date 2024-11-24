import networkx as nx
import matplotlib.pyplot as plt
from my_networkx import draw_networkx_curved_edge_labels
import numpy as np

class GraphDrawer:
    def __init__(self, levels: dict, adj_matrix: np.array=None, edges_list: list=None):
        if adj_matrix is None and edges_list is None:
            raise ValueError('Graph should me defined by edges_list or adj_matrix')
        
        self.G = nx.DiGraph()
        self.levels = levels
        self.picture_drawn = False

        if edges_list is not None:
            self.edges_list = edges_list
        else:
            self.edges_list = self.edges_from_adj_matrix(adj_matrix)
        
        self.G.add_edges_from(self.edges_list)
        
        self.pos = {n: self.node_pos(n) for n in self.G.nodes()}
        self.straight_edges, self.curved_edges = self.sort_straight_curved()
        self.edge_weights = nx.get_edge_attributes(self.G, 'weight')

        self.curved_edge_labels = {edge: self.edge_weights[edge] for edge in self.curved_edges}
        self.straight_edge_labels = {edge: self.edge_weights[edge] for edge in self.straight_edges}

    def edges_from_adj_matrix(self, adj_matrix):
        edges_list = []
        nodes = adj_matrix.shape[0]
        for i in range(nodes):
            for j in range(nodes):
                weight = adj_matrix[i,j]
                if weight == 0:
                    continue

                edges_list.append( (str(i+1), str(j+1), {'weight': weight}) )
        
        return edges_list

    # Функция для определения позиции узла на основе уровня
    def node_pos(self, node):
        x = self.levels[node][0]
        y = -self.levels[node][1]
        return (x, y)

    def sort_straight_curved(self):
        straight_edges = []
        curved_edges = []
        for u, v, _ in self.edges_list:
            #Одинаковый y и располагаются дальше чем на 1 уровень
            if self.pos[u][1] == self.pos[v][1] and self.pos[v][0] - self.pos[u][0] > 1:
                curved_edges.append((u,v))
            else:
                straight_edges.append((u,v))
        
        return (straight_edges, curved_edges)

    def draw(self):
        fig, ax = plt.subplots()
        fig.set_figwidth(8.5)
        fig.set_figheight(8.5)

        #Узлы
        nx.draw_networkx_nodes(self.G, self.pos, ax=ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=ax)

        #Дуги
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edgelist=self.straight_edges)
        arc_rad = 0.35
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edgelist=self.curved_edges,
                            connectionstyle=f'arc3, rad = {arc_rad}')

        #Метки
        draw_networkx_curved_edge_labels(self.G, self.pos, ax=ax,
                                        edge_labels=self.curved_edge_labels, rotate=False,
                                        rad=arc_rad)
        nx.draw_networkx_edge_labels(self.G, self.pos, ax=ax, edge_labels=self.straight_edge_labels,
                                    rotate=False)

        self.picture_drawn = True
        return fig, ax


def main():
    '''
    Демо работы модуля
    '''
    # edges_list = [
    #     ('A', 'B', {'weight': 10}),
    #     ('A', 'C', {'weight': 20}),
    #     ('B', 'D', {'weight': 30}),
    #     ('A', 'D', {'weight': 20}),
    #     ('A', 'F', {'weight': 15}),
    #     ('C', 'E', {'weight': 40}),
    #     ('D', 'F', {'weight': 50}),
    #     ('E', 'F', {'weight': 60})
    # ]
    A = np.array([
        [0, 2, 5, 0, 3, 7],
        [0, 0, 0, 7, 9, 0],
        [0, 0, 0, 2, 1, 0],
        [0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0]
    ])

    # Определяем уровни узлов
    levels = {
        '1': (0, 0),
        '2': (1, 0), '3': (1, 1),
        '4': (2, 0), '5': (2, 1),
        '6': (3, 0)
    }

    #graphDrawer = GraphDrawer(edges_list=edges_list, levels=levels)
    graphDrawer = GraphDrawer(levels, adj_matrix=A)
    graphDrawer.draw()

    plt.show()


if __name__ == '__main__':
    main()
