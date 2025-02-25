import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from typing import List, Dict, Any, Optional, Union
from yyyutils.decorator_utils import DecoratorUtils
from contextlib import contextmanager
import pandas as pd
import time
import os
import tempfile
from yyyutils.print_utils import PrintUtils

pr = PrintUtils(add_line=False)
op = PrintUtils.original_print


@DecoratorUtils.print_return_value_for_class()
class DatabaseUtils:
    """
    这是数据库工具类，封装了常用的数据库操作，包括连接池、查询、插入、删除等。
    """
    def __init__(self, host='localhost', user='root', port=3306, password='', charset='utf8mb4', max_connections=5,
                 database=None, always_print=True):
        """
        Initialize the database connection pool
        """
        self.host = host
        self.user = user
        self.port = port
        self.password = password
        self.charset = charset
        self.max_connections = max_connections
        self.pool = self._create_pool(database)
        self.database = database
        self.always_print = always_print
        pr.green = True
        print(f"Database connection pool initialized with host: {host}, user: {user}, database: {database}")
        pr.green = False

    def _create_pool(self, database):
        return MySQLConnectionPool(
            pool_name="mypool",
            pool_size=self.max_connections,
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=database,
            charset=self.charset
        )

    @contextmanager
    def get_connection(self):
        """
        Get a database connection from the pool
        """
        conn = self.pool.get_connection()
        try:
            yield conn
        except Exception as e:
            pr.red = True
            print(f"Database connection error: {e}")
            pr.red = False
            conn.rollback()
            raise
        finally:
            conn.close()

    def _execute_query(self, query: str, params: Optional[Union[tuple, List[tuple]]] = None, fetch: bool = True) -> \
            Optional[List[Dict[str, Any]]]:
        """
        Execute a query and return the result
        """
        start_time = time.time()
        try:
            with self.get_connection() as conn:
                if self.database and conn.database != self.database:
                    conn.database = self.database
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                if fetch:
                    result = cursor.fetchall()
                else:
                    result = None
                cursor.close()
                if not fetch:
                    conn.commit()
            execution_time = time.time() - start_time
            pr.green = True
            print(f"Query executed in {execution_time:.2f} seconds: {query} | {params}")
            pr.green = False
            return result
        except Exception as e:
            pr.red = True
            print(f"Query execution error: {query} | Params: {params} | Error: {e}")
            pr.red = False
            raise

    def open_database(self, database_name: str) -> None:
        """
        Select a database
        """
        self.database = database_name
        self.pool = self._create_pool(database_name)
        pr.green = True
        print(f"Database {database_name} selected.")
        pr.green = False

    def show_databases(self) -> List[str]:
        """
        Show all databases
        """
        result = self._execute_query("SHOW DATABASES")
        return [row['Database'] for row in result]

    def create_database(self, database_name: str) -> None:
        """
        Create a database
        """
        self._execute_query(f"CREATE DATABASE {database_name}", fetch=False)

    def drop_database(self, database_name: str) -> None:
        """
        Drop a database
        """
        self._execute_query(f"DROP DATABASE {database_name}", fetch=False)

    @DecoratorUtils.validate_input
    def create_table(self, table_name: str, columns_dict: Dict[str, str]) -> None:
        """
        Create a table
        """
        columns_str = ', '.join([f"{key} {value}" for key, value in columns_dict.items()])
        self._execute_query(f"CREATE TABLE {table_name} ({columns_str})", fetch=False)

    def drop_table(self, table_name: str) -> None:
        """
        Drop a table
        """
        self._execute_query(f"DROP TABLE {table_name}", fetch=False)

    def show_tables(self) -> List[str]:
        """
        Show all tables
        """
        result = self._execute_query("SHOW TABLES")
        return [list(row.values())[0] for row in result]

    @DecoratorUtils.validate_input
    def insert_data(self, table_name: str, columns_list: Optional[List[str]] = None,
                    values_list: List[tuple] = None) -> None:
        """
        Insert data into a table
        """
        if not values_list:
            pr.red = True
            print("No values provided for insertion.")
            pr.red = False
            return

        # 获取表的列信息
        column_info = self.get_table_format(table_name)
        default_values = {col['Field']: col['Default'] for col in column_info if col['Default'] is not None}

        max_length = len(column_info)

        new_values_list = []
        for value_tuple in values_list:
            new_tuple = list(value_tuple)

            # 填充缺失的值
            while len(new_tuple) < max_length:
                column_name = column_info[len(new_tuple)]['Field']
                new_tuple.append(default_values.get(column_name, None))

            new_values_list.append(tuple(new_tuple))

        # 构建插入 SQL 语句
        values_str = ', '.join(['%s'] * max_length)
        if columns_list is None:
            sql = f"INSERT INTO {table_name} VALUES ({values_str})"
        else:
            columns_str = ', '.join(columns_list)
            sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"

        # 扁平化新元组列表
        flat_values = [item for sublist in new_values_list for item in sublist]

        try:
            self._execute_query(sql, flat_values, fetch=False)
            pr.green = True
            print(f"Data inserted into table {table_name}")
            pr.green = False
        except Exception as e:
            pr.red = True
            print(f"Data insertion error: {sql} | Values: {new_values_list} | Error: {e}")
            pr.red = False
            raise

    def bulk_insert_csv(self, table_name, csv_file_path):
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                with open(csv_file_path, 'r') as csv_file:
                    temp_file.write(csv_file.read())
                temp_file_path = temp_file.name

            query = f"""
            LOAD DATA INFILE %s
            INTO TABLE {table_name}
            FIELDS TERMINATED BY ','
            ENCLOSED BY '"'
            LINES TERMINATED BY '\n'
            IGNORE 1 ROWS
            """
            self._execute_query(query, (temp_file_path,))
            os.remove(temp_file_path)  # 删除临时文件
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    @DecoratorUtils.validate_input
    def delete_data(self, table_name: str, condition_str_list: Optional[List[str]] = None,
                    restart_main_key: bool = False) -> None:
        """
        Delete data from a table
        """
        sql = f"DELETE FROM {table_name}"
        params = []
        if condition_str_list:
            if restart_main_key:
                raise ValueError("Cannot restart main key when using conditions.")
            condition_str = " AND ".join([f"{cond.split('=')[0].strip()} = %s" for cond in condition_str_list])
            sql += f" WHERE {condition_str}"
            for cond in condition_str_list:
                key, value = cond.split('=')
                params.append(value.strip())
        self._execute_query(sql, params, fetch=False)

        if restart_main_key:
            self._execute_query(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1", fetch=False)

    @DecoratorUtils.validate_input
    def update_data(self, table_name: str, set_values: Dict[str, Any],
                    condition_str_list: Optional[List[str]] = None) -> None:
        """
        Update data in a table with flexible conditions.
        """
        set_str = ', '.join([f"{key} = %s" for key in set_values.keys()])
        values = list(set_values.values())
        sql = f"UPDATE {table_name} SET {set_str}"

        if condition_str_list:
            condition_str = " AND ".join(condition_str_list)  # 直接使用 condition_str_list 中的条件
            sql += f" WHERE {condition_str}"

        # 执行更新操作
        try:
            self._execute_query(sql, values, fetch=False)
            pr.green = True
            print(f"Data updated in table {table_name}")
            pr.green = False
        except Exception as e:
            pr.red = True
            print(f"Data update error: {sql} | Values: {values} | Error: {e}")
            pr.red = False
            raise

    @DecoratorUtils.validate_input
    def query_data(self, table_name: str, columns_list: Optional[List[str]] = None,
                   condition_str_list: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Query data from a table
        """
        columns_str = "*" if columns_list is None else ', '.join(columns_list)
        sql = f"SELECT {columns_str} FROM {table_name}"
        params = []

        if condition_str_list:
            # 直接拼接条件字符串
            condition_str = " AND ".join(condition_str_list)  # 这里不再限制为 key=value
            sql += f" WHERE {condition_str}"

        # 调用执行查询
        return self._execute_query(sql, params)

    def execute_script(self, script: str) -> None:
        """
        Execute a multi-line SQL script
        """
        for statement in script.split(';'):
            if statement.strip():
                self._execute_query(statement, fetch=False)

    @contextmanager
    def transaction(self):
        """
        Transaction context manager
        """
        with self.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                pr.red = True
                print(f"Transaction error: {e}")
                pr.red = False
                raise

    @DecoratorUtils.validate_input
    def query_to_dataframe(self, query: str, params: Optional[Union[tuple, List[tuple]]] = None) -> pd.DataFrame:
        """
        Execute a query and return the result as a DataFrame
        """
        result = self._execute_query(query, params)
        return pd.DataFrame(result)

    @DecoratorUtils.validate_input
    def bulk_insert_same(self, table_name: str, data: List[Dict[str, Any]], batch_size: int = 1000) -> None:
        """
        Bulk insert data into a table
        """
        if not data:
            logger.warning("No data provided for bulk insert.")
            return

        columns = list(data[0].keys())
        placeholders = ', '.join(['%s'] * len(columns))
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                values = [tuple(row[col] for col in columns) for row in batch]
                cursor.executemany(sql, values)
            conn.commit()
            cursor.close()

    @DecoratorUtils.validate_input
    def create_table_if_not_exists(self, table_name: str, columns_dict: Dict[str, str]) -> None:
        """
        Create a table if it does not exist
        """
        columns_str = ', '.join([f"{key} {value}" for key, value in columns_dict.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self._execute_query(sql, fetch=False)

    def column_exists(self, table_name: str, column_name: str) -> bool:
        """
        Check if a column exists in a table
        """
        sql = """
            SELECT 1
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s AND COLUMN_NAME = %s
        """
        params = (table_name, column_name)
        result = self._execute_query(sql, params)
        return len(result) > 0

    def add_column(self, table_name: str, column_name: str, column_type: str) -> None:
        """
        Add a column to a table
        """
        if not self.column_exists(table_name, column_name):
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            self._execute_query(sql, fetch=False)
        else:
            print(f"Column '{column_name}' already exists in table '{table_name}'")

    def drop_column(self, table_name: str, column_name: str) -> None:
        """
        Drop a column from a table
        """
        if self.column_exists(table_name, column_name):
            sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            self._execute_query(sql, fetch=False)
        else:
            pr.red = True
            print(f"Column '{column_name}' does not exist in table '{table_name}'")
            pr.red = False

    def rename_table(self, old_name: str, new_name: str) -> None:
        """
        Rename a table
        """
        sql = f"ALTER TABLE {old_name} RENAME TO {new_name}"
        self._execute_query(sql, fetch=False)

    def get_table_format(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get the schema of a table
        """
        return self._execute_query(f"DESCRIBE {table_name}")

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists
        """
        result = self._execute_query(f"SHOW TABLES LIKE '{table_name}'")
        return len(result) > 0

    def get_row_count(self, table_name: str) -> int:
        """
        Get the row count of a table
        """
        result = self._execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
        return result[0]['count']

    def truncate_table(self, table_name: str) -> None:
        """
        Truncate a table
        """
        self._execute_query(f"TRUNCATE TABLE {table_name}", fetch=False)

    def get_column_names(self, table_name: str) -> List[str]:
        """
        Get the column names of a table
        """
        schema = self.get_table_format(table_name)
        return [column['Field'] for column in schema]

    @DecoratorUtils.validate_input
    def create_index(self, table_name: str, column_names: List[str], index_name: Optional[str] = None) -> None:
        """
        Create an index on a table
        """
        if index_name is None:
            index_name = f"idx_{'_'.join(column_names)}"
        columns = ', '.join(column_names)
        sql = f"CREATE INDEX {index_name} ON {table_name} ({columns})"
        self._execute_query(sql, fetch=False)

    def index_exists(self, table_name: str, index_name: str) -> bool:
        """
        Check if an index exists in a table
        """
        sql = """
            SELECT 1
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_NAME = %s AND INDEX_NAME = %s
        """
        params = (table_name, index_name)
        result = self._execute_query(sql, params)
        return len(result) > 0

    def drop_index(self, table_name: str, index_name: str) -> None:
        """
        Drop an index from a table
        """
        if self.index_exists(table_name, index_name):
            sql = f"DROP INDEX {index_name} ON {table_name}"
            self._execute_query(sql, fetch=False)
        else:
            pr.red = True
            print(f"Index '{index_name}' does not exist on table '{table_name}'")
            pr.red = False

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get the foreign keys of a table
        """
        sql = """
            SELECT 
                CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM 
                INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE 
                TABLE_NAME = %s
                AND REFERENCED_TABLE_NAME IS NOT NULL
            """
        params = (table_name,)
        return self._execute_query(sql, params)

    def optimize_table(self, table_name: str) -> None:
        """
        Optimize a table
        """
        self._execute_query(f"OPTIMIZE TABLE {table_name}", fetch=False)

    def get_create_table_statement(self, table_name: str) -> str:
        """
        Get the create table statement of a table
        """
        result = self._execute_query(f"SHOW CREATE TABLE {table_name}")
        return result[0]['Create Table']

    def backup_table(self, table_name: str, backup_table_name: str) -> None:
        """
        Backup a table
        """
        create_stmt = self.get_create_table_statement(table_name)
        create_backup_stmt = create_stmt.replace(f"CREATE TABLE `{table_name}`", f"CREATE TABLE `{backup_table_name}`")
        self._execute_query(create_backup_stmt, fetch=False)
        self._execute_query(f"INSERT INTO {backup_table_name} SELECT * FROM {table_name}", fetch=False)

    def restore_table(self, backup_table_name: str, target_table_name: str) -> None:
        """
        Restore a table from a backup
        """
        self.drop_table(target_table_name)
        self.rename_table(backup_table_name, target_table_name)

    def get_table_size(self, table_name):
        query = """
            SELECT 
                data_length, index_length
            FROM 
                information_schema.TABLES
            WHERE 
                table_schema = DATABASE()
                AND table_name = %s
        """
        result = self._execute_query(query, (table_name,))

        if result:
            return result[0].get('DATA_LENGTH', 0), result[0].get('INDEX_LENGTH', 0)
        else:
            return 0, 0

    def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get slow query logs
        """
        sql = f"""
            SELECT 
                start_time, user_host, query_time, lock_time, rows_sent, rows_examined, db, sql_text
            FROM 
                mysql.slow_log
            ORDER BY 
                query_time DESC
            LIMIT {limit}
            """
        return self._execute_query(sql)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            pr.red = True
            print(f"Exception occurred: {exc_type}, {exc_val}, {exc_tb}")
            pr.red = False
        return False

    class QueryBuilder:
        def __init__(self):
            self.select_columns = []
            self.from_table = ""
            self.where_conditions = []
            self.order_by = []
            self.group_by = []
            self.limit = None
            self.offset = None
            self.condition_connector = " AND "

        def select(self, *columns):
            self.select_columns.extend(columns)
            return self

        def from_(self, table):
            self.from_table = table
            return self

        def where(self, condition, connector=None):
            if connector:
                self.condition_connector = connector
            self.where_conditions.append(condition)
            return self

        def order_(self, *columns, asc=True):
            if asc:
                columns = [f"{col} ASC" for col in columns]
            else:
                columns = [f"{col} DESC" for col in columns]
            self.order_by.extend(columns)
            return self

        def group_(self, *columns):
            self.group_by.extend(columns)
            return self

        def limit_(self, limit):
            self.limit = limit
            return self

        def offset(self, offset):
            self.offset = offset
            return self

        def build_(self):
            if not self.select_columns:
                raise ValueError("No columns specified for SELECT")
            if not self.from_table:
                raise ValueError("No table specified for FROM")

            query = f"SELECT {', '.join(self.select_columns)} FROM {self.from_table}"
            if self.where_conditions:
                query += " WHERE " + self.condition_connector.join(self.where_conditions)
            if self.group_by:
                query += f" GROUP BY {', '.join(self.group_by)}"
            if self.order_by:
                query += f" ORDER BY {', '.join(self.order_by)}"
            if self.limit:
                query += f" LIMIT {self.limit}"
            if self.offset:
                query += f" OFFSET {self.offset}"
            return query


if __name__ == '__main__':
    with DatabaseUtils(host='localhost', user='root', password='13541Wky@') as db:
        db.open_database('test_db')

    print(DatabaseUtils.QueryBuilder().select().from_().where().build_())

