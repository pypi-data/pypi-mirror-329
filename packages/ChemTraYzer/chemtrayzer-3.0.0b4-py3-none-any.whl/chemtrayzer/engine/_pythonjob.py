"""
Contains the Python code that is executed as a job when submitting an instance
of PythonJob. It unpickles the callable object that was pickled by the job and
execues it.
"""

import importlib.util
import logging
import pickle
import traceback


class CallableUnpickler(pickle.Unpickler):
    '''used to unpickle the callable from a pickle file

    :param callable_path: file in which the callable is defined
    '''

    def __init__(self, file, *,
                 callable_path: str,
                 **kwargs) -> None:
        super().__init__(file, **kwargs)

        self.callable_file = callable_path

    @staticmethod
    def get_nested_attr(module_obj, qualified_name):
        '''retrieves an attribute from a module even if it is nested'''
        attributes = qualified_name.split('.')
        current_attribute = module_obj

        for attr in attributes:
            try:
                current_attribute = getattr(current_attribute, attr)
            except AttributeError as err:
                raise AttributeError(f"Attribute '{attr}' not found in "
                                     f"'{module_obj.__name__}' under name"
                                     f"'{qualified_name}'") from err

        return current_attribute


    def find_class(self, module, name):
        # try to import with the default method
        try:
            print(module, name)
            return super().find_class(module, name)

        # AttributeError is raised when the module is __main__, but in the
        # context of the script that pickled the object
        except (AttributeError, ModuleNotFoundError):
            logging.info('Importing %s.%s failed. Trying to import'
                         ' from %s', module, name, self.callable_file)

            # ensure that only the code meant to be executed on import is
            # executed once we import the file
            if module == '__main__':
                module = '__not_main__'

            spec = importlib.util.spec_from_file_location(module,
                                                          self.callable_file)
            module_obj = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_obj)

            return self.get_nested_attr(module_obj, name)

def main():
    try:
        with open('callable_file.txt', 'r', encoding='utf-8') as f:
            callable_path = f.read()

        with open('callable.pickle', 'rb') as f:
            unpickler = CallableUnpickler(f, callable_path=callable_path)
            callable = unpickler.load()

        with open('args.pickle', 'rb') as f:
            args, kwargs = pickle.load(f)

        result = {'return': callable(*args, **kwargs)}
    except Exception as err: # noqa: F841
        result = {'reason': traceback.format_exc()}

    try:
        with open('result.pickle', 'wb') as f:
            pickle.dump(result, f)
    except Exception as err: # noqa: F841
        with open('result.pickle', 'wb') as f:
            pickle.dump({'reason': 'An exception occured while pickling the '
                         f'return value\n{traceback.format_exc()}'}, f)

if __name__ == '__main__':
    main()
