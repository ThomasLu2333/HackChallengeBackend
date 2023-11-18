import sqlite3


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for our app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Secures a connection with the database and stores it into the
        instance variable `conn`
        """
        self.conn = sqlite3.connect("todo.db", check_same_thread=False)
        self.create_location_table()
        self.create_restaurant_table()
        self.create_review_table()

    # -- TASKS -----------------------------------------------------------

    def create_location_table(self):
        """
        Create a table to general locations (North, South, CTown, etc..)
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS location( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                );
                """
            )
            self.conn.commit()
        except Exception as e:
            print("error creating location table" + e)

    def create_restaurant_table(self):
        """
        Create a table to store dining halls / restaurants
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS restaurant( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL, 
                    cuisine TEXT NOT NULL, 
                    address TEXT NOT NULL, 
                    image TEXT NOT NULL, 
                    rating REAL NOT NULL, 
                    location_id INTEGER NOT NULL, 
                    FOREIGN KEY(location_id) REFERENCES location(id) ON DELETE CASCADE,
                );
                """
            )
            self.conn.commit()
        except Exception as e:
            print("error creating restaurant table" + e)

    def create_review_table(self):
        """
        Create a table to store restaurant reviews
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS review( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_created DATE NOT NULL, 
                    service INTEGER NOT NULL, 
                    decor INTEGER NOT NULL, 
                    food INTEGER NOT NULL, 
                    description TEXT NOT NULL, 
                    restaurant_id INTEGER NOT NULL, 
                    FOREIGN KEY(restaurant_id) REFERENCES restaurant(id) ON DELETE CASCADE,
                """
            )
        except Exception as e:
            print("error creating review table" + e)


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
