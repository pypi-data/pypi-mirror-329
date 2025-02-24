import pandas as pd
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column, types
from sqlalchemy.engine import reflection
import sqlalchemy

class PostgresqlBase:
    """
    PostgresqlBase is a base class for all postgresql databases
    """
    def __init__(self):
        self.id = ""
        self.credential = {
            "host": "",
            "port": "",
            "username": "",
            "password": "",
            "database_name": ""
        }

    def get_instance(self):
        """
        create a singleton instance of the class
        """
        self.instance = self.get_connect_psycopg2()
        return self.instance

    def get_connect_sqlalchemy(self, readonly=False) -> sqlalchemy.engine.Connection:
        """
        return sqlalchemy connection
        """
        engine = create_engine(
            f"postgresql://{self.credential['username']}:{self.credential['password']}@{self.credential['host']}:{self.credential['port']}/{self.credential['database_name']}"
        )
        return engine

    def get_connect_psycopg2(self, readonly=False) -> psycopg2.extensions.connection:
        """
        return psycopg2 connection
        """
        conn = psycopg2.connect(
            user=self.credential['username'],
            password=self.credential['password'],
            host=self.credential['host'],
            port=self.credential['port'],
            database=self.credential['database_name']
        )
        if readonly:
            conn.set_session(readonly=readonly)
        return conn

    def query(self, query_string: str) -> pd.core.frame.DataFrame:
        """
        return dataframe from query
        """
        conn = self.get_connect_psycopg2(readonly=False)
        df = pd.read_sql_query(query_string, conn)
        conn.close()
        return df

    def disconnect(self) -> bool:
        return True   

    def connect_orm(self, isPoolConnection: bool):
        """
        return orm library connection to client
        """
        return "lib_connection_here"    
    
    def get_info(self) -> str:
        """
        get source information from sdk server, low priority
        """
        return ""

    
    # TODO
    def create_table_from_dataframe(engine, df, table_name, metadata=None, dtype_mapping=None):
        """
        Creates a PostgreSQL table based on a Pandas DataFrame schema and optional metadata.

        Args:
            engine: SQLAlchemy engine connected to the PostgreSQL database.
            df: Pandas DataFrame representing the table structure.
            table_name: Name of the table to create.
            metadata: Optional SQLAlchemy MetaData object to attach the table to.  If None, one is created.
            dtype_mapping: Optional dictionary for custom data type mapping (e.g., {'my_column': types.Text}).
        """

        if metadata is None:
            metadata = MetaData()

        # Reflect existing table if it exists, otherwise create a new one
        try:
            inspector = reflection.Inspector.from_engine(engine)
            if table_name in inspector.get_table_names():
                print(f"Table '{table_name}' already exists. Skipping creation.")
                return  # Table already exists

        except Exception as e:
            print(f"Error during table reflection: {e}")
            raise  # Re-raise the exception

        columns = []
        for col_name, data_type in df.dtypes.items():
            sql_type = None

            # Default Pandas dtype to SQLAlchemy type mapping
            if pd.api.types.is_integer_dtype(data_type):
                sql_type = types.BigInteger  # Or Integer, SmallInteger, etc.
            elif pd.api.types.is_float_dtype(data_type):
                sql_type = types.Float  # Or Double
            elif pd.api.types.is_bool_dtype(data_type):
                sql_type = types.Boolean
            elif pd.api.types.is_datetime64_any_dtype(data_type):
                sql_type = types.DateTime
            else:
                sql_type = types.String(255)  # Default to String (adjust length as needed)

            # Apply custom mapping if provided
            if dtype_mapping and col_name in dtype_mapping:
                sql_type = dtype_mapping[col_name]

            if sql_type is None:
                raise ValueError(f"Could not infer SQL type for column '{col_name}'")

            columns.append(Column(col_name, sql_type))

        # Create the Table object
        table = Table(table_name, metadata, *columns)

        # Create the table in the database
        try:
            metadata.create_all(engine)
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
            raise

