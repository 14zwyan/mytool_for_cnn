# config.py
import os.path

# gets home dir cross platform
HOME = os.path.expanduser("~")

# for making bounding boxes pretty
COLORS = ((255, 0, 0, 128), (0, 255, 0, 128), (0, 0, 255, 128),
          (0, 255, 255, 128), (255, 0, 255, 128), (255, 255, 0, 128))

MEANS = (104, 117, 123)

# SSD300 CONFIGS
voc = {
    'num_classes': 21,
    'lr_steps': (80000, 100000, 120000),
    'max_iter': 120000,
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'min_dim': 300,
    'steps': [8, 16, 32, 64, 100, 300],
    'min_sizes': [30, 60, 111, 162, 213, 264],
    'max_sizes': [60, 111, 162, 213, 264, 315],
    'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
    'variance': [0.1, 0.2],
    'clip': True,
    'name': 'VOC',
}

coco = {
    'num_classes': 201,
    'lr_steps': (280000, 360000, 400000),
    'max_iter': 400000,
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'min_dim': 300,
    'steps': [8, 16, 32, 64, 100, 300],
    'min_sizes': [21, 45, 99, 153, 207, 261],
    'max_sizes': [45, 99, 153, 207, 261, 315],
    'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2], [2]],
    'variance': [0.1, 0.2],
    'clip': True,
    'name': 'COCO',
}

#SSD321 CONFIGS
voc_321 = {
    'num_classes': 21,
    'lr_steps': (80000, 100000, 120000),
    'max_iter': 120000,
    'feature_maps': [40, 20, 10, 5, 3, 1],
    'min_dim': 320,
    'steps': [8, 16, 32, 64, 64, 321],
    'min_sizes': [32, 64, 121, 179, 237, 295],
    'max_sizes': [64, 121, 179,237, 295, 353],
    'aspect_ratios': [[1.6,2.0,3.0], [1.6,2.0,3.0], [1.6,2.0,3.0], [1.6,2.0,3.0],[1.6,2.0,3.0], [1.6,2.0,3.0]],
    'variance': [0.1, 0.2],
    'clip': True,
    'name': 'VOC_321',
}

#for resnet50
voc_res50 = {
    'num_classes': 21,
    'lr_steps': (40000, 500000, 60000),
    'max_iter': 65000,
    'feature_maps': [38, 19, 10, 5, 3, 1],
    'min_dim': 300,
    'steps': [8, 16, 32, 64, 100, 300],
    'min_sizes': [30, 60, 114, 168, 222, 276],
    'max_sizes': [60, 114, 168, 222, 276, 330],
    'aspect_ratios': [[2], [2, 3], [2, 3], [2, 3], [2,3], [2,3]],
    'variance': [0.1, 0.2],
    'clip': True,
    'name': 'VOC',
}
