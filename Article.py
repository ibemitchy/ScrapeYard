class Article:

    __author = None
    __content = None
    __date = None
    __title = None

    def __init__(self, author, content, date, title):
        self.__author = author
        self.__content = content
        self.__date = date
        self.__title = title

    def to_string(self):
        author = "author: " + self.__author + "\n"
        content = "content: " + self.__content[:50] + "...\n"
        date = "date: " + self.__date + "\n"
        title = "title: " + self.__title + "\n"

        return title + author + date + content
