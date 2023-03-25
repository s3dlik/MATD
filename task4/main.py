import requests
import os
import string
import unicodedata
import re

class PreText:
    def __init__(self) -> None:
        self.path = os.getcwd() + "\gutenberg"


    def download(self, limit=100):
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        base_url = "https://www.gutenberg.org/files/"

        i = 1
        num = 0
        while num < limit:    
            book = str(i) + "-0.txt"
            extended_url = base_url + str(i) + "/" + book

            r = requests.get(extended_url)
            content = str(r.content)
            if not "<!DOCTYPE" in content:            
                open("gutenberg/" + book, 'wb').write(r.content)
                num += 1

            i += 1
            
    def handle_file(self):
        pathProcessed = os.getcwd() + "\gutenbergProc"
        
        if not os.path.exists(pathProcessed):
            os.mkdir(pathProcessed)
        
        for file in os.listdir(self.path):
            text, file = self.open_file(file)
            text_split = text.split(' ')
            if os.path.isfile(pathProcessed + "/" + file):
                os.remove(pathProcessed + "/" + file)
            
            with open(pathProcessed + "/" + file, "w") as f:
                for word in text_split:
                    f.write(word + '\n')
        
        
        
        

                
    def open_file(self, file):
        output_str = ''

        with open(self.path + "/" + file, 'r', encoding="iso-8859-15") as f:
            text = f.read()

        text = text.lower()
        text_reg = re.sub(r'[^a-zA-Z0-9\s]+', '', text)
        text_split = text_reg.split()
        text_str = ' '.join(text_split)
        text_norm = unicodedata.normalize('NFD', text_str)
        text_enc = text_norm.encode('ascii', 'ignore')
        text_dec = text_enc.decode('utf-8')

        
        return text_dec, file

if __name__ == '__main__':
    pretext = PreText()
    #pretext.download()
    pretext.handle_file()
    