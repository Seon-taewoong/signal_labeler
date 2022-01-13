import tkinter
import os
import numpy as np
import tkinter as tk
from tkinter import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, \
    QErrorMessage, QGraphicsPixmapItem, QGraphicsScene, QSlider
from PyQt5.QtGui import QPixmap, QMouseEvent, QWheelEvent
from PyQt5.QtCore import Qt
# matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.widgets import RectangleSelector
# pyqtgraph
import pyqtgraph as pg

class WindowClass(QMainWindow, uic.loadUiType('G:\github\signal_labeler\gui\\main_window_pyqtgraph.ui')[0]) :
    def __init__(self, data, fs,
                 window_sec=10, wheel_sec=1) :
        super().__init__()
        self.setupUi(self)
        # 파라메터 정의
        self.data = np.array(data)
        self.data_len = len(data)
        self.label = np.zeros(self.data.shape)
        self.events_array = []
        self.event_spans = []
        self.event_texts = []
        self.fs = fs
        self.window_sec = window_sec
        self.wheel_sec = wheel_sec
        # 위젯 정의
        self.signal_slider = signal_slider(self, Qt.Horizontal)
        self.fig_agg = None
        # 이벤트 연결
        self.actionLoadFile.triggered.connect(self.menu_btn_clicked_load_file)
        self.actionExit.triggered.connect(self.menu_btn_clicked_exit)
        self.pushButtonDeleteEvent.clicked.connect(self.btn_clicked_delete_event)
        self.EventProperty.doubleClicked.connect(self.double_click_list_view)
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
        # set data to graph
        self.fig_agg = pg.plot(self.data)
        self.fig_agg.setXRange(self.xlim_start, self.xlim_end, padding=0)
        self.graphLayout.addWidget(self.fig_agg)
        # set slider
        self.sliderLayout.addWidget(self.signal_slider)
        self.signal_slider.setRange(0, np.ceil((self.data_len / self.fs) / self.wheel_sec))

        # event connect
        self.fig_agg.scene().sigMouseClicked.connect(self.on_wheel_graph)

        # event connect
        # self.mouse_whell_evnet = self.fig.canvas.mpl_connect('scroll_event', self.on_wheel_graph)
        # self.rect_sel = RectangleSelector(self.ax_data, self.line_select_callback,
        #                                   drawtype='box', useblit=True, button=[1],
        #                                   minspanx=5, minspany=5, spancoords='pixels',
        #                                   interactive=True)
        # self.mouse_click_event = self.fig.canvas.mpl_connect('button_press_event', self.on_click_graph)
        # self.mouse_release_evnet = self.fig.canvas.mpl_connect('button_release_event', self.on_release_graph)

    # def line_select_callback(self, eclick, erelease):
    #     self.x1, self.y1 = eclick.xdata, eclick.ydata
    #     self.x2, y2 = erelease.xdata, erelease.ydata
    #     print(self.x1, self.x2)
    #
    # def on_click_graph(self, event):
    #     self.rect_sel.set_visible(True)
    #     print('click')

    # def on_release_graph(self, event):
    #     if str(event.button) == 'MouseButton.LEFT':
    #         print('L click')
    #
    #     elif str(event.button) == 'MouseButton.RIGHT':
    #         self.rect_sel.set_visible(False)
    #         tmp_span = self.ax_data.axvspan(self.x1, self.x2, color='#ccc')
    #         tmp_event_name = 'event'
    #         tmp_duration = np.round((self.x2 - self.x1) / self.fs, 2)
    #         tmp_event_number = len(self.events_array)
    #         tmp_event = {'event_number': tmp_event_number,
    #                      'event_name': tmp_event_name,
    #                      'start_idx': self.x1,
    #                      'end_idx': self.x2,
    #                      'duration': tmp_duration,
    #                      'span_y': self.y1}
    #         self.add_item_to_list_view(tmp_event)
    #         self.events_array.append(tmp_event)
    #         tmp_text = self.ax_data.text(self.x1, self.y1,
    #                                      'event number: {} \n event name: {} \n'.format(tmp_event_number, tmp_event_name) + ' duration: {} sec'.format(tmp_duration),
    #                                       family='sans-serif',
    #                                       size=10,
    #                                       horizontalalignment='center',
    #                                       verticalalignment='center')
    #         self.fig.canvas.draw()
    #         # append span and text plot
    #         self.event_spans.append(tmp_span)
    #         self.event_texts.append(tmp_text)
    #     else:
    #         pass
    #

    def on_wheel_graph(self):
        print('mouse whell~ ~')

    def on_wheel_slider(self):
        pass

    # def on_wheel_graph(self, event):
    #     if event.button == 'up':
    #         if self.xlim_end >= len(self.data):
    #             pass
    #         else:
    #             self.xlim_start += int(self.fs * self.wheel_sec)
    #             self.xlim_end += int(self.fs * self.wheel_sec)
    #             self.ax_data.set_xlim([self.xlim_start, self.xlim_end])
    #             self.fig.canvas.draw_idle()
    #     elif event.button == 'down':
    #         if self.xlim_start <= 0:
    #             pass
    #         else:
    #             self.xlim_start -= int(self.fs * self.wheel_sec)
    #             self.xlim_end -= int(self.fs * self.wheel_sec)
    #             self.ax_data.set_xlim([self.xlim_start, self.xlim_end])
    #             self.fig.canvas.draw_idle()
    #     else:
    #         pass

    def menu_btn_clicked_exit(self):
        print('exit')

    def menu_btn_clicked_load_file(self):
        # 사진 파일 경로 읽어오기
        self.load_file_path, self.load_file_path_type = QFileDialog.getOpenFileName()

        if self.load_file_path[-3::].lower() not in ['png', 'jpeg', 'jpg']:
            self.emsg_load_file.setWindowTitle('경고')
            self.emsg_load_file.showMessage('올바르지 않은 형식입니다. png 또는 jpeg 파일을 선택해 주세요.')
        else:
            self.listWidgetLoadFile.addItem(self.load_file_path)

    def btn_clicked_delete_event(self):
        # 그래프 이벤트 지우기
        events_num = len(self.events_array)
        if events_num > 0:
            delete_idx = self.EventProperty.currentRow()
            # 이벤트 데이터 지우기
            self.events_array.pop(delete_idx)
            # span, text graph, listview clear
            [tmp_event_spans.remove() for tmp_event_spans in self.event_spans]
            [tmp_event_texts.remove() for tmp_event_texts in self.event_texts]
            self.EventProperty.clear()
            self.event_spans.clear()
            self.event_texts.clear()
            # span, text graph, listview 넣기
            events_num_after = len(self.events_array)
            if events_num_after > 0:
                for tmp_dict_event_idx, tmp_dict_event in enumerate(self.events_array):
                    tmp_event_number = tmp_dict_event_idx
                    # 각 event dict 로 부터 그래프 그리는 특징 받아오기
                    tmp_event_name = tmp_dict_event['event_name']
                    tmp_start_idx = tmp_dict_event['start_idx']
                    tmp_end_idx = tmp_dict_event['end_idx']
                    tmp_duration = tmp_dict_event['duration']
                    tmp_span_y = tmp_dict_event['span_y']
                    # list view 채우기
                    event_str = 'event number: {}, event name: {}, duration: {} sec'.format(tmp_event_number,
                                                                                            tmp_event_name, tmp_duration)
                    self.EventProperty.addItem(event_str)
                    self.events_array[tmp_dict_event_idx]['event_number'] = tmp_dict_event_idx
                    # span 그리기
                    tmp_span = self.ax_data.axvspan(tmp_start_idx, tmp_end_idx, color='#ccc')
                    # text 그리기
                    tmp_text = self.ax_data.text(tmp_start_idx, tmp_span_y,
                                                 'event number: {} \n event name: {} \n'.format(tmp_event_number, tmp_event_name) + ' duration: {} sec'.format(tmp_duration),
                                                 family='sans-serif',
                                                 size=10,
                                                 horizontalalignment='center',
                                                 verticalalignment='center'
                                                 )
                    # append span and text plot
                    self.event_spans.append(tmp_span)
                    self.event_texts.append(tmp_text)
                # figure 다시 그리기
                # self.fig.canvas.draw()
            else:
                print('event not exist')

    def add_item_to_list_view(self, event_dict):
        # 새 특징를 리스트 뷰에 추가
        tmp_event_number = event_dict['event_number']
        tmp_event_name = event_dict['event_name']
        duration = event_dict['duration']
        event_str = 'event number: {}, event name: {}, duration: {} sec'.format(tmp_event_number, tmp_event_name, duration)
        self.EventProperty.addItem(event_str)

    def double_click_list_view(self):
        events_num = len(self.events_array)
        if events_num > 0:
            target_idx = self.EventProperty.currentRow()
            target_event = self.events_array[target_idx]
            x1 = target_event['start_idx']
            window = int((self.window_sec * self.fs) / 2)
            self.ax_data.set_xlim([x1 - window, x1 + window])
            # figure 다시 그리기
            self.fig.canvas.draw()
        else:
            print('event not exist')


class signal_slider(QSlider):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent

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


if __name__ == '__main__':
    data = np.random.randn(100000)
    app = QApplication(sys.argv)
    window = WindowClass(data, fs=4, window_sec=60, wheel_sec=10)
    window.show()
    app.exec_()
