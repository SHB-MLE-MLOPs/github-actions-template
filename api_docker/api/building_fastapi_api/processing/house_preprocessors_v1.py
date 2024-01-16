# to handle datasets
# to save data in database using pipelines
# import the database connector to connect python and our database (MySQL here)
import mysql.connector
import pandas as pd
from mysql.connector import errorcode
# for fit_transform object compatible to scikit-learn
from sklearn.base import BaseEstimator, TransformerMixin


class SaveIntoMySQLDatabase(BaseEstimator, TransformerMixin):
    def __init__(self, schema_name, table_name, db_host, user, password):
        # Schema and table name
        self.schema_name = schema_name
        self.table_name = table_name
        self.db_host = db_host
        self.user = user
        self.password = password

        # # database connection settings
        # # Settings to connect to my local MySQL server
        # self.MySQL_db_connection_config = {
        #     "user": "root", # Specify the user (root here)
        #     "password": "!BUij44Nr1986", # Specify the local password to connect to MySQL server
        #     "host": "127.0.0.1", # localhost , # Specify the host (or IP adress) of MySQL server
        #     "database": self.schema_name, # Specify the schema name
        #     "raise_on_warnings": True
        # }
        # # Settings to connect to MySQL server running in container. you need to know the
        # container IP adress with command "docker inspect container_ID_or_container_name"
        # self.MySQL_db_connection_config = {
        #     "user": "root",
        #     "password": "root_password",
        #     "host": "172.17.0.2",
        #     "database": self.schema_name,
        #     "raise_on_warnings": True
        # }
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

        # test to know if connection with database is OK
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

        # # database connection settings
        # # Settings to connect to my local MySQL server
        # self.MySQL_db_connection_config = {
        #     "user": "root", # Specify the user (root here)
        #     "password": "!BUij44Nr1986", # Specify the local password to connect to MySQL server
        #     "host": "127.0.0.1", # localhost , # Specify the host (or IP adress) of MySQL server
        #     "database": self.schema_name, # Specify the schema name
        #     "raise_on_warnings": True
        # }

        # # Settings to connect to MySQL server running in container. you need to know the
        # # container IP adress with command "docker inspect container_ID_or_container_name"
        # self.MySQL_db_connection_config = {
        #     "user": "root",
        #     "password": "root_password",
        #     "host": "172.17.0.2",
        #     "database": self.schema_name,
        #     "raise_on_warnings": True
        # }

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

        # Test table creation
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
