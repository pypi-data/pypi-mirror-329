import importlib
import sys
import os
import json
from abc import ABC, abstractmethod

class XtendR:
    """Plugin system to manage plugins.
    
    Example:
    >>> system = XtendRSystem()
    >>> system.attach("example_plugin")  # Assuming 'example_plugin/plugin_info.json' exists
    >>> system.run("example_plugin")
    ExamplePlugin is running!
    >>> system.stop("example_plugin")
    ExamplePlugin has stopped!
    >>> system.detach("example_plugin")
    Detached plugin 'example_plugin'.
    """
    def __init__(self):
        self.plugins = {}
    
    def attach(self, name: str) -> None:
        """Dynamically load a plugin from its folder."""
        if name in self.plugins:
            print(f"Plugin '{name}' is already attached.")
            return
        
        plugin_path = os.path.join(os.getcwd(), name)
        info_path = os.path.join(plugin_path, "plugin_info.json")
        
        if not os.path.isdir(plugin_path) or not os.path.isfile(info_path):
            print(f"Failed to attach plugin '{name}', folder or info file not found.")
            return
        
        try:
            with open(info_path, "r", encoding="utf-8") as f:
                plugin_info = json.load(f)
                module_name = plugin_info.get("module")
                class_name = plugin_info.get("class")
                if not module_name or not class_name:
                    print(f"Plugin '{name}' info file is missing 'module' or 'class' key.")
                    return
                
                sys.path.insert(0, plugin_path)
                module = importlib.import_module(module_name)
                plugin_class = getattr(module, class_name)
                instance = plugin_class()
                
                if not isinstance(instance, XtendRBase):
                    print(f"Plugin '{name}' does not inherit from PluginBase.")
                    return
                
                self.plugins[name] = {
                    'instance': instance,
                    'running': False,
                    'info': plugin_info
                }
                print(f"Attached plugin '{name}'.")
        except (ModuleNotFoundError, json.JSONDecodeError, AttributeError) as e:
            print(f"Failed to attach plugin '{name}': {e}")
    
    def run(self, name: str, *args, **kwargs):
        """Run the plugin's 'run' method if available."""
        if name in self.plugins:
            self.plugins[name]['running'] = True
            return self.plugins[name]['instance'].run(*args, **kwargs)
        print(f"Plugin '{name}' not found or has no 'run' method.")
    
    def stop(self, name: str) -> None:
        """Stop the plugin if it's running."""
        if name in self.plugins and self.plugins[name]['running']:
            self.plugins[name]['running'] = False
            self.plugins[name]['instance'].stop()
        else:
            print(f"Plugin '{name}' is not running.")
    
    def detach(self, name: str) -> None:
        """Unload a plugin."""
        if name in self.plugins:
            del self.plugins[name]
            sys.modules.pop(name, None)
            print(f"Detached plugin '{name}'.")
        else:
            print(f"Plugin '{name}' is not attached.")
