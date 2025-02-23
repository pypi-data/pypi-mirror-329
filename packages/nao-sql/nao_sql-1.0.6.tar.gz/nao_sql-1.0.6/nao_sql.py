from pyodbc import Cursor, Connection, connect
import functools
import datetime
import decimal
from nao_logger import get_nao_logger

LOGGER = get_nao_logger('nao_sql')

data_type_map = {
    int: 'INTEGER',               # INTEGER in SQL for Python int
    float: 'REAL',                # REAL in SQL for Python float
    str: 'NVARCHAR(255)',         # TEXT in SQL for Python str. VARCHAR or NVARCHAR can be used in other SQL databases
    bool: 'BOOLEAN',              # BOOLEAN in SQL for Python bool (SQLite stores this as INTEGER 0 or 1)
    bytes: 'BLOB',                # BLOB in SQL for Python bytes
    datetime.date: 'DATE',        # DATE in SQL for Python datetime.date
    datetime.datetime: 'DATETIME',# DATETIME in SQL for Python datetime.datetime
    datetime.time: 'TIME',        # TIME in SQL for Python datetime.time
    decimal.Decimal: 'NUMERIC',   # NUMERIC in SQL for Python decimal.Decimal (useful for precise fixed-point arithmetic)
    list: 'TEXT',                 # Serialized list (e.g., JSON) stored as TEXT in SQL
    dict: 'TEXT',                 # Serialized dictionary (e.g., JSON) stored as TEXT in SQL
    None: 'NULL',                 # NULL in SQL for Python None
}

class Database:

    def __init__(self, server:str = None, database:str = None, **kwargs):
        """Initializes a new Database object with connection details.

        This class sets up the configuration for a database connection. It allows for different
        authentication methods and can be customized further with additional keyword arguments.

        Args:
            username (str, optional): The username for database login. It's required if the login method is not 'windows_auth'.
            password (str, optional): The password for database login. It's required if the login method is not 'windows_auth'.
            server (str, optional): The server address of the database.
            database (str, optional): The name of the specific database to connect to.
            **kwargs: Additional keyword arguments for more customization.
        """
        self.username:str = kwargs.get('username')
        self.password:str = kwargs.get('password')
        self.server:str = server
        self.database:str = database

        if self.username and self.password:
            self.connection:Connection = self.login_sql_server_authentication(self.server, self.database, self.username, self.password)

        else:
            self.connection:Connection = self.login_windows_authentication(self.server, self.database)

    def __str__(self) -> str:
        return self.server + '-' + self.database

    def login_windows_authentication(self, server: str,database: str) -> Connection:
        """
        Establishes a connection to a SQL Server database using provided credentials.

        :param server: The address of the SQL Server database (IP or hostname).
        :param database: The name of the database to connect to.

        :return: A pyodbc Connection object if the connection is successful, None otherwise.

        """
        connection = ('DRIVER={SQL Server};'
                f'Trusted_Connection=Yes;'
                f'SERVER={server};'
                f'DATABASE={database};')
        try:
            connection = connect(connection, timeout = 120)
            LOGGER.info('Connection Successful')
            return connection
        except Exception as e:
            LOGGER.error(f'{e}')
            return None
             
    def login_sql_server_authentication(self, server: str, database: str, username: str, password: str) -> Connection:
        """
        Establishes a connection to a SQL Server database using provided credentials.

        :param server: The address of the SQL Server database (IP or hostname).
        :param database: The name of the database to connect to.
        :param username: The username for database authentication.
        :param password: The password for database authentication.

        :return: A pyodbc Connection object if the connection is successful, None otherwise.

        """
        connection = ('DRIVER={SQL Server};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}')
        try:
            connection = connect(connection, timeout = 120)
            LOGGER.info('Connection Successful')
            return connection
        except Exception as e:
            LOGGER.critical(f'{e}')
            return None
    
    def __db_operation(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            connection: Connection = self.connection
            cursor = None
            try:
                cursor = connection.cursor()
                result = func(self, cursor, *args, **kwargs)
                connection.commit()
                return result
            except Exception as e:
                print(f'An error occurred: {e}')
                connection.rollback()
                return None
            finally:
                if cursor:
                    cursor.close()
        return wrapper
        
    @__db_operation
    def select(self, cursor: Cursor, table_name: str, cols='*', where: str = None, order_by: str = None, distinct: bool = False):
        # If cols is a list, convert it to a comma-separated string.
        if isinstance(cols, list):
            cols = ', '.join(cols)
        
        query = 'SELECT '
        if distinct:
            query += 'DISTINCT '
        query += f'{cols} FROM {table_name}'
        if where:
            query += f' WHERE {where}'
        if order_by:
            query += f' ORDER BY {order_by}'

        LOGGER.debug(f'Executing query: {query}')
        cursor.execute(query)
        
        # Extract column names from the cursor description.
        columns = [column[0] for column in cursor.description]
        
        # Fetch all rows and convert each row to a dict (with column names as keys).
        rows = cursor.fetchall()
        result_list = [dict(zip(columns, row)) for row in rows]
        
        return result_list

    @__db_operation
    def insert(self, cursor:Cursor, table_name:str, dict_data:dict=None):
        if dict_data:
            columns = list(dict_data.keys())
            values = list(dict_data.values())
        try:
            placeholders = ', '.join(['?' for _ in columns])
            statement = f'INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})'
            cursor.execute(statement, values)
            LOGGER.debug(f'SUCCESS: {statement}')
            self.connection.commit()
            return True
        except Exception as e:
            LOGGER.critical(f'FAILURE: {statement}')
            LOGGER.debug(e, exc_info=True)
            return False

    @__db_operation
    def statement(self, cursor:Cursor, statement:str):
        # To pass params to the statement, give the function a tuple. The statement will use the param tuple arguements in order. They replace the question marks in the statement, in order.
        try:
            cursor.execute(statement)
            LOGGER.debug(f'SUCCESS: {statement}')
            result = cursor.fetchall()
            self.connection.commit()
            return result
        except Exception as e:
            LOGGER.critical(f'FAILURE: {statement}')
            LOGGER.debug(e, exc_info=True)
            return False
        
    @__db_operation
    def get_definition(self, cursor:Cursor, table_name:str, schema_name:str='dbo'):
        columns = cursor.columns(table=table_name, schema=schema_name)
        columns_raw_dict = {}
        for column in columns:
            columns_raw_dict[column.column_name] = {
                'TABLE_CAT': column.table_cat,
                'TABLE_SCHEM': column.table_schem,
                'TABLE_NAME': column.table_name,
                'COLUMN_NAME': column.column_name,
                'DATA_TYPE': column.data_type,
                'TYPE_NAME': column.type_name,
                'COLUMN_SIZE': column.column_size,
                'BUFFER_LENGTH': column.buffer_length,
                'DECIMAL_DIGITS': column.decimal_digits,
                'NUM_PREC_RADIX': column.num_prec_radix,
                'NULLABLE': column.nullable,
                'REMARKS': column.remarks,
                'COLUMN_DEF': column.column_def,
                'SQL_DATA_TYPE': column.sql_data_type,
                'SQL_DATETIME_SUB': column.sql_datetime_sub,
                'CHAR_OCTET_LENGTH': column.char_octet_length,
                'ORDINAL_POSITION': column.ordinal_position,
                'IS_NULLABLE': column.is_nullable,
            }

        return columns_raw_dict