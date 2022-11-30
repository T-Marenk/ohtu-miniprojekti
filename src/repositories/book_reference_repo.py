class BookReference:
    def __init__(self, connection):
        self.connection = connection

    def get_data(self):
        cursor = self.connection.cursor()

        data = cursor.execute("SELECT * FROM bookreferences").fetchall()

        return data


    def add_to_table(self, list):
        cursor = self.connection.cursor()

        cursor.execute("INSERT INTO bookreferences (author, title, year, publisher, bib_key) VALUES (?, ?, ?, ?, ?)", list)
        self.connection.commit()


    
