from sqlalchemy import create_engine, Column, Integer, MetaData, Table
from sqlalchemy import Integer, String, Text, Boolean, Float, DateTime, Date, Time, LargeBinary, ForeignKey
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus


class Database:
    def __init__(self, username, password, host, port, database):
        encoded_password = quote_plus(password)
        self.engine = create_engine(f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.tables = {table_name: Table(table_name, self.metadata, autoload_with=self.engine) for table_name in self.metadata.tables}

    def define_table(self, name, **columns):
        """Dynamically define a table and ensure it exists in the database"""
        if name in self.tables:
            return self.tables[name]

        columns_def = [Column("id", Integer, primary_key=True, autoincrement=True)]
        for col_name, col_type in columns.items():
            columns_def.append(Column(col_name, col_type))

        new_table = Table(name, self.metadata, *columns_def)
        new_table.create(self.engine)
        self.metadata.reflect(bind=self.engine)
        self.tables[name] = new_table
        return new_table

    def insert(self, table, **data):
        """Insert a record into a table"""
        if table not in self.tables:
            raise ValueError(f"Table '{table}' does not exist.")
        stmt = self.tables[table].insert().values(**data)
        with self.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    def search(self, table, json=False, **filters):
        """Search records in a table with optional filters"""
        if table not in self.tables:
            raise ValueError(f"Table '{table}' does not exist.")
        stmt = select(self.tables[table])
        for key, value in filters.items():
            stmt = stmt.where(self.tables[table].c[key] == value)
        with self.engine.connect() as conn:
            results = [dict(row._mapping) for row in conn.execute(stmt).fetchall()]
        return results if json else results

    def get(self, table, json=False, **filters):
        """Fetch a single record based on filters (like an ID)"""
        results = self.search(table, json=True, **filters)
        return results[0] if results else None

    def update(self, table, filters, updates):
        """Update records in a table"""
        if table not in self.tables:
            raise ValueError(f"Table '{table}' does not exist.")
        stmt = self.tables[table].update()
        for key, value in filters.items():
            stmt = stmt.where(self.tables[table].c[key] == value)
        stmt = stmt.values(**updates)
        with self.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    def delete(self, table, **filters):
        """Delete records from a table"""
        if table not in self.tables:
            raise ValueError(f"Table '{table}' does not exist.")
        stmt = self.tables[table].delete()
        for key, value in filters.items():
            stmt = stmt.where(self.tables[table].c[key] == value)
        with self.engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    def list_tables(self):
        """List all tables in the database"""
        return list(self.tables.keys())
