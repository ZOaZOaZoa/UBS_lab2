from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QComboBox
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPainter
import numpy as np
from GraphDrawer import GraphDrawer
from pathlib import Path

drawingAllowed = False

A_default = np.array([
    #  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17
    [  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2],
    [  0,  0,  0,  6,  4,  0,  5,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  3,  0,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0],
    [  2,  0,  0,  2,  0,  0,  0,  0,  5,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0],
    [  3,  4,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  3,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0],
], dtype=np.int16)

def input_data(dataGetter, graphOptimizer, A_table):
    dataGetter.catch_input_errors()
    graphOptimizer.init_from_matrix(A_table.matrix)

def add_nodes_to_combo(node_names: list, combo: QComboBox):
    combo.clear()
    combo.addItems(sorted(node_names, key=float))
    combo.setEnabled(True)

def draw_graph(graphOptimizer, A_table):
    graphDrawer = GraphDrawer(graphOptimizer.levels, A_table.matrix)
    fig, ax = graphDrawer.draw()
    Path('./tmp').mkdir(exist_ok=True)
    fig.savefig('./tmp/graph.svg', bbox_inches='tight', pad_inches=0)
    global drawingAllowed
    drawingAllowed = True

def main():
    Form, Window = uic.loadUiType("main_window.ui")
    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    
    from tableHandlers import TableHandler
    A_table = TableHandler(form.AMatrix, A_default)
    A_table.table.itemChanged.connect(TableHandler.floatValidateAndMessage)

    from userInfo import DataGetter
    dataGetter = DataGetter({'A': A_table})

    from GraphOptimizer import GraphOptimizer
    graphOptimizer = GraphOptimizer(A_table.matrix)
    
    form.dataInput.clicked.connect(lambda: (
        input_data(dataGetter, graphOptimizer, A_table),
        add_nodes_to_combo(graphOptimizer.levels.keys(), form.nodesCombo),
        draw_graph(graphOptimizer, A_table)
    ))

    def showSVG(event):
        global drawingAllowed
        if drawingAllowed:
            svgRenderer = QSvgRenderer('./tmp/graph.svg')
            painter = QPainter(form.svgView)
            svgRenderer.render(painter)

    form.svgView.paintEvent = showSVG
    window.show()
    app.exec()

if __name__ == '__main__':
    main()