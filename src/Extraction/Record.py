class Record:
    def __init__(self, title: str, link: str, description: str, pubDate: str, guid: str, categories: list[str]):
        self.title = title
        self.link = link
        self.description = description
        self.pubDate = pubDate
        self.guid = guid
        self.categories = categories
    
    def __str__(self):
        return f"Title: {self.title}\nLink: {self.link}\nDescription: {self.description}\nPubDate: {self.pubDate}\nGuid: {self.guid}\nCategories: {self.categories}"