import os

if __name__=="__main__":
    script_path = os.path.abspath(__file__)
    print(script_path)
    root_dir = os.path.dirname(script_path)
    print(root_dir)