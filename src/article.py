class Article:

    author = None
    content = None
    date = None
    title = None

    def __init__(self, author, content, date, title):
        self.author = author
        self.content = content
        self.date = date
        self.title = title

    def to_string(self):
        author = "author: " + self.author + "\n"
        content = "content: " + (self.content[0][:50] + "...\n" if self.content[0] else "No content available\n")
        date = "date: " + self.date + "\n"
        title = "title: " + self.title + "\n"

        return title + author + date + content
