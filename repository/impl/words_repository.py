from model.words_model import Words
from repository.abstract_repository import AbstractRepository


class WordsRepository(AbstractRepository):

    def __init__(self, storage):
        self.__storage = storage
        self.create_table()

    def create_table(self):
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER NOT NULL,
                text VARCHAR (200) NOT NULL,
                id_author VARCHAR (36) NULL,
                
                PRIMARY KEY(id)
            );        
        ''')

    def select_all(self):
        query = self.connection.execute('SELECT * FROM words')
        return [Words.from_result_set(result) for result in query.fetchall()]

    def insert(self, value):
        self.connection.execute('INSERT INTO words(text,id_author) VALUES (?,?);', (value.text, value.author))
        self.connection.commit()

    def delete_by_id(self, unique_id):
        super().delete_by_id(unique_id)

    def drop_table(self):
        super().drop_table()

    @property
    def connection(self):
        return self.__storage.connection
