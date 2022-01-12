import tkinter
import os
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from PyQt5 import uic
# from PyQt5 import QtGui
# from PyQt5.QtCore import QCoreApplication
import cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, \
    QErrorMessage, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtGui import QPixmap
# matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import RectangleSelector


class WindowClass(QMainWindow, uic.loadUiType('G:\github\signal_labeler\gui\\main_window.ui')[0]) :
    def __init__(self, data, fs,
                 window_sec=10, wheel_sec=1) :
        super().__init__()
        self.setupUi(self)
        # 파라메터 정의
        self.data = np.array(data)
        self.label = np.zeros(self.data.shape)
        self.events_array = []
        self.fs = fs
        self.window_sec = window_sec
        self.wheel_sec = wheel_sec
        # 이벤트 연결
        self.actionLoadFile.triggered.connect(self.btn_clicked_load_file)
        self.actionExit.triggered.connect(self.btn_clicked_exit)
        self.pushButtonDeleteLoadFile.clicked.connect(self.btn_clicked_delete_load_file)
        self.pushButtonViewImageLoadFile.clicked.connect(self.btn_clicked_view_image_load_file)
        self.listWidgetLoadFile.clicked.connect(self.view_property_load_file)

        # 메세지 창
        self.emsg_load_file = QErrorMessage(self)
        self.resizing_not_chosen_file = QErrorMessage(self)
        # 리스트 뷰
        # 그래픽 뷰
        self.xlim_start = 0
        self.xlim_end = self.fs * self.window_sec
        self.ax_data = None
        self.ax_label = None
        self.init_graph()

    def init_graph(self):
        self.fig = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax_data = self.fig.add_subplot(111)
        # set data
        self.canvas_data, = self.ax_data.plot(self.data)
        # set title
        self.ax_data.set_title('Signal')
        # set ticks
        # set init x axis limitation
        self.ax_data.set_xlim([self.xlim_start, self.xlim_end])
        # make widget
        fig_agg = FigureCanvas(self.fig)
        self.LayoutGraph.addWidget(fig_agg)
        # event connect
        self.mouse_whell_evnet = self.fig.canvas.mpl_connect('scroll_event', self.on_wheel)
        self.rect_sel = RectangleSelector(self.ax_data, self.line_select_callback,
                                          drawtype='box', useblit=False, button=[1],
                                          minspanx=5, minspany=5, spancoords='pixels',
                                          interactive=True)
        self.mouse_click_event = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.mouse_release_evnet = self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def line_select_callback(self, eclick, erelease):
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        self.x2, y2 = erelease.xdata, erelease.ydata
        # rect = plt.Rectangle((min(self.x1, self.x2), min(y1, y2)), np.abs(self.x1 - self.x2), np.abs(y1 - y2))
        print(self.x1, self.x2)

    def on_click(self, event):
        self.rect_sel.set_visible(True)
        print('click')

    def on_release(self, event):
        if str(event.button) == 'MouseButton.LEFT':
            print('L click')

        elif str(event.button) == 'MouseButton.RIGHT':
            self.rect_sel.set_visible(False)
            self.ax_data.axvspan(self.x1, self.x2, color='#ccc')
            tmp_event_name = 'event'
            tmp_duration = np.round((self.x2 - self.x1) / self.fs, 2)
            tmp_event = {'event_name': tmp_event_name,
                         'start_idx': self.x1,
                         'end_idx': self.x2,
                         'duration': tmp_duration}
            self.events_array.append(tmp_event)
            self.ax_data.text(self.x1, self.y1, 'event name: {} \n'.format(tmp_event_name) + ' duration: {}'.format(tmp_duration), fontsize=10)
            self.fig.canvas.draw()
        else:
            pass

    def on_wheel(self, event):
        if event.button == 'up':
            if self.xlim_end >= len(self.data):
                print('wheel up pass')
            else:
                self.xlim_start += int(self.fs * self.wheel_sec)
                self.xlim_end += int(self.fs * self.wheel_sec)
                self.ax_data.set_xlim([self.xlim_start, self.xlim_end])
                self.fig.canvas.draw()
                print('wheel up')
        elif event.button == 'down':
            if self.xlim_start <= 0:
                print('wheel down pass')
            else:
                self.xlim_start -= int(self.fs * self.wheel_sec)
                self.xlim_end -= int(self.fs * self.wheel_sec)
                self.ax_data.set_xlim([self.xlim_start, self.xlim_end])
                self.fig.canvas.draw()
                print('wheel down')
        else:
            pass

    def btn_clicked_exit(self):
        print('exit')

    def btn_clicked_load_file(self):
        # 사진 파일 경로 읽어오기
        self.load_file_path, self.load_file_path_type = QFileDialog.getOpenFileName()

        if self.load_file_path[-3::].lower() not in ['png', 'jpeg', 'jpg']:
            self.emsg_load_file.setWindowTitle('경고')
            self.emsg_load_file.showMessage('올바르지 않은 형식입니다. png 또는 jpeg 파일을 선택해 주세요.')
        else:
            self.listWidgetLoadFile.addItem(self.load_file_path)

    def btn_clicked_delete_load_file(self):
        # 특징 데이터를 특징 리스트뷰에서 삭제
        self.delete_property_load_file()
        # 로드 된 파일의 경로를 삭제
        delete_idx = self.listWidgetLoadFile.currentRow()
        self.listWidgetLoadFile.takeItem(delete_idx)
        # 현재 QgraphicView의 이미지 삭제
        try:
            self.scene.clear()
        except:
            pass

    def delete_property_load_file(self):
        # 이전 데이터를 리스트뷰에서 지우기
        self.listWidgetLoadFileProperty.takeItem(0)
        self.listWidgetLoadFileProperty.takeItem(0)

    def btn_clicked_view_image_load_file(self):
        try:
            current_path = self.listWidgetLoadFile.currentItem().text()
        except:
            return -1

        if current_path is None:
            return -1
        else:
            # 선택한 로드파일 시각화
            self.scene = QGraphicsScene(self)
            pixmap = QPixmap(current_path)
            item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(item)
            # self.graphicsView.setScene(self.scene)

    def view_property_load_file(self):
        # 이전 데이터를 리스트뷰에서 지우기
        self.delete_property_load_file()
        # 새 특징를 리스트 뷰에 추가
        path = self.listWidgetLoadFile.currentItem().text()
        img_array = np.fromfile(path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        img_shape = img.shape
        img_raw_volume = os.path.getsize(path)

        image_size = 'image size: {} x {}'.format(img_shape[0], img_shape[1])
        image_volume = 'image raw volume: {} bytes'.format(img_raw_volume)

        self.listWidgetLoadFileProperty.addItem(image_size)
        self.listWidgetLoadFileProperty.addItem(image_volume)

    def view_property_result_file(self):
        pass

if __name__ == '__main__':
    data = np.random.randn(1000)
    app = QApplication(sys.argv)
    window = WindowClass(data, fs=10)
    window.show()
    app.exec_()
