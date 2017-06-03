import os
import pathlib
import sys



if __name__ == '__main__':
    for filename in os.listdir(sys.argv[1]):
        if filename.endswith(".xml"):
            print("diff " + filename)
            print(os.system("diff -w "+sys.argv[1] + "/" + filename + " " + sys.argv[2] + "/" + filename))