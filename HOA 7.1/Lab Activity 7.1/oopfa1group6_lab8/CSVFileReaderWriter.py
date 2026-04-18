from FileReaderWriter import FileReaderWriter
import csv
import os  

class CSVFileReaderWriter(FileReaderWriter):
    def read(self, filepath):
        filepath = os.path.join(os.path.dirname(__file__), filepath)
        with open(filepath, newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in data:
                print(row)
            return data

    def write(self, filepath, data):
        with open(filepath, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(data)