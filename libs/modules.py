import sys
from PyQt5.QtWidgets import QSlider, QApplication
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter
from matplotlib.widgets import RectangleSelector


class signal_slider(QSlider):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.event = None

    def wheelEvent(self, e):
        current_pos = self.value()
        if e.angleDelta().y() > 0:

            if current_pos < self.maximum():
                current_pos += 1
                self.setValue(current_pos)
                self.parent.fig_agg.setXRange(int(current_pos * self.parent.fs * self.parent.wheel_sec),
                                              int(current_pos * self.parent.fs * self.parent.wheel_sec) + int(
                                                  self.parent.window_sec * self.parent.fs))

        elif e.angleDelta().y() < 0:

            if current_pos > self.minimum():
                current_pos -= 1
                self.setValue(current_pos)
                self.parent.fig_agg.setXRange(int(current_pos * self.parent.fs * self.parent.wheel_sec),
                                              int(current_pos * self.parent.fs * self.parent.wheel_sec) + int(
                                                  self.parent.window_sec * self.parent.fs))
        else:
            pass

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        current_pos = self.value()
        self.parent.fig_agg.setXRange(int(current_pos * self.parent.fs * self.parent.wheel_sec),
                                      int(current_pos * self.parent.fs * self.parent.wheel_sec) + int(
                                          self.parent.window_sec * self.parent.fs))

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        current_pos = self.value()
        self.parent.fig_agg.setXRange(int(current_pos * self.parent.fs * self.parent.wheel_sec),
                                      int(current_pos * self.parent.fs * self.parent.wheel_sec) + int(
                                          self.parent.window_sec * self.parent.fs))


class signal_plot(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.begin, self.destination = QPoint(), QPoint()
        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.white)

    def mousePressEvent(self, ev):
        super().mousePressEvent(ev)
        print('mouse press')

        if ev.buttons() & Qt.LeftButton:
            print('Point 1')
            self.begin = ev.pos()
            self.destination = self.begin
            self.update()

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        print('mouse release {}'.format(ev.pos()))

        if ev.button() & Qt.LeftButton:
            print('draw rect')
            # rect = QRect(self.begin, self.destination)
            # painter = QPainter(self.pix)
            # painter.drawRect(rect.normalized())
            self.event = ev
            self.begin, self.destination = QPoint(), QPoint()
            self.update()
        #
        # painter = QPainter(self)
        # painter.drawPixmap(QPoint(), self.pix)
        # if not self.begin.isNull() and not self.destination.isNull():
        #     rect = QRect(self.begin, self.destination)
        #     painter.drawRect(rect.normalized())

    def mouseMoveEvent(self, ev):
        if ev.buttons() & Qt.LeftButton:
            print('{}'.format(ev.pos()))
            self.destination = ev.pos()

            # begin_x, begin_y = self.begin.x(), self.begin.y()
            # des_x, des_y = self.destination.x(), self.destination.y()
            # w, h = des_x - begin_x, des_y - begin_y
            # r1 = pg.QtGui.QGraphicsRectItem(begin_x, begin_y, w, h)
            # r1.setPen(pg.mkPen(None))
            # r1.setBrush(pg.mkBrush('r'))
            # self.addItem(r1)

            self.update()


if __name__ == '__main__':
    data = [0,1,2,3,4]
    r1 = pg.QtGui.QGraphicsRectItem(0, 0, 0.4, 1)
    r1.setPen(pg.mkPen(None))
    r1.setBrush(pg.mkBrush('r'))
    app = QApplication(sys.argv)
    my_custom_plot_widget = signal_plot()
    my_custom_plot_widget.plot(data, data)
    my_custom_plot_widget.addItem(r1)
    my_custom_plot_widget.show()
    app.exec_()
