print('wiflip/__main__.py executed')
import sys
from wiflip import MSCGui

print("__name__:", __name__)            
if __name__ == '__main__':
    MSCGui().runApp(argv=sys.argv)

