# Définir une variable globale
#VERSION0 = "1.0.0"

# # Importer des modules
# # from .module1 import fonction1
# from .wiflip    import MSCGui
# from .wiflip    import MyMain
# from .fletcher  import Fletcher
# # Définir un point d'entrée
# from .resource_rc import *
#
import sys
from .wiflip import MSCGui

def mainp():
    MSCGui().runApp(argv=sys.argv)
    