import sys

# import the database connector to connect python and our database (MySQL here)
import mysql.connector
# import neccessary library or module
import pandas as pd
from mysql.connector import errorcode
# for fit_transform object compatible to scikit-learn
# you need to write fit and transform method in child object construction
# base or mother object export from scikit-learn
# for getting and setting variables compatible to scikit-learn variables
from sklearn.base import BaseEstimator, TransformerMixin


# for data extraction from data base
class ExtractDataFromMySQLDatabase(BaseEstimator, TransformerMixin):
    def __init__(self, size, schema_name, table_name, db_host, user, password):
        # check if size input variable is integer
        if not isinstance(size, int):
            raise ValueError("size of row should be an integer")
        self.size = size
        # Schema and table name
        self.schema_name = schema_name
        self.table_name = table_name
        self.db_host = db_host
        self.user = user
        self.password = password

        # Settings to connect to MySQL server running in docker-compose.
        self.MySQL_db_connection_config = {
            "user": self.user,
            "password": self.password,
            "host": self.db_host,
            "database": self.schema_name,
            "raise_on_warnings": True,
        }

    def fetch_from_database(self):
        # test to know if connection with database is OK
        try:
            # connect to database with settings set in config
            self.conn = mysql.connector.connect(**self.MySQL_db_connection_config)
        except mysql.connector.Error as erreur:
            if erreur.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("username or password or both is not correct")
            elif erreur.errno == errorcode.ER_BAD_DB_ERROR:
                print("data base does not exist")
            else:
                print(erreur)
            exit()

        # define request action
        query = f"SELECT * FROM {self.table_name}"
        self.request_action = query

        # Create cursor, used to execute commands
        # create the link between data base and my python file
        self.curserFetch = self.conn.cursor()

        # # Make a test to ensure that schema and table exist
        # Execute the create table query
        if self.database_exists():
            print(f"Database '{self.schema_name}' exists.")
            # Execute the create table query
            if self.table_exists():
                print(f"Table '{self.table_name}' exists.")
            else:
                print(f"Table '{self.table_name}' does not exist.")
                sys.exit()
        else:
            print(f"Database '{self.schema_name}' does not exist.")
            sys.exit()

        # execute request to database with action and value
        data_to_fetch = self.query_with_fetchmany()

        # Execute insert of data into database
        # commit the data inserted in database
        self.conn.commit()

        # Close cursor & connection to database
        self.curserFetch.close()
        self.conn.close()

        return data_to_fetch

    def table_exists(self):
        query = (
            "SELECT TABLE_NAME "
            "FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s"
        )
        self.curserFetch.execute(query, (self.schema_name, self.table_name))
        return self.curserFetch.fetchone() is not None

    def database_exists(self):
        query = (
            "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s"
        )
        self.curserFetch.execute(query, (self.schema_name,))
        return self.curserFetch.fetchone() is not None

    def iter_row(self):
        while True:
            rows = self.curserFetch.fetchmany(self.size)
            if not rows:
                break
            for row in rows:
                yield row

    def query_with_fetchmany(self):
        db_data_list = []
        try:
            # execute request to database with action and value
            self.curserFetch.execute(self.request_action)
            # get data into list
            for row in self.iter_row():
                db_data_list.append(list(row))
            # Get all database columns into list
            columns_names = [i[0] for i in self.curserFetch.description]
            # Convert data from list to dataframe
            db_data_frame = pd.DataFrame(db_data_list, columns=columns_names)
        except mysql.connector.Error as e:
            print(e)

        return db_data_frame

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        # check if function input variable is dataframe
        if not isinstance(X, pd.DataFrame):
            raise ValueError("X should be a dataframe")

        # save data into MySQL data base
        db_data_frame = self.fetch_from_database()

        return db_data_frame


class SaveIntoMySQLDatabase(BaseEstimator, TransformerMixin):
    def __init__(self, schema_name, table_name, db_host, user, password):
        # Schema and table name
        self.schema_name = schema_name
        self.table_name = table_name
        self.db_host = db_host
        self.user = user
        self.password = password

        # Settings to connect to MySQL server running in docker-compose.
        self.MySQL_db_connection_config = {
            "user": self.user,
            "password": self.password,
            "host": self.db_host,
            "database": self.schema_name,
            "raise_on_warnings": True,
        }

    def save_into_database(self, dataframe):
        # so that we do not over-write the original dataframe
        dataframe_copy = dataframe.copy()

        # Convert Pandas DataFrame to a List of Tuples
        data_to_save = dataframe_copy.to_records(index=False).tolist()

        # test to know if connection with database is OK
        try:
            # connect to database with settings set in config
            self.conn = mysql.connector.connect(**self.MySQL_db_connection_config)
        except mysql.connector.Error as erreur:
            if erreur.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("username or password or both is not correct")
            elif erreur.errno == errorcode.ER_BAD_DB_ERROR:
                print("data base does not exist")
            else:
                print(erreur)
            exit()

        # define request action
        column_names = [
            "pclass",
            "name",
            "sex",
            "age",
            "sibsp",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "boat",
            "body",
            "homedest",
            "survived",
        ]
        query = (
            f"INSERT INTO {self.table_name} "
            f"({', '.join(column_names)}) "
            f"VALUES ({', '.join(['%s' for _ in column_names])})"
        )
        self.request_action = query
        # define request value
        self.request_value = data_to_save

        # Create cursor, used to execute commands
        # create the link between data base and my python file
        self.curserInsert = self.conn.cursor()

        # Create books table if none exists
        # Column names and data types specified in a Python list of tuples
        self.column_definitions = [
            ("id", "INT NOT NULL AUTO_INCREMENT PRIMARY KEY"),
            ("pclass", "INT"),
            ("name", "VARCHAR(55)"),
            ("sex", "VARCHAR(6)"),
            ("age", "FLOAT"),
            ("sibsp", "INT"),
            ("parch", "INT"),
            ("ticket", "VARCHAR(60)"),
            ("fare", "FLOAT"),
            ("cabin", "VARCHAR(20)"),
            ("embarked", "VARCHAR(5)"),
            ("boat", "VARCHAR(20)"),
            ("body", "VARCHAR(15)"),
            ("homedest", "VARCHAR(75)"),
            ("survived", "FLOAT"),
            ("time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]

        # SQL query to create a table with the specified column names and data types
        # Instantiate YourClass and call the method
        Instance = CreateTableQueryClass(
            schema_name=self.schema_name,
            table_name=self.table_name,
            column_definitions=self.column_definitions,
        )
        self.create_table_query = Instance.create_table_query()

        try:
            # Execute the create table query
            self.curserInsert.execute(self.create_table_query)
            print("Table created successfully!")
        except mysql.connector.Error as erreur:
            print(f"Error: {erreur}")

        # execute request to database with action and value
        self.curserInsert.executemany(self.request_action, self.request_value)

        # Execute insert of data into database
        # commit the data inserted in database
        self.conn.commit()

        # Close cursor & connection to database
        self.curserInsert.close()
        self.conn.close()

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError("X should be a dataframe")

        # so that we do not over-write the original dataframe
        X_copy = X.copy()

        # save data into MySQL data base
        self.save_into_database(X_copy)

        return X_copy


class SaveIntoMySQLDatabasebyEndpoint(BaseEstimator, TransformerMixin):
    def __init__(self, schema_name, table_name, db_host, user, password):
        # Schema and table name
        self.schema_name = schema_name
        self.table_name = table_name
        self.db_host = db_host
        self.user = user
        self.password = password

        # Settings to connect to MySQL server running in docker-compose.
        self.MySQL_db_connection_config = {
            "user": self.user,
            "password": self.password,
            "host": self.db_host,
            "database": self.schema_name,
            "raise_on_warnings": True,
        }

    def save_into_database(self, dataframe):
        # so that we do not over-write the original dataframe
        dataframe_copy = dataframe.copy()

        # Convert Pandas DataFrame to a List of Tuples
        data_to_save = dataframe_copy.to_records(index=False).tolist()

        # test to know if connection with database is OK
        try:
            # connect to database with settings set in config
            self.conn = mysql.connector.connect(**self.MySQL_db_connection_config)
        except mysql.connector.Error as erreur:
            if erreur.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("username or password or both is not correct")
            elif erreur.errno == errorcode.ER_BAD_DB_ERROR:
                print("data base does not exist")
            else:
                print(erreur)
            exit()

        # define request action
        column_names = [
            "pclass",
            "name",
            "sex",
            "age",
            "sibsp",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "boat",
            "body",
            "homedest",
            "pclass_mi",
            "age_mi",
            "sibsp_mi",
            "parch_mi",
            "fare_mi",
            "age_na_mi",
            "fare_na_mi",
            "age_outliers_mi",
            "sibsp_outliers_mi",
            "parch_outliers_mi",
            "fare_outliers_mi",
            "sex_female_mi",
            "cabin_Rare_mi",
            "cabin_Missing_mi",
            "cabin_B_mi",
            "embarked_S_mi",
            "embarked_Q_mi",
            "title_Mrs_mi",
            "title_Miss_mi",
            "title_Mr_mi",
            "survived",
            "feature_drift_statut",
            "concept_probability_drift_statut",
            "concept_accuracy_drift_statut",
            "target_drift_statut",
            "prior_probability_drift_statut",
        ]
        query = (
            f"INSERT INTO {self.table_name} "
            f"({', '.join(column_names)}) "
            f"VALUES ({', '.join(['%s' for _ in column_names])})"
        )
        self.request_action = query

        # define request value
        self.request_value = data_to_save

        # # Schema and table name
        # self.schema_name = "user_data"
        # self.table_name = "data_conserve_all"

        # Create cursor, used to execute commands
        # create the link between data base and my python file
        self.curserInsert = self.conn.cursor()

        # Create books table if none exists
        # Column names and data types specified in a Python list of tuples
        self.column_definitions = [
            ("id", "INT NOT NULL AUTO_INCREMENT PRIMARY KEY"),
            ("pclass", "INT"),
            ("name", "VARCHAR(55)"),
            ("sex", "VARCHAR(6)"),
            ("age", "FLOAT"),
            ("sibsp", "INT"),
            ("parch", "INT"),
            ("ticket", "VARCHAR(60)"),
            ("fare", "FLOAT"),
            ("cabin", "VARCHAR(20)"),
            ("embarked", "VARCHAR(5)"),
            ("boat", "VARCHAR(20)"),
            ("body", "VARCHAR(15)"),
            ("homedest", "VARCHAR(75)"),
            ("pclass_mi", "FLOAT"),
            ("age_mi", "FLOAT"),
            ("sibsp_mi", "FLOAT"),
            ("parch_mi", "FLOAT"),
            ("fare_mi", "FLOAT"),
            ("age_na_mi", "FLOAT"),
            ("fare_na_mi", "FLOAT"),
            ("age_outliers_mi", "FLOAT"),
            ("sibsp_outliers_mi", "FLOAT"),
            ("parch_outliers_mi", "FLOAT"),
            ("fare_outliers_mi", "FLOAT"),
            ("sex_female_mi", "FLOAT"),
            ("cabin_Rare_mi", "FLOAT"),
            ("cabin_Missing_mi", "FLOAT"),
            ("cabin_B_mi", "FLOAT"),
            ("embarked_S_mi", "FLOAT"),
            ("embarked_Q_mi", "FLOAT"),
            ("title_Mrs_mi", "FLOAT"),
            ("title_Miss_mi", "FLOAT"),
            ("title_Mr_mi", "FLOAT"),
            ("survived", "FLOAT"),
            ("time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]

        # SQL query to create a table with the specified column names and data types
        # Instantiate YourClass and call the method
        Instance = CreateTableQueryClass(
            schema_name=self.schema_name,
            table_name=self.table_name,
            column_definitions=self.column_definitions,
        )
        self.create_table_query = Instance.create_table_query()

        try:
            # Execute the create table query
            self.curserInsert.execute(self.create_table_query)
            print("Table created successfully!")
        except mysql.connector.Error as erreur:
            print(f"Error: {erreur}")

        # execute request to database with action and value
        self.curserInsert.executemany(self.request_action, self.request_value)

        # Execute insert of data into database
        # commit the data inserted in database
        self.conn.commit()

        # Close cursor & connection to database
        self.curserInsert.close()
        self.conn.close()

        # return dataframe

    # def close_curser_conn(self):
    # ## Close cursor & connection to database
    # self.curserInsert.close()
    # self.conn.close()

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            raise ValueError("X should be a dataframe")

        # so that we do not over-write the original dataframe
        X_copy = X.copy()

        # save data into MySQL data base
        self.save_into_database(X_copy)

        # close cursor and connection with data base
        # self.close_curser_conn()

        return X_copy


# create_table_script.py
class CreateTableQueryClass:
    def __init__(self, schema_name, table_name, column_definitions):
        # Schema and table name
        self.schema_name = schema_name
        self.table_name = table_name
        self.column_definitions = column_definitions

    def create_table_query(self):
        query = (
            f"CREATE TABLE IF NOT EXISTS {self.schema_name}.{self.table_name} ("
            f"{', '.join(f'{col} {data_type}' for col, data_type in self.column_definitions)}"
            ");"
        )
        return query
