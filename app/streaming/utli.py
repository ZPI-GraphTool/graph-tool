import importlib
import importlib.util
import importlib.machinery
import inspect
import types
from pathlib import Path
import sys

module_name = "connections_preprocess.py"
file_path = "C:\\Users\\bbart\\Desktop\\ml\\inzynierka\\code\\github-main\\network-stream-tool\\app\\demos"
# spec = importlib.util.spec_from_file_location(module_name, file_path)
loader = importlib.machinery.SourceFileLoader(module_name, file_path)
mod = types.ModuleType(loader.name)
loader.exec_module(mod)





# path_pyfile = Path('\..\demos\connections_preprocess.py')
# path_pyfile = Path("C:\\Users\\bbart\\Desktop\\ml\\inzynierka\\code\\github-main\\network-stream-tool\\app\\demos\\connections_preprocess.py")

mysterious = importlib.import_module(module)

for name_local in dir(mysterious):
    if inspect.isclass(getattr(mysterious, name_local)):
        print(f'{name_local} is a class')
        MysteriousClass = getattr(mysterious, name_local)
        mysterious_object = MysteriousClass()
        mysterious_object.create_edge_from("Hell")