from xml.etree.ElementTree import fromstring
import xmltodict
import os
import tempfile


class Soundpad:
    """
    Provides methods to interact with Soundpad via a named pipe.
    """

    def __init__(self):
        self.pipe = None
        self.pipe_name = "sp_remote_control"
        self.tmp_file = os.path.join(tempfile.gettempdir(), "soundpad_query.txt")

    def _init_connection(self):
        """
        Initializes the connection to the Soundpad pipe.
        """
        if not self.pipe:
            try:
                self.pipe = open(rf"\\.\pipe\{self.pipe_name}", "r+b", buffering=0)
            except Exception as e:
                print(f"Error opening pipe: {e}")
                self.pipe = None

    def _close_connection(self):
        """
        Closes the Soundpad pipe connection if open.
        """
        if self.pipe:
            try:
                self.pipe.close()
            except Exception:
                pass
            finally:
                self.pipe = None

    def send_command(self, command):
        """
        Sends a command to Soundpad and reads the response.
        """
        self._init_connection()
        try:
            if self.pipe:
                self.pipe.write(command.encode())
                self.pipe.seek(0)
                # FIXME: use chucks or something here
                data = self.pipe.read(65536)
                self.pipe.seek(0)
                return data
            else:
                print("Pipe is not initialized.")
                return None
        except Exception as e:
            print(f"Error sending command: {e}")
            return None

    def categories(self) -> dict[str, str]:
        """
        Retrieves available categories from Soundpad.

        Returns:
            dict[str, str]: Maps category index to category name.
        """
        data = self.send_command("GetCategories(false, false)")
        if not data:
            return {}
        category_dict = {}
        xml_data = fromstring(data)
        for cat in xml_data:
            if "All sounds" not in cat.attrib["name"]:
                category_dict[cat.attrib["index"]] = cat.attrib["name"]
        return category_dict

    def category_sounds(self, category_id) -> dict[str, str]:
        """
        Retrieves the sounds for the given category.

        Returns:
            dict[str, str]: Maps sound index to sound title.
        """
        data = self.send_command(f"GetCategory({category_id},true,false)")
        if not data:
            return {}
        xml_data = data.decode("utf-8")
        xml_dict = xmltodict.parse(xml_data)
        sounds = {}
        for sound in xml_dict["Categories"]["Category"]["Sound"]:
            sounds[sound["@index"]] = sound["@title"]
        return sounds

    def sound_play(self, sound_id):
        """
        Plays the specified sound by ID.
        """
        self.send_command(f"DoPlaySound({sound_id})")

    def sound_stop(self):
        """
        Stops all currently playing sounds.
        """
        self.send_command("DoStopSound()")

    def query_sounds(self, search_string: str) -> dict[str, str]:
        """
        Returns sounds matching the given search string.

        Returns:
            dict[str, str]: Maps sound index to sound title for matches.
        """
        all_sounds = {
            sid: sname
            for cat_id in self.categories()
            for sid, sname in self.category_sounds(cat_id).items()
        }

        search_results = {
            sid: sname
            for sid, sname in all_sounds.items()
            if search_string.lower() in sname.lower()
        }

        return search_results

    def query_id_set(self, sound_id: str) -> None:
        """
        Stores the given sound ID in a temporary file.
        """
        # write the id to a temp file (windows)
        with open(self.tmp_file, "w") as file:
            file.write(sound_id)

    def query_id_get(self) -> str:
        """
        Retrieves the stored sound ID from the temporary file.
        """
        # read the id from a temp file (windows)
        with open(self.tmp_file, "r") as file:
            return file.read().strip()

    def query_play(self, id: str) -> None:
        """
        Plays the sound with the currently set ID.
        """
        self.sound_play(id)

    def get_all_sounds(self) -> dict[str, str]:
        """
        Returns a dictionary of all sounds in Soundpad.

        Returns:
            dict[str, str]: Maps sound index to sound title.
        """
        data = self.send_command("GetSoundlist()")
        if not data:
            return {}
        xml_data = data.decode("utf-8")
        xml_dict = xmltodict.parse(xml_data)
        sounds = {}
        for sound in xml_dict["Soundlist"]["Sound"]:
            sounds[sound["@index"]] = sound["@title"]
        return sounds
