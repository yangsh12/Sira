from os import F_OK, access, listdir

import kivy.properties as kp
from kivy.app import App

from utils import asserts

class Mutative(object):
    """TODO

    Instance Variables:
        Class-scope Variables:
            username -- kivy.properties.StringPorperty (default None)

        Method-established Variables:
            (initialized by subclasses)
            commandText -- advancedtextinput.AdvancedTextInput (default None)
            config -- kivy.config.ConfigParser
    
    Public Methods:
        Original:
            print_header(self) -> None

    Private Methods:
        _get_font_path(self, str) -> str
        _on_cmd_idf(self, str) -> None
        _on_font_name(self, str) -> None
        _on_font_size(self, str) -> None
        _reset_header(self, str, str) -> None
    
    Events:
        `on_username`
            Fired when username is changed. This will change and write the
            sira.ini (Section: Text, Key: username) based on its value, and call
            _reset_header to preserve [convention #1.1].

    Property Driven Methods:
        on_username(self, advancedtextinput.AdvancedTextInput, str) -> None

    Conventions:
        {
            TODO
        }
    """

    username = kp.StringProperty(None)
    """Kivy string property to store username.

    [convention #4]: {
            [convention #1.1]
        &&  (self.username = "") iff [no user is logged in]         #4.1
    }

    [callback]: on_username
    """

    ###
    commandText = None
    config = None

    def __init__(self):
        """
        """
        pass

    def print_header(self) -> None:
        """Public function to print self.header in self.commandText.

        [requires]: self.header is not None
                    self.commandText is not None
        [ensures]:  [self.header displays as the last part in self.commandText]
                    self.protected_text = self.header
        [calls]:    [reset self.commandText.protected_len]
        """
        if not asserts(self.header is not None,
                       "self.header must be initialized before calling print_header."):
            return
        if not asserts(self.commandText is not None,
                       "self.commandText must be initialized before callingprint_header."):
            return

        obj = self.commandText

        obj.insert_text("\n" + self.header)
        self.protected_text = self.header
        obj.last_row = len(obj._lines) - 1
        obj.last_row_start = len(obj.text) - len(obj._lines[obj.last_row])
        obj.on_cursor(obj, obj.cursor)
    
    def _get_font_path(self, font_name) -> str:
        """Private function to search the path of font file based on font_name.

        [returns]:  "Roboto" if ["res/fonts/" directory is not readable]
                                or [not font file matches font_name]
                                or [the matched file is not readable]
                    "res/fonts/{font_name}.*" if [there is a font file matches
                                                  font_name]
        """
        directory = "res/fonts/"
        if not access(directory, F_OK):
            return "Roboto"
        file_list = listdir(directory)
        for file_name in file_list:
            if font_name.lower() in file_name.lower():
                path = directory + file_name
                break
        return path if access(path, F_OK) else "Roboto"

    def _on_cmd_idf(self, value: str) -> None:
        """Private function fired when cmd_identifier is changed through
        self.config.

        [ensures]:  reset self.header to preserve [convention #1.1]
        [calls]:    _reset_header
        """
        self._reset_header(self.username, value)

    def _on_font_name(self, value: str) -> None:
        """"Privated function fired when font_name is changed through
        self.config.
        """
        self.commandText.font_name = self._get_font_path(value)

    def _on_font_size(self, value: str) -> None:
        """Privated function fired when font_size is changed through
        self.config.

        [ensures]:  self.commandText.font_size = int(value)
        """
        self.commandText.font_size = int(value)

    def _reset_header(self, username: str, identifier: str) -> None:
        """Private funciton to reset self.header based on username and
        identifier to preserve [convention #1.1]

        [ensures]:  [convention #1.1]
        """
        self.header = username + identifier

    def on_username(self, instance: App, value: str) -> None:
        """Property driven function, fired when username is changed. This
        function writes the new value in self.config and its corresponding
        config files.

        [requires]: self.config is not None
                    [convention #4.1] (unchecked)
        [ensure]:   self.config.get("Text", "username") = value
                    [convention #1.1]
        [calls]:    _reset_header
        """
        if not asserts(self.config is not None,
                       "self.config must be initialized before calling on_username."):
            return

        self.config.set("Text", "username", value)
        self.config.write()
        self._reset_header(value, self.config.get("Text", "cmd_identifier"))
