"""
Copyright (c) 2025, Auorui.
All rights reserved.

This module is used for reading and displaying images and videos. The image contains
OpenCV and PIL, and the loading method for the video is OpenCV.
"""
from .imvision import bgr_read, imwriter, display, url2image, stacked2image, \
    StackedImagesV1, StackedImagesV2, imattributes
from .pilvision import rgb_read, imshowplt, StackedpltV1, StackedpltV2, matplotlib_patch
from .videovision import VideoCap, Mp4toGif, FindColor, DetectImageColor, DetectVideoColor