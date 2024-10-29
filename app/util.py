import importlib
import importlib.util
import importlib.machinery
import inspect
import types
from pathlib import Path
import sys
import os




def get_class_instance_from( file_path=""):

    file_path = "C:\\Users\\bbart\\Desktop\\ml\\inzynierka\\code\\github-main\\network-stream-tool\\app\\demos\\connections_preprocess.py"
    module_name = os.path.basename(file_path)
    
    

    spec = importlib.util.spec_from_file_location(file_path, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)


    for name_local in dir(module):
        
        if inspect.isclass(getattr(module, name_local)):

            MysteriousClass = getattr(module, name_local)
           
           # checks if the mystery class is not abstract  
            if not inspect.isabstract(MysteriousClass):
                return MysteriousClass()
                
        