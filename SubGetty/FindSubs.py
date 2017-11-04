import argparse,os,ctypes
from Managers.OpenSubtitlesManager import OpenSubtitlesManager
from utils import install,Messagebox,check_language


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--install", help="Install self as a right click option",action="store_true")
    parser.add_argument("-p","--password",type=str,help="A valid password for an OpenSubtitles user",required=True)
    parser.add_argument("-u","--user", type=str, help="A valid email for an OpenSubtitles user",required=True)
    parser.add_argument("-f","--file", type=str, help="Path to a media file")
    parser.add_argument("-l", "--language", type=str,default="eng" ,help="Language of desired subtitles, NOTE: if used with install flag will install for the specifid language. default is English")
    args = parser.parse_args()

    if not args.install and not args.file:
        print "Argument Error: you must either specify --file or --install"
        return False

    if not check_language(args.language):
        return False

    if args.install:
        install(args)
        Messagebox("Installed", "Installed Subgetty on your computer with these parameters password={} user={} language={}".format(args.password ,args.user,args.language), 1)
        return True

    if not os.path.exists(args.file):
        print "Error Media File Doesnt exists"
        return False


    osm = OpenSubtitlesManager(args.user, args.password, args.file, language=args.language)
    if osm.run():
        Messagebox("Found!", "Subtitles were found and downloaded", 1)
    else:
        Messagebox("Check STDOUT for Error Message", "No subtitles found", 1)


if __name__ == "__main__":
    main()