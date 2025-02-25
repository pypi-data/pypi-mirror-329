"""
This module contains the class for interacting with the Goodgame Empire API's movements-related functions.

The `Movements` class provides methods for managing movements. It is a subclass of `BaseGgeSocket`.
"""

from ..base_gge_socket import BaseGgeSocket

class Movements(BaseGgeSocket):
    """
    A class for interacting with the Goodgame Empire API's movements-related functions.

    This class provides methods for managing movements. It is a subclass of `BaseGgeSocket`.
    """

    def get_movements(self, sync=True, quiet=False):
        """
        Get the movements of the player.

        Args:
            sync (bool, optional): If True, waits for a response and returns it. Defaults to True.
            quiet (bool, optional): If True, suppresses exceptions and returns False on failure. Defaults to False.

        Returns:
            dict: The response from the server if `sync` is True.
            bool: True if the operation was successful and `sync` is False, False if it failed and `quiet` is True.

        Raises:
            Exception: If an error occurs and `quiet` is False.
        """
        try:
            self.send_json_command("gam", {})
            if sync:
                response = self.wait_for_json_response("gam")
                self.raise_for_status(response)
                return response
            return True
        except Exception as e:
            if not quiet:
                raise e
            return False