from FileReaderWriter import FileReaderWriter
import json
import os

class JSONFileReaderWriter(FileReaderWriter):
    def read(self, filepath):
        filepath = os.path.join(os.path.dirname(__file__), filepath)
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
            print(data)
            return data

    def write(self, filepath, data):
        with open(filepath, "w") as write_file:
            json.dump(obj=data, fp=write_file)