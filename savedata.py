import os

class SaveData:
    def __init__(self):
        self.save_file_path = os.path.join(os.getenv("APPDATA"), "OskuDev", "ScreriTetris")
        self.save_file_name = "save.dat"

        if not os.path.exists(self.save_file_path):
            os.makedirs(self.save_file_path)

    def save(self, score):
        with open(os.path.join(self.save_file_path, self.save_file_name), "w") as file:
            file.write(self.cipher("score: " + str(score)))

    def load(self):
        try:
            with open(os.path.join(self.save_file_path, self.save_file_name), "r") as file:
                encrypted_score = file.read()
                return int(self.decipher(encrypted_score).lstrip(':'))
        except FileNotFoundError:
            return 0

    def cipher(self, text):
        result = ""
        for char in text:
            result += chr(ord(char) + 10)
        return result

    def decipher(self, text):
        result = ""
        for char in text:
            result += chr(ord(char) - 10)
        return result
