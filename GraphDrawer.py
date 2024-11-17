import networkx as nx
import matplotlib.pyplot as plt
from my_networkx import draw_networkx_curved_edge_labels

class GraphDrawer:
    def __init__(self, edges_list, levels):
        self.G = nx.DiGraph()
        self.G.add_edges_from(edges_list)

        self.edges_list = edges_list
        self.levels = levels
        
        self.pos = {n: self.node_pos(n) for n in self.G.nodes()}
        self.straight_edges, self.curved_edges = self.sort_straight_curved()
        self.edge_weights = nx.get_edge_attributes(self.G, 'weight')

        self.curved_edge_labels = {edge: self.edge_weights[edge] for edge in self.curved_edges}
        self.straight_edge_labels = {edge: self.edge_weights[edge] for edge in self.straight_edges}

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

        #Узлы
        nx.draw_networkx_nodes(self.G, self.pos, ax=ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=ax)

        #Дуги
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edgelist=self.straight_edges)
        arc_rad = 0.25
        nx.draw_networkx_edges(self.G, self.pos, ax=ax, edgelist=self.curved_edges,
                            connectionstyle=f'arc3, rad = {arc_rad}')

        #Метки
        draw_networkx_curved_edge_labels(self.G, self.pos, ax=ax,
                                        edge_labels=self.curved_edge_labels, rotate=False,
                                        rad=arc_rad)
        nx.draw_networkx_edge_labels(self.G, self.pos, ax=ax, edge_labels=self.straight_edge_labels,
                                    rotate=False)

        return fig, ax


def main():
    edges_list = [
        ('A', 'B', {'weight': 10}),
        ('A', 'C', {'weight': 20}),
        ('B', 'D', {'weight': 30}),
        ('A', 'D', {'weight': 20}),
        ('C', 'E', {'weight': 40}),
        ('D', 'F', {'weight': 50}),
        ('E', 'F', {'weight': 60})
    ]

    # Определяем уровни узлов
    levels = {
        'A': (0, 0),
        'B': (1, 0), 'C': (1, 1),
        'D': (2, 0), 'E': (2, 1),
        'F': (3, 0)
    }

    graphDrawer = GraphDrawer(edges_list, levels)
    graphDrawer.draw()

    plt.show()


if __name__ == '__main__':
    main()
