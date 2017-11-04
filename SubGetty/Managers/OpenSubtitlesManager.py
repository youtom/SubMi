import struct, os, urllib2, sys, difflib, random, shutil,ctypes
from pythonopensubtitles.opensubtitles import OpenSubtitles
from pythonopensubtitles.utils import File
from zipfile import ZipFile
import operator
from utils import compare_types


class OpenSubtitlesManager():
    """
        this class manages the connection, search and fetching of the subtitles.
    """

    def __init__(self,opensubs_email,opensubs_password,path,language="eng"):
        """
            init opensubtitles object, and token
        :param path: path to media file
        :param language: language of subtitles needed
        :param opensubs_email: Email of OpenSubtitles account
        :param opensubs_password:  Password of OpenSubtitles account
        """
        self.path = path
        self.language = language
        self.opensubtitles = OpenSubtitles()
        self.token = self.opensubtitles.login(opensubs_email, opensubs_password)
        self.is_auth = False
        if self.token:
            self.is_auth = True

    def run(self):
        """
        this dont need no doc
        :return:
        """
        subtitles_objects = self.search_subtitles()
        if not subtitles_objects:
            return None
        matched_sub = self.filter_results(subtitles_objects)
        self.download_subs(matched_sub)
        return True

    def search_subtitles(self):
        """
            search subtitles for a given file
        :return: Opensubtitles search data or None
        """

        try:
            movie_file = File(self.path)
        except:
            print "Error Calculating File Size"
            return False

        file_hash = movie_file.get_hash()
        if "Error" in file_hash:
            print "Error Calculating File Hash"
            return False

        if not self.is_auth:
            print "Error Connecting to OpenSubtitles"
            return False

        # search function
        searchdata = self.opensubtitles.search_subtitles(
            [{'sublanguageid': self.language, 'moviehash': file_hash, 'moviebytesize': movie_file.size}])

        return searchdata

    # TODO: fix access deined error
    def download_subs(self,subtitles_object):
        """

        :param subtitles_object: an object recived from the opensubtitles API search function
        :return: nothing
        """

        res = urllib2.urlopen(subtitles_object['ZipDownloadLink'])

        # find extension of subtitles file
        extension = subtitles_object['SubFileName'][subtitles_object['SubFileName'].rindex('.'):]

        # create temp file name for downloading subtitles zip
        zippath = os.path.join(os.getenv("TEMP"), "temp_{}.zip".format(random.randint(10000, 99999)))

        try:
            with open(zippath, "wb") as z:
                z.write(res.read())
            fZip = ZipFile(zippath, 'r')

            # extract subtitles
            for zipobj in fZip.filelist:
                if extension in zipobj.filename:
                    name = zipobj.filename
                    fZip.extract(zipobj, path=os.getenv("TEMP"))

            # copy file to movie folder and change name
            shutil.copyfile(os.path.join(os.getenv("TEMP"), name), self.path.replace(self.path[self.path.rindex('.'):], extension))
        except:
            print "Error in Saving or Exracting files"


    def filter_results(self, subtitles_objects):
        """

        :param subtitles_objects: a list of subtitles objects recived from opensubtitles API search finction
        :return: best matching subtitle object
        """
        similar_dic = {}
        basename = os.path.basename(self.path)

        # main loop, iterates subtitles objects
        for sub,i in zip(subtitles_objects,range(len(subtitles_objects))):
            # using difflib to find how similar the name of the media file is to the subtitle file.
            ratio = difflib.SequenceMatcher(a=sub["SubFileName"].lower(),b=basename.lower()).ratio()

            # if ratio is more than 90% return
            if ratio > 0.9:
                return sub

            # checks if the type of movie is compatible. if so gives bonus points
            if compare_types(basename, sub["SubFileName"]):
                ratio += 0.1

            similar_dic[i] = ratio

        # return the max value of ratio.
        return subtitles_objects[max(similar_dic.iteritems(), key=operator.itemgetter(1))[0]]


