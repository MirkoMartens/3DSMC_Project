import json
import os
import random



class Questions:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_questions()

    def load_questions(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data
    
    def get_question(self):
        return self.data[random.randint(0, len(self.data) - 1)]
    