
import csv
import time
import pandas as pd
import util
import os

class Main:

    def __init__(self, 
                 streaming_path : str = "", 
                 batch_path : str = "", 
                 dataset_path: str = "",
                 preprocess_path : str = ""):
        # self.__streaming_path = streaming_path
        # self.__batch_path = batch_path
        # self.__preprocess_path = preprocess_path
        self.__include_preprocess = not preprocess_path
        self.__dataset = dataset_path

        if self.__include_preprocess:
            self._preprocess = util.get_class_instance_from(preprocess_path)
        
        self.__batch = util.get_class_instance_from(batch_path)
        self.__stream = util.get_class_instance_from(streaming_path)

        self.__avg_property_time_per_edge = []
        self.__avg_preprocessing_time_per_edge = []
        self.__number_of_processed_edges = 0


    # @property
    # def batch_path(self):
    #     return self.__batch_path

    # @property
    # def streaming_path(self):
    #     return self.__streaming_path
    
    # @property
    # def preprocess_path(self):
    #     return self.__preprocess_path


    # @batch_path.setter
    # def batch_path(self, path:str):
    #     self.__batch_path = path

    # @streaming_path.setter
    # def streaming_path(self, path:str):
    #     self.__streaming_path = path

    # @preprocess_path.setter
    # def preprocess_path(self, path:str):
        self.__preprocess_path = path


    def run(self):
        columns = ["", "company","line","departure_time","arrival_time","start","end",
                                              "start_lat","start_lon","end_lat","end_lon"]
        with open(self.__dataset,encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=columns) # , is the default delimiter
            next(reader, None)

            for row in reader:
                self.__number_of_processed_edges +=1

                if self.__include_preprocess:
                    preprocess_start = time.time()
                    # processssss
                    preprocess_end = time.time()
                    preprocess_duration += preprocess_end - preprocess_start
                    self.__avg_preprocessing_time_per_edge.append(
                        preprocess_duration/self.number_of_processed_edges)
                
                property_start = time.time()
                self.__stream(row)
                property_end = time.time()
                property_calculation_duration += property_end - property_start
                self.__avg_property_time_per_edge.append(
                    property_calculation_duration/self.number_of_processed_edges)
            

            if os.path.basename(self.__dataset).endswith('.csv'):
                self.__batch.calculate_property(pd.read_csv(self.__dataset))

            elif os.path.basename(self.__dataset).endswith('.mtx'):
                # TODO: convert mtx to dataframe 
                pass
            
            else:
                # TODO: how to make it possible to batch process when the best we got is some text file 
                # batch processing atm requires a pandas DataFrame 
                pass

            
        return self.__stream.submit_results(), self.__batch.submit_results(), self.__avg_property_time_per_edge, self.__avg_preprocessing_time_per_edge




if __name__ == "__main__":
    obj = Main()
    util.get_class_instance_from()
    # obj.run()

