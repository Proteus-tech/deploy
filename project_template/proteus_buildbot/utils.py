from importlib import import_module
import os

def load_modules(parent, modules):
    for module in modules:
        import_module(parent.__name__ + '.' + module)

def list_modules(module):
    path = module.__path__[0]
    return set([ module_name(sub_module)
                 for sub_module in os.listdir(path) 
                 if module_name(sub_module) ])

def module_name(module):
    if '.' in module:
        extension = ('.py', '.pyc')
        if module.endswith(extension):
            module_name = os.path.splitext(module)[0]
            if module_name == '__init__':
                module_name = None
        else:
            module_name = None
        return module_name
    else:
        return module 

