"""
Utility class for shared functions.
"""

import os


class Utility:
    @staticmethod
    def clean_date(date):
        """
        Strips the date to only YYYY-MM-DD.

        :type date: str
        :rtype:     str
        """
        return date[:date.find("T")]

    @staticmethod
    def clean_url(url):
        """
        Strips references (rref) from article URLs.

        :type url: str
        :rtype:    str
        """
        if ".html" in url and "?rref" in url:
            return url[:url.find("?rref")]

        return url

    @staticmethod
    def reset_cache(directory):
        """
        Reset side-effects from previous executions
        """
        # creates directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        # clears files in directory from previous executions
        for file in os.listdir(directory):
            file_loc = os.path.join(directory, file)

            try:
                os.unlink(file_loc)
            except Exception as err:
                print(err)
