import pkgutil
import importlib

package_name = 'models'
package = importlib.import_module(package_name)
for _, module_name, _ in pkgutil.iter_modules(package.__path__):
    print(module_name)