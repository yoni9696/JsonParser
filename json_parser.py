class StreamReader(object):
    def __init__(self,path):
        self.file = self.open_file(path)

    def open_file(self,path):
        return open(path,'r')

    def read_next_line(self):
        return next(self.file)

    def close_file(self):
        return self.file.close()

class JsonParser(object):

    def __init__(self,json_path):
        self.st = StreamReader(json_path)
        self.records_counter = 0
        self.logs_counter = 0
        self.success_counter = 0
        self.actions = {}

    def is_valid_record(self,line):
        return line.find(':') >=0

    def get_record_value(self,line):
        val = line[line.find(':'):]
        return val[val.find('"')+1:-3]

    def add_action(self,action):
        if self.actions.get(action):
            self.actions[action] +=1
        else:
            self.actions[action] = 1

    def parse_json(self,line):
        if line.find('action') >=0 :
            action = self.get_record_value(line)
            self.add_action(action)

        if line.find('result') >=0 :
            if self.get_record_value(line) == 'success':
                self.success_counter +=1

    def read_all(self):
        line = self.st.read_next_line()
        try:
            while True:
                line = self.find_next_json(line)
        except StopIteration:
            self.st.close_file()

    def find_next_json(self,line):
        while line.find('{') >= 0:
            line = self.st.read_next_line()
            while line.find('}') == -1:
                while not self.is_valid_record(line):
                    line = self.st.read_next_line()
                self.records_counter +=1
                self.parse_json(line)
                line = self.st.read_next_line()

            self.logs_counter += 1
        return self.st.read_next_line()


