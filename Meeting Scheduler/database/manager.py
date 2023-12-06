import psycopg2


class DatabaseManager:
    """
    This class is responsible for managing the connection to the database and performing various operations.
    """

    def __init__(self):
        self.conn = None

    def open_connection(self):
        """
        Opens a connection to the database.
        :param self:
        :return:
        """
        self.conn = psycopg2.connect(
            dbname="meetings",
            user="postgres",
            password="user",
            host="localhost",
            port="5432"
        )

    def close_connection(self):
        """
        Closes the connection to the database.
        :param self:
        :return:
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def search_id_db(self, id):
        """
        Verifies the id doesn't already exist in the database.
        :param id:
        :return: True if the id doesn't exist in the database, False otherwise.
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM person WHERE id = %s", (id,))
            rows = cursor.fetchall()
            if len(rows) != 0:
                print(rows)
                return False

            else:
                return True
        except psycopg2.Error as e:
            print("Error:", e)
            return False

    def add_person(self, id, first_name, last_name):
        """
        Adds a person to the database
        :param id:
        :param first_name:
        :param last_name:
        :return: True if the person was successfully added to the database, False otherwise.
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO person (id, first_name, last_name) VALUES (%s, %s, %s)",
                           (id, first_name, last_name))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error:", e)
            return False
