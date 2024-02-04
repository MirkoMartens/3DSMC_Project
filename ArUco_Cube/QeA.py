import json
import os
import random


#class that saves the choosen answer-id from input, the question, the right answer and the other 2 answers and safe them in QeA.json
class SaverReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_questions()

    def load_questions(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data

    def get_question(self):
        return self.data[random.randint(0, len(self.data) - 1)]

    def save_question(self, question, answer, right_answer, wrong_answer1, wrong_answer2):
        self.data.append({'question': question, 'answer': answer, 'right_answer': right_answer, 'wrong_answer1': wrong_answer1, 'wrong_answer2': wrong_answer2})
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
        self.data = self.load_questions()
        return self.data
    
    def get_all_questions(self):
        return self.data
    
    #erase everything in the file

    def erase_all(self):
        with open(self.file_path, 'w') as f:
            f.write("[]")
        self.data = self.load_questions()
        return self.data
    
    
    
    