import pkgutil
import os
import sys

def find_package(import_name): 
    #copy from flask
    """Finds a package and returns the prefix (or None if the package is
    not installed) as well as the folder that contains the package or
    module as a tuple.  The package path returned is the module that would
    have to be added to the pythonpath in order to make it possible to
    import the module.  The prefix is the path below which a UNIX like
    folder structure exists (lib, share etc.).
    """
    root_mod_name = import_name.split('.')[0]
    loader = pkgutil.get_loader(root_mod_name)
    if loader is None or import_name == '__main__':
        # import name is not found, or interactive/main module
        package_path = os.getcwd()
    else:
        # For .egg, zipimporter does not have get_filename until Python 2.7.
        if hasattr(loader, 'get_filename'):
            filename = loader.get_filename(root_mod_name)
        elif hasattr(loader, 'archive'):
            # zipimporter's loader.archive points to the .egg or .zip
            # archive filename is dropped in call to dirname below.
            filename = loader.archive
        else:
        # At least one loader is missing both get_filename and archive:
        # Google App Engine's HardenedModulesHook
        #
        # Fall back to imports.
            __import__(import_name)
            filename = sys.modules[import_name].__file__
        package_path = os.path.abspath(os.path.dirname(filename))
        # package_path ends with __init__.py for a package
        if loader.is_package(root_mod_name):
            package_path = os.path.dirname(package_path)

    site_parent, site_folder = os.path.split(package_path)
    py_prefix = os.path.abspath(sys.prefix)
    if package_path.startswith(py_prefix):
        return py_prefix, package_path
    elif site_folder.lower() == 'site-packages':
        parent, folder = os.path.split(site_parent)
        # Windows like installations
        if folder.lower() == 'lib':
            base_dir = parent
        # UNIX like installations
        elif os.path.basename(parent).lower() == 'lib':
            base_dir = os.path.dirname(parent)
        else:
            base_dir = site_parent
            return base_dir, package_path
    return None, package_path


def getDefaultPath():
    prefix, package_path = find_package(__name__)
    if prefix is None:
        return package_path
    root_mod_name = __name__.split('.')[0]
    return os.path.join(prefix, 'var', root_mod_name)
