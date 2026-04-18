from FileReaderWriter import FileReaderWriter
from CSVFileReaderWriter import CSVFileReaderWriter
from JSONFileReaderWriter import JSONFileReaderWriter

# Test the defult class
df = FileReaderWriter()
df.read()
df.write()

# Test the polymorphic methods
c = CSVFileReaderWriter()
c.read("sample.csv")
c.write(filepath="sample2.csv", data=["Hello", "World"])
        
j = JSONFileReaderWriter()
j.read("sample.json")
j.write(data = ['foo', {'bar': ('baz', None, 1.0, 2)}], filepath="sample2.json")