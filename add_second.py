import os
import shutil
def add_second(file_name, lin):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    lines[1] = str(lin) + '\n'
    with open(file_name, "w") as file:
        for line in lines:
            file.write(line)
shutil.rmtree(os.getcwd() + '/__pycache__')

