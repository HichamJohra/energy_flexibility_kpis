import pkgutil
import importlib
import inspect
import unittest
import io
import textwrap

def get_classes_from_module(module):
    """Given a module, returns a list of all classes defined in that module."""
    return [name for name, obj in inspect.getmembers(module) if inspect.isclass(obj) and obj.__module__ == module.__name__]

def get_submodules_and_classes(package_name):
    """Given a package name, returns a dictionary of all modules and classes defined in that package."""
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        print(f"Unable to import the package: {package_name}")
        return {}

    modules_and_classes = {}
    for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if not ispkg:  # We only want modules, not sub-packages
            full_module_name = f"{package_name}.{modname}"
            try:
                module = importlib.import_module(full_module_name)
                classes = get_classes_from_module(module)
                modules_and_classes[modname] = classes
            except ImportError:
                print(f"Unable to import the module: {full_module_name}")

    return modules_and_classes

def find_untested_classes(source_modules, test_modules):
    """Given a dictionary of source modules and a dictionary of test modules, returns a dictionary of all untested classes."""
    untested_classes = {}

    for module, classes in source_modules.items():
        test_module_name = f"test_{module}"
        if test_module_name not in test_modules:
            untested_classes[module] = classes
        else:
            untested_classes_in_module = [cls for cls in classes if f"test_{cls}" not in test_modules[test_module_name]]
            if untested_classes_in_module:
                untested_classes[module] = untested_classes_in_module

    return untested_classes

def run_unittests_for_module(module_name, class_name):
    """Given a module name and a class name, runs the unit tests for that class and returns the output."""
    # Create a TestLoader to discover tests from the test module and class
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f"{module_name}.test_{class_name}")

    # Create a TextTestRunner with a custom output stream to capture results
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(suite)

    # Get the captured output
    output = stream.getvalue()

    # Indent each line of the output
    indented_output = textwrap.indent(output, '    ')

    # Return the captured output
    return indented_output

if __name__ == "__main__":
    source_dir = get_submodules_and_classes("energy_flexibility_kpis.kpi.energy_flexibility")
    test_dir = get_submodules_and_classes("energy_flexibility_kpis.test")
    
    for module, classes in source_dir.items():
        print(f"Module: {module}")
        for cls in classes:
            print(f"  Class: {cls}")
            test_module_name = f"test_{module}"
            if test_module_name in test_dir and f"test_{cls}" in test_dir[test_module_name]:
                test_output = run_unittests_for_module(test_module_name, cls)
                print(test_output)
            else:
                print("    NA")
