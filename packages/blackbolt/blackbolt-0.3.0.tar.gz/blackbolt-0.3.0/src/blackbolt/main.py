from blackbolt.utils.shell_utils import get_folder
from blackbolt.utils.shell_utils import get_file
from blackbolt.utils.shell_utils import remove_folder

available = {'0 ' : "ML TS XAI HC(Folder)",
             '-1' : "Remove Folder"}

def echo(name = None, open = False):
    try:
        if name is not None:
            name = str(name)
        if name in ['0']    :   get_folder("ML TS XAI HC", loc = True)
        elif name in ['-1'] :   remove_folder("ML TS XAI HC")
        else:
            for k, v in available.items():
                sep = " : " if v else ""
                print(k,v,sep = sep)
    except Exception as error:
        print(error)