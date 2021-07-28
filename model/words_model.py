class Words:

    def __init__(self, text, author, unique_id=None):
        self.__unique_id = unique_id
        self.__text = text
        self.__author = author

    @property
    def text(self):
        return self.__text

    @property
    def unique_id(self):
        return self.__unique_id

    @property
    def author(self):
        return self.__author

    def __str__(self):
        return "Words(id={}, text={}, authorId={})".format(self.unique_id, self.text, self.author)

    @staticmethod
    def from_result_set(result):
        return Words(unique_id=result[0], text=result[1], author=result[2])
