# system packages
import os
# 3-party packages
import numpy as np
from matplotlib import pyplot as plt
# custom packages
from libs.signal_search import bio_signal_marker


if __name__ == '__main__':
    ## load abdo
    abdo_fs = 200
    abdo = np.random.randn(abdo_fs * 100)
    ## interpolate noise label
    annotation = np.zeros([len(abdo), ])
    ## data visuallization
    ts = range(len(abdo))
    data_visuallization_object = bio_signal_marker(ts, abdo, abdo, annotation,
                                                   abdo_fs, wheel_sec=1, screen_sec=10)
    data_visuallization_object.run()
