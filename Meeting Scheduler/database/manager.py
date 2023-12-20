import psycopg2


class DatabaseManager:
    """
    This class is responsible for managing the connection to the database and performing various operations.
    """

    def __init__(self):
        self.conn = None

    def open_connection(self):
        """
        Opens a connection to the database \n
        Parameters
        ----------
            self : DatabaseManager
                The object itself
        Returns
        -------
            None
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
        Closes the connection to the database \n
        Parameters
        ----------
            self : DatabaseManager
                The object itself
        Returns
        -------
            None
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    def search_id_db(self, id):
        """
        Verifies the id doesn't already exist in the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        id : int
            The id to be verified
        Returns
        -------
        bool
            True if the id doesn't exist in the database, False otherwise.
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
        Adds a person to the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        id : int
            The id of the person
        first_name : str
            The first name of the person
        last_name : str
            The last name of the person
        Returns
        -------
        bool
            True if the person was successfully added to the database, False otherwise.
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

    def find_all_persons(self):
        """
        Finds all the persons in the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        Returns
        -------
        list
            A list of all the persons in the database.
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM person")
            rows = cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error:", e)
            return None

    def add_meeting(self, start_time, end_time, participants, name):
        """
        Adds a meeting to the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        start_time : datetime.datetime
            The start time of the meeting
        end_time : datetime.datetime
            The end time of the meeting
        participants : list
            The participants of the meeting
        name : str
            The name of the meeting
        Returns
        -------
        bool
            True if the meeting was successfully added to the database, False otherwise.
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO meeting (start_time, end_time, name) VALUES (%s, %s, %s)",
                           (start_time, end_time, name))

            cursor.execute("SELECT * FROM meeting ORDER BY ID DESC LIMIT 1")
            meeting_id = cursor.fetchone()[0]
            res = self.add_participants_to_meeting(meeting_id, participants)
            if not res:
                print("Error while adding participants to meeting")
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error:", e)
            return False

    def add_participants_to_meeting(self, meeting_id, participants):
        """
        Adds participants to a meeting \n
       Parameters
         ----------
            self : DatabaseManager
                The object itself
            meeting_id : int
                The id of the meeting
            participants : list
                The participants of the meeting
        Returns
        -------
            bool
                True if the participants were successfully added to the meeting, False otherwise.

        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            participants = list(set(participants))
            for participant in participants:
                participant_id = participant[0]
                cursor.execute("INSERT INTO meeting_participants (meeting_id, person_id) VALUES (%s, %s)",
                               (meeting_id, participant_id))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error:", e)
            return False

    def search_meetings(self, start_time, end_time):
        """
        Searches for meetings in the database that are in the specified interval \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        start_time : datetime.datetime
            The start time of the interval
        end_time : datetime.datetime
            The end time of the interval
        Returns
        -------
        list
            A list of meetings that are in the specified interval
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM meeting WHERE start_time >= %s AND end_time <= %s", (start_time, end_time))
            rows = cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error:", e)
            return None

    def get_participants(self, meeting_id):
        """
        Gets the participants of a meeting \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        meeting_id : int
            The id of the meeting
        Returns
        -------
        list
            A list of participants of the meeting

        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT person_id FROM meeting_participants WHERE meeting_id = %s", (meeting_id,))
            rows = cursor.fetchall()
            participants = []
            for row in rows:
                cursor.execute("SELECT * FROM person WHERE id = %s", (row[0],))
                participants.append(cursor.fetchone())
            return participants
        except psycopg2.Error as e:
            print("Error:", e)
            return None

    def get_all_meetings_with_participants(self):
        """
        Gets all the meetings from the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        Returns
        -------
        list
            A list of all the meetings from the database
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM meeting")
            rows = cursor.fetchall()
            for i in range(len(rows)):
                participants = self.get_participants(rows[i][0])
                rows[i] = (rows[i], participants)
            return rows
        except psycopg2.Error as e:
            print("Error:", e)
            return None

    def update_person(self, id, first_name, last_name):
        """
        Updates a person in the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        id : int
            The id of the person
        first_name : str
            The first name of the person
        last_name : str
            The last name of the person
        Returns
        -------
        bool
            True if the person was successfully updated, False otherwise.
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("UPDATE person SET first_name = %s, last_name = %s WHERE id = %s",
                           (first_name, last_name, id))
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error:", e)
            return False

    def update_meetings(self, meetings, participants):
        """
        Updates a meeting in the database \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        meetings : list
            The meetings to be updated
        participants : list
            The participants of the meetings
        Returns
        -------
        bool
            True if the meetings were successfully updated, False otherwise.
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            for meeting in meetings:
                cursor.execute("DELETE FROM meeting_participants WHERE meeting_id = %s", (meeting[0][0],))
                res = self.add_participants_to_meeting(meeting[0][0], participants)
                if not res:
                    print("Error while updating meeting")
                    return False
            self.conn.commit()
            return True
        except psycopg2.Error as e:
            print("Error:", e)
            return False

    def get_meetings_by_participant_id(self, id):
        """
        Gets the meetings of a participant \n
        Parameters
        ----------
        self : DatabaseManager
            The object itself
        id : int
            The id of the participant
        Returns
        -------
        list
            A list of meetings of the participant
        """
        try:
            if not self.conn:
                self.open_connection()
            cursor = self.conn.cursor()
            cursor.execute("SELECT meeting_id FROM meeting_participants WHERE person_id = %s", (id,))
            rows = cursor.fetchall()
            meetings = []
            for row in rows:
                cursor.execute("SELECT * FROM meeting WHERE id = %s", (row[0],))
                meetings.append(cursor.fetchone())
            return meetings
        except psycopg2.Error as e:
            print("Error:", e)
            return None
