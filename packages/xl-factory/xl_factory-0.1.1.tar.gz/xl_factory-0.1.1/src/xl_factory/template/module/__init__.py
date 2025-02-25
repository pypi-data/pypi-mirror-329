import os 
import copier


def copy(dst_path, data=None):
    copier.run_copy(os.path.dirname(os.path.abspath(__file__)), dst_path, data)

