import json
import subprocess


class DefaultList(list):
    def __init__(self, default_value=None):
        super().__init__()
        self.default = default_value

    def __getitem__(self, index):
        if 0 <= index < len(self):
            return super().__getitem__(index)
        return self.default


def load_plist(b_input) -> dict:
    """
    Converts a binary plist input into a dictionary by first converting the binary plist
    to JSON format and then loading it as a native Python dictionary. The function uses
    the 'plutil' command-line utility for the conversion from binary to JSON.

    :param b_input: A process object or similar that provides a readable stream for
        the binary plist content, typically accessible via its stdout attribute.
    :type b_input: subprocess.CompletedProcess or any object with a similar interface.

    :return: A dictionary representation of the plist data after conversion to JSON.
    :rtype: dict

    :raises subprocess.CalledProcessError: If the 'plutil' command execution fails.
    :raises json.JSONDecodeError: If the converted output is not valid JSON format.
    """

    cmd = ["plutil", "-convert", "json", "-o", "-", "-"]
    data = subprocess.run(cmd, input=b_input, capture_output=True, text=True)
    return json.loads(data.stdout)
