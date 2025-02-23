import os

class Importer:
    def __init__(self):
        pass

    def read_goonfile(self, filename):
        if self.is_goonfile(filename):
            return open(filename, "r").read()
        else:
            print("ERROR!!! NOT A GOONER FILE")
            exit()

    def is_goonfile(self, filename):
        file_ext = os.path.splitext(filename)[1]

        return file_ext == ".goon"