# XtendR

A very basic Python 3.12 plugin system based on the K.I.S.S principle.

I was in need of a new plugin system, which should meet these requirements:  
:heavy_plus_sign: Simple to use  
:heavy_plus_sign: Work well with Python 3.12  
:heavy_plus_sign: Maintainable - Don't expect to see new releases every month. __If it ain't broken, don't fix it!!!__

I previously used yapsy, but it doesn't meet the requirements anymore.  
:x: No longer simple, and simple to use (Simplicity in use has been sacrificed for more complexity. It has become bloated)  
:x: Not workink with Python 3.12  
:x: No longer maintained (Hasn't been maintained for a few years)

I didn't find anything that suited my needs, so I decided to make my own plugin system.  
It simply contains 2 classes, one for the plugin system and one abstraction base class for the plugins themselves.

At the moment only 4 functions are available:
- Attach
- Run
- Stop
- Detach

Attach and Detach are used for registrering/unregistrering a module on the system.
The Run and Stop functions are mandatory in the plugin modules.

The system expects a folder called 'plugins', placed at the root, along side your main python file.
Each plugin should be placed in subfolders, named as the plugin, inside the 'plugins' folder.

The example.py along with the plugins/example_plugin/example_plugin.py and plugins/example_plugin/example_plugin.json shows the workings of this plugin system.