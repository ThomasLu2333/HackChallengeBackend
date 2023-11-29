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
        Create a table to general locations (e.g. North, South, CTown) and prepopulate table with some locations
        """
        try:
            self.conn.execute("""DROP TABLE IF EXISTS location; """)
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS location( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                );
                """
            )
            self.conn.execute("INSERT INTO location (name) VALUES ('North Campus'); ")
            self.conn.execute("INSERT INTO location (name) VALUES ('West Campus');")
            self.conn.execute("INSERT INTO location (name) VALUES ('Central Campus'); ")
            self.conn.execute(" INSERT INTO location (name) VALUES ('Central Campus'); ")
            self.conn.execute("INSERT INTO location (name) VALUES ('Downtown'); ")
            self.conn.execute("INSERT INTO location (name) VALUES ('Other'); ")
            self.conn.commit()
        except Exception as e:
            print("error creating location table " + str(e))

    def create_restaurant_table(self):
        """
        Create a table to store dining halls / restaurants
        """
        try:
            self.conn.execute("""DROP TABLE IF EXISTS restaurant; """)
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
                    FOREIGN KEY(location_id) REFERENCES location(id) ON DELETE CASCADE
                );
                """
            )
            self.conn.commit()
        except Exception as e:
            print("error creating restaurant table " + str(e))

    def create_review_table(self):
        """
        Create a table to store restaurant reviews
        """
        try:
            self.conn.execute("""DROP TABLE IF EXISTS review; """)
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
                    FOREIGN KEY(restaurant_id) REFERENCES restaurant(id) ON DELETE CASCADE
                ); 
                """
            )
        except Exception as e:
            print("error creating review table " + str(e))

    def get_locations(self):
        """
        Return a list of all available locations, each as a dictionary of form {"id":id,"name":name}.
        """
        cursor = self.conn.execute(
            """
            SELECT * 
            FROM location; 
        """)
        return [{"id": row[0], "name": row[1]} for row in cursor]

    def get_location(self, location_id):
        """
        Return the location that has id location_id if the corresponding location exists, and return None otherwise.
        """
        row = self.conn.execute(
            """
            SELECT *
            FROM location
            WHERE id = ?; 
            """,
            (location_id,)
        ).fetchone()
        if row is None:
            return None
        return {"id": row[0], "name": row[1]}

    def get_restaurant(self, restaurant_id):
        """
        Return the restaurant that has id restaurant_id if the corresponding location exists, and return None
        otherwise. The returned restaurant will be a dictionary of form
        {"id":id,"description":description",
        "cuisine":cuisine,"address":address,"image":image, "rating":rating,"location_id":location_id}
        """
        row = self.conn.execute(
            """
            SELECT *
            FROM restaurant
            WHERE id = ?; 
            """,
            (restaurant_id,)
        ).fetchone()
        if row is None:
            return None
        restaurant = {"id": row[0], "description": row[1], "cuisine": row[2], "address": row[3], "image": row[4],
                      "rating": row[5], "location_id": row[6]}
        cursor = self.conn.execute(
            """
            SELECT *
            FROM review
            WHERE restaurant_id=?;
            """,
            (restaurant["id"],)
        )
        restaurant["reviews"] = [
            {"date_created": row[0], "service": row[1], "decor": row[2], "food": row[3], "description": row[4]}
            for row in cursor
        ]
        return restaurant

    def get_restaurants_of_location(self, location_id):
        """
        Return a list of all restaurants in the location with id location_id, each as a dictionary of form
        {"id":id,"description":description",
        "cuisine":cuisine,"address":address,"image":image, "rating":rating,"location_id":location_id}
        Requires that location_id must correspond to a valid location.
        """
        cursor = self.conn.execute(
            """
            SELECT id
            FROM restaurant
            WHERE location_id=?;""",
            (location_id,)
        )
        return [self.get_restaurant(row[0]) for row in cursor]

    def create_restaurant(self, description, location_id, cuisine, address, image):
        """
        Creates a new restaurant in the restaurant table with default rating 3.0.
        """
        cursor = self.conn.execute(
            """
            INSERT INTO restaurant (description, cuisine, address, image, rating, location_id)
            VALUES (?, ?, ?, ?, 3, ?)""",
            (description, cuisine, address, image, location_id)
        )
        self.conn.commit()
        return self.get_restaurant(cursor.lastrowid)


# Only <=1 instance of the database driver
# exists within the app at all times
DatabaseDriver = singleton(DatabaseDriver)
