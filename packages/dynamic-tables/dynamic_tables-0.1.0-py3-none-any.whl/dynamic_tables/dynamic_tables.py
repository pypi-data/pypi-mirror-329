# this is dynamic_tables.py

import psycopg2, re
from psycopg2 import sql

class DynamicTables:
    
    def __init__(self):
        """Initialize the class by calling self.initialize() to set up default values."""
        self.initialize()

    def initialize(self):
        """Sets up default attributes for the table structure."""
        self.column_list = []
        self.column_dynamic = ''
        self.table_prefix = 'dtbl_'
        self.table_name_dynamic = ''

    def connection_open(self, dbname, user, password, host):
        """Opens a connection to the PostgreSQL database and initializes the cursor."""
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cur = self.conn.cursor()

    def connectHC(self, dbname, user, password, host):
        """Helper function to open a connection using hardcoded credentials."""
        self.connection_open(dbname, user, password, host)

    def connectJSON(self):
        """Opens a database connection using credentials from a JSON config file."""
        import json
        with open("config.json") as config_file:
            config = json.load(config_file)
        self.conn = psycopg2.connect(**config)
        self.cur = self.conn.cursor()

    def connectENVS(self):
        """Opens a database connection using environment variables."""
        import os
        self.conn = psycopg2.connect(
            host=os.getenv("DTABLES_ENVS_PGSQL_HOST"),
            user=os.getenv("DTABLES_ENVS_PGSQL_USER"),
            password=os.getenv("DTABLES_ENVS_PGSQL_PASSWORD"),
            database=os.getenv("DTABLES_ENVS_PGSQL_DATABASE")
        )
        self.cur = self.conn.cursor()

    def connection_close(self):
        """Closes the database cursor and connection."""
        self.cur.close()
        self.conn.close()

    def close(self):
        """Alias for connection_close() to improve readability."""
        self.connection_close()

    def format_table_name(self, input_column):
        """Formats an input column name to create a valid table name."""
        cleaned = re.sub(r'[^a-zA-Z0-9_]', '', input_column)
        return self.table_prefix + cleaned

    def input(self, *args):
        """Handles data insertion by dynamically determining the table name and inserting values."""
        column_dict = {}
        self.table_name_dynamic = ''

        for column_number, (column_name, _) in enumerate(self.column_list):
            if column_name == self.column_dynamic:
                self.table_name_dynamic = self.format_table_name(args[column_number])
                column_dict[column_name] = args[column_number]
            else:
                column_dict[column_name] = args[column_number]

        if self.table_name_dynamic:
            self.create_table(self.table_name_dynamic, self.column_list)

        self.insert_data(self.table_name_dynamic, column_dict)

    def insert_data(self, table_name, data_dict):
        """Inserts data into a dynamically created table."""
        columns = data_dict.keys()
        values = list(data_dict.values())

        query = sql.SQL("""
            INSERT INTO {} ({})
            VALUES ({});
        """).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() for _ in columns)
        )

        self.cur.execute(query, values)
        self.conn.commit()

    def create_table(self, table_name, columns):
        """Creates a table dynamically if it does not already exist."""
        column_definitions = sql.SQL(", ").join(
            sql.SQL("{} {}").format(sql.Identifier(col_name), sql.SQL(col_type))
            for col_name, col_type in columns
        )

        query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                {}
            );
        """).format(sql.Identifier(table_name), column_definitions)

        self.cur.execute(query)
        self.conn.commit()

    def show_db(self):
        """Lists all available databases."""
        self.cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        for row in self.cur.fetchall():
            print(row)

    def show_tables(self):
        """Fetch and return a list of all table names."""
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = self.cur.fetchall()

        if tables:
            table_list = [table[0] for table in tables]  # Convert to a simple list of table names
            print("\n".join(table_list))  # Print for debugging
            return table_list
        else:
            print("No tables found.")
            return []  # Return an empty list instead of None

    def show_columns(self, table_name):
        """Displays all columns and their data types for a given table."""
        try:
            query = sql.SQL("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """)
            self.cur.execute(query, (table_name,))
            columns = self.cur.fetchall()

            if columns:
                print(f"Columns in table '{table_name}':")
                for column_name, data_type in columns:
                    print(f" - {column_name}: {data_type}")
            else:
                print(f"No columns found for table '{table_name}' or the table does not exist.")
        except Exception as e:
            print(f"Error retrieving columns for '{table_name}': {e}")

    def show_columns_all(self):
        """Lists column details for all tables."""
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        for table in self.cur.fetchall():
            self.show_columns(table[0])

    def select_table(self, table_name):
        """Retrieves and prints all rows from the specified table."""
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        self.cur.execute(query)
        rows = self.cur.fetchall()

        if rows:
            for row in rows:
                print(f"Row: {row}")
        else:
            print(f"Table '{table_name}' exists but has no data.")

        return rows

    def delete_tables(self):
        """Deletes all tables that match the current table prefix."""
        query = """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name LIKE %s;
        """
        prefix_pattern = self.table_prefix + "%"  # Dynamic prefix
        print("prefix_pattern:" + prefix_pattern)  # Debugging output
        self.cur.execute(query, (prefix_pattern,))

        tables = self.cur.fetchall()
        print("DEBUG - Found tables to delete:", tables)  # Debugging output

        for table in tables:
            table_name = table[0]
            print(f"Dropping table: {table_name}")

            drop_query = sql.SQL("DROP TABLE IF EXISTS {} CASCADE;").format(sql.Identifier(table_name))
            self.cur.execute(drop_query)

        self.conn.commit()

    def set_columns(self, input_columns):
        """Sets the columns for table creation based on user input."""
        self.column_list = []
        for column in input_columns.split(','):
            column = column.strip()
            parts = column.split(maxsplit=1)
            if len(parts) == 2:
                self.column_list.append((parts[0], parts[1]))
            else:
                print(f"Invalid column format: '{column}'")

    def set_table_prefix(self, input_prefix):
        """Defines a custom table name prefix."""
        self.table_prefix = input_prefix

    def set_dynamic_column(self, input_column):
        """Sets the column that determines dynamic table names."""
        self.column_dynamic = input_column

    def status(self):
        """Displays the currently configured column settings."""
        print('\nConfigured Columns:')
        for column in self.column_list:
            print(column)
        print('\nDynamic Column:\n', self.column_dynamic, '\n')

