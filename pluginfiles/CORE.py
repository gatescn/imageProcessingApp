from datetime import datetime

from pluginfiles import HelperLibrary
from pluginfiles.plugin import Plugin, Classifier
from pluginfiles.FeatureGrabber import Region_Props
from PIL import Image, ImageFile, UnidentifiedImageError
import sys
import time
import os
import csv


def save_images(image_map, output_directory):
    if len(image_map) > 0:
        for key in image_map:
            operation_output_directory = output_directory + "/" + key
            if os.path.isdir(operation_output_directory):
                now = datetime.now()
                d = now.strftime("%m%d%Y%H_%M_%S")
                operation_output_directory = output_directory + "/" + key + str(d)
            os.mkdir(operation_output_directory)
            processed_images = image_map[key]
            for i in range(len(processed_images)):
                im = Image.fromarray(processed_images[i])
                im.save(operation_output_directory + "/" + str(i), "bmp")
                print("image saved: " + str(i))
    else:
        print("no images to save")


class CORE_IM_PROCESSOR:
    plugin_def_directory = "/operationDefinitionRepository/"
    app_directory = os.path.dirname(__file__)
    # creates map to hold all processed images by this individual filter.
    modified_collection = {}
    batch_start_time = None
    optimizeRun = False

    def __init__(self):
        pass

    def run(self):
        self.batch_start_time = time.time()
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        # get config params for program
        raw_directory, output_directory, operations = HelperLibrary.read_config()
        # check if each filter has a definition file associated, if not, stop the program because it will cause error
        # later
        # if not HelperLibrary.checkForDefinitionFiles(self.app_directory, self.plugin_def_directory, operations):
        #     print("please ensure definition file is present for each Plugin used and try again")
        #     sys.exit()
        #     # o is the current operation
        for o in operations:
            print("Current Plugin: " + o)
            plugin = HelperLibrary.get_plugin(o)
            # get the plugin's definition file. The definition file contains the params for the filter.
            plugin_config_path = os.path.join(self.app_directory + self.plugin_def_directory + o + "Definition.config")
            self.run_plugin(plugin, plugin_config_path, raw_directory)
            if plugin.is_image_save_required(self):
                save_images(self.modified_collection, output_directory)
            if plugin.is_file_save_required(self):
                csv_output_location = os.path.join(output_directory, "csv_reports")
                props_data_collection = []
                for key in self.modified_collection:
                    props_data_collection.append(self.modified_collection[key])
                self.write_csv_file(key, csv_output_location, props_data_collection)

    def run_plugin(self, plugin, plugin_config_path, raw_directory):
        file_directory_contents = os.listdir(raw_directory)
        if len(file_directory_contents) > 0:
            for folder in file_directory_contents:
                if not str(folder) == ".DS_Store":
                    folder_directory = os.path.join(raw_directory, str(folder))
                    result_collection = self.iterate_through_files(folder, plugin, plugin_config_path, folder_directory)
                    self.modified_collection[folder] = result_collection
                    if self.optimizeRun:
                        break

    def iterate_through_files(self, folder_name, plugin, plugin_config_path, raw_directory):
        file_index = 0
        files = os.listdir(raw_directory)
        file_total = len(files)
        results = []

        # iterate through each file at the location specified in the configuration
        for file in files:
            filepath = raw_directory + "/" + file
            # opens the raw image
            try:
                raw_img = Image.open(filepath).convert('L')
            except UnidentifiedImageError:
                print("Folder contains non image, please remove file named:" + file + " and rerun")
                sys.exit()
            if issubclass(plugin, Plugin):
                self.optimizeRun = False
                # pass image, run filters
                plugin_results = plugin.run(plugin, raw_img, folder_name, plugin_config_path)
                results.append(plugin_results)
                # increment file index
                file_index = file_index + 1

                # prints the current filter being used along with the file being filtered
                print(str(file_index) + "of" + str(file_total - 1))
            if issubclass(plugin, Classifier):
                self.optimizeRun = True
                plugin_results = plugin.run(plugin, plugin_config_path)
                break
        return results

    def write_csv_file(self, title, csv_output_location, data_collection):
        header = ["area", "perimeter", "roundness", "label"]
        temp = str(title) + ".csv"
        if not os.path.exists(csv_output_location):
            os.mkdir(csv_output_location)
        csv_title = os.path.join(csv_output_location, temp)
        rows = []
        for data_list in data_collection:
            for props in data_list:
                if isinstance(props, Region_Props):
                    row = props.get_data_row()
                    rows.append(row)
        with open(csv_title, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
