__author__ = 'Dennis Wallace'

import tempfile

class MediaBase(object):
    """Base Media class.  All media objects should inherit from this class
    to allow common functions to be used in core code.  See MP3 and OGG classes
    for examples on how to configure a subclass."""

    def __init__(self):
        object.__init__(self)

        # Set the following five values in an inherited subclass.

        # A text string describing this media type
        self.description = ''

        # A text string declaring the MIME Type for this media type
        self.mime_type = ''

        # A text string declaring the common file extension for this media type
        self.extension = ''

        # A text string declaring the media format.  The self.format property
        # should be unique across all subclasses inherited from MediaBase.
        self.format = ''

        # tagdata contains a dictionary of tags to use to gather metadata from the sourceobj
        self.tagdata = {}

        self.media = None
        self.item_id = ''
        self.source = None
        self.options = {}
        self.bitrate_default = 0
        self.info = None
        self.bitrate = 0
        self.length = 0
        self.metadata = {
            'title': '',
            'artist': '',
            'album': '',
            'date': '',
            'comment': '',
            'country': '',
            'genre': '',
            'copyright': ''
        }

        # sourceobj contains the metadata information for the referenced object
        self.sourceobj = {}

        self.media_info = []
        self.file_name = ''
        self.file_title = ''
        self.file_ext = ''
        self.size = 0

        # A more cross-platform way to do this
        self.cache_dir = tempfile.gettempdir()

    def get_format(self):
        """Gets the format string of the media type"""
        return self.format

    def get_file_extension(self):
        """Gets the actual file extension string of the media"""
        return self.file_ext

    def get_mime_type(self):
        """Gets the MIME Type string for this media type"""
        return self.mime_type

    def get_description(self):
        """Gets the description string for this media type"""
        return self.description

    def set_cache_dir(self, path):
        """Sets an alternate location for temporary cache files used in this media object"""
        self.cache_dir = path

    def get_file_metadata(self):
        """Returns the metadata for the media, filtered by the tagdata dictionary for this media type"""
        metadata = {}
        for key in self.tagdata.keys():
            metadata[key] = ''
            try:
                metadata[key] = self.sourceobj[key][0]
            except:
                try:
                    if self.tagdata[key] != '':
                        metadata[key] = self.sourceobj[self.tagdata[key]][0]
                except:
                    pass
        return metadata

    def __get_metadata_value(self, key, clean=False):
        """Returns a metadata value for a give key.  If clean is True, then the resulting string will
        be cleaned before it is returned.  If the key does not exist, an empty string is returned."""
        if key not in self.metadata:
            return ''
        r = self.metadata[key]
        if clean:
            r = r.replace('_',' ').strip()
        return r.encode('utf-8')

    def get_title(self):
        """Returns the cleaned title for this media"""
        return self.__get_metadata_value('title', True)

    def get_artist(self):
        """Returns the cleaned artist for this media"""
        return self.__get_metadata_value('artist', True)

    def get_song(self, usefn=True):
        """Returns a string in the form "artist - title" for this media.  If either artist or title are blank,
        only the non-blank field is returned.  If both fields are blank, and the usefn parameter is True, then
        the filename is returned instead.  Otherwise, an empty string is returned."""
        a = self.__get_metadata_value('artist', True)
        t = self.__get_metadata_value('title', True)
        if len(a) == 0 and len(t) == 0 and usefn:
            a = self.file_name.encode('utf-8')
        r = a
        if len(a) > 0 and len(t) > 0:
            r += ' - '
        r += t
        return r
