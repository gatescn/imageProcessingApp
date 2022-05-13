import math

import numpy as np
from skimage.color import label2rgb
import matplotlib.patches as mpatches
from skimage.measure import label, regionprops, find_contours
import matplotlib.pyplot as plt

from pluginfiles.plugin import Plugin


class Region_Props:
    label = None
    area = None
    perimeter = None
    roundness = None
    eccentricity = None
    name = None

    def __init__(self, filename, label_val, area_val, perimeter_val, eccentricity, roundness_val):
        self.name = filename
        self.label = str(self.name) + "-" + str(label_val)
        self.area = area_val
        self.perimeter = perimeter_val
        self.roundness = roundness_val
        self.eccentricity = eccentricity

    def get_data_row(self):
        data_row = [self.area, self.perimeter, self.eccentricity, self.roundness, self.name]
        return data_row

    def get_header_row(self):
        header_row = ["area", "perimeter", "eccentricity", "roundness", "label"]
        return header_row


def calculate_roundness(area, perimeter):
    p_squared = perimeter * perimeter
    denominator = 4 * math.pi * area
    if denominator != 0:
        radius = p_squared / denominator
    else:
        radius = 0
    return radius


def find_features(filename, labeled_image):
    region_properties = []
    regions = regionprops(labeled_image)

    for r in regions:
        label_val = r.label
        area = r.area
        perimeter = r.perimeter
        eccentricity = r.eccentricity
        roundness = calculate_roundness(area, perimeter)
        prop = Region_Props(filename, label_val, area, perimeter, eccentricity, roundness)
        region_properties.append(prop)

    return region_properties, regions


def label_image(orig_image):
    labeled_image = label(orig_image)
    return labeled_image


def view_regions(regions, labeled_image, image):
    image_label_overlay = label2rgb(labeled_image, image=image, bg_label=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)

    for region in regions:
        minr, minc, maxr, maxc = region.bbox
        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                  fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)

    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


class FeatureGrabber(Plugin):
    labeled_img = None
    region_properties = []

    def run(self, raw_img, filename, definition_path):
        orig_image = np.array(raw_img)
        self.labeled_img = label_image(orig_image)
        self.region_properties, regions = find_features(str(filename), self.labeled_img)
        max_round_region = self.pick_max_roundness(self)
        # view_regions(regions, self.labeled_img, orig_image)
        return max_round_region

    def pick_max_roundness(self):
        val = 0
        max_prop = None
        for props in self.region_properties:
            if props.roundness > val:
                val = props.roundness
                max_prop = props
        return max_prop

    def is_image_save_required(self):
        return False

    def is_file_save_required(self):
        return True
