TYPES = ["cam","dvdscr","dvdrip","hdtv","web-dl","webrip","brrip","bdrip","bluray", "ts","tc","scr"]
FILE_EXTENSIONS = [".avi",".mkv",".mp4"]
import winreg as reg
import shutil,os,sys,ctypes,pycountry

def check_language(lang_code):
    try:
        lang_check = pycountry.languages.get(alpha_3=lang_code)
        return True
    except:
        print "Error Wrong Language Code"
        return False

def get_language_name(lang_code):
    return pycountry.languages.get(alpha_3=lang_code).name

def findtype(name):
    for t in TYPES:
        if t in name.lower():
            return t
    return False

def compare_types(a,b):
    if findtype(a) == findtype(b):
        return True
    return False

def Messagebox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)

def uninstall():
    pass

def install(args):
    if not os.path.exists(r"C:\SubGetty"):
        os.mkdir(r"C:\SubGetty")
    if ".exe" in sys.argv[0]:
        exepath = os.path.join("C:\\SubGetty\\",os.path.basename(sys.argv[0]))
        shutil.copyfile(sys.argv[0], exepath)
        params = ' -f "%1" -p {} -u {} -l {}'.format(args.password, args.user, args.language)
    elif ".py" in sys.argv[0]:
        exepath = sys.executable
        params = ' "{}" -f "%1" -p {} -u {} -l {}'.format(sys.argv[0],args.password, args.user, args.language)
    else:
        print "Error wrong extension"
        return False

    classes = reg.ConnectRegistry(None, reg.HKEY_CLASSES_ROOT)
    for extension in FILE_EXTENSIONS:
        key_name = reg.QueryValue(classes,extension)
        reg.SetValue(classes,key_name + "\\shell\\SubGetty"+ args.language,reg.REG_SZ, "Get {} Subtitles".format(get_language_name(args.language)))
        reg.SetValue(classes, key_name + "\\shell\\SubGetty" + args.language+ "\\Command", reg.REG_SZ, exepath + params)
