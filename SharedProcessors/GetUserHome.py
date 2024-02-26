#!/usr/local/autopkg/pythoncipeo

import os

from autopkglib import Processor

__all__ = ["GetUserHome"]


class GetUserHome(Processor):
    """
    This processor returns the current user's Home Directory.
    """

    input_variables = {}
    output_variables = {}

    description = __doc__

    def main(self):
        """Main process."""
        try:
            user_home = os.path.expanduser("~")
            current_user = os.path.basename(user_home)
            self.env["user_home"] = user_home
            self.env["current_user"] = current_user
            self.output(f"Current user: {current_user}")
            self.output(f"User Home Directory: {user_home}")
        except Exception as e:
            self.output(f"User Home Directory could not be determined (error: {e})")


if __name__ == "__main__":
    PROCESSOR = GetUserHome()
    PROCESSOR.execute_shell()
