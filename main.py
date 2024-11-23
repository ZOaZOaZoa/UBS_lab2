from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QScrollArea
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QRegularExpressionValidator, QPainter
import numpy as np


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
    
    form.dataInput.clicked.connect(lambda: dataGetter.catch_input_errors())

    # def showSVG(event):
    #     svgRenderer = QSvgRenderer('out.svg')
    #     painter = QPainter(form.svgView)
    #     svgRenderer.render(painter)

    # form.svgView.paintEvent = showSVG
    window.show()
    app.exec()

if __name__ == '__main__':
    main()