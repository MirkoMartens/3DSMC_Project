import json
import os
import random


#class that saves the choosen answer-id from input, the question, the right answer and the other 2 answers and safe them in QeA.json
class SaverReader:

    def __init__(self, file_path):
        self.file_path = file_path
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(self.file_path, 'a') as f:
            f.write("[")



    def save_question(self, question, user_answer, right_answer, wrong_answer1, wrong_answer2):
        question = {'question': question, 'user_answer': user_answer, 'right_answer': right_answer, 'wrong_answer1': wrong_answer1, 'wrong_answer2': wrong_answer2}
        with open(self.file_path, 'a') as f:
            if f.tell() > 1:  # Check if the file is not empty
                f.write(",\n")

            json.dump(question, f, indent=4, separators=(",", ":"))

    def finish_json(self):
        with open(self.file_path, 'a') as f:
            f.write("]")

    # this method can get called at the end of the game and retrieves all saved questions and user answers
    def load_questions_from_file(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        return data
