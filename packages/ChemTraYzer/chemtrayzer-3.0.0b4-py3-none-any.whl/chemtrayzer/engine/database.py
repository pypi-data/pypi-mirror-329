"""
Helper classes to set up sqlite database
"""
from enum import Enum
import logging
import os
from pathlib import Path
import re
import sqlite3
from typing import Any


class DatabaseError(Exception):
    """base class for all database errors"""


class DBOpenModeError(DatabaseError):
    """raised when an operation is illegal due to the mode with which the
    database is opened, e.g. writing in READ mode or opening two instances in
    WRITE mode
    """


class IntegrityError(DatabaseError):
    """raised when the structural or relational integrity of the database is
    affected"""


class DBOpenMode(Enum):
    """deterimes mode with which a database is opened"""

    READ = 0  # read only mode
    WRITE = 1  # reading and writing possible, creates a database if


class Database:
    """A class to help create sqlite databases based on Python's sqlite3
    module.
    To create a database, simply inherit from this class and extend the
    ``_TABLES`` variable with the definition of the tables you want and define
    the version of the class:

    .. code::

        class MyDatabase(Database):

            _VERSION = {
                'MyDatabase': '2.1',
                # use the unpacking operator to keep the entries of the parent
                # class
                **Database._VERSION
            }
            _TABLES = {
                'my_table': [
                    ('first_column', 'integer'),
                    ('some_data', 'text'),
                    ('more_data', 'blob')
                ],
                **Database._TABLES
            }

    .. note::
        The ``_TABLES`` and ```_VERSION`` dictionaries need to be **extended**,
        not overwritten, a simple way to do so is the unpacking operator `**`
        oder the `update()` function.

    As a convention, database objects should offer methods that receive and
    return chemtrayzer objects (usually from the pacakge ``chemtrayzer.
    ctydata``). The method names should have the prefixes `list_`, `load_` and
    `save_` followed by a description of what kind of objects should be loaded
    or stored, e.g. ``load_TS_geometry(id)``. The `list_` functions should list
    ids of objects stored in the database which can than be passed to
    ``load_...(id)`` to retrieve a single object at a time.
    The ids are typically determined by the database itself and returned by the
    `save_` functions when saving a new object.

    A database should always be used as context manager, i.e.

    .. code::

        with MyDatabase('path/to/file.sqlite') as db:
            # now you can use the database
            obj_id = db.save_my_object(obj)

    Using context managers ensures that the internal connection to the database
    is properly opened and closed.

    .. note::
        Database classes should be given a version by extending the
        ``_VERSION`` dictionary. The keys in this dictionary can be any unique
        name corresponding to the database class, but it should be the class
        name. If non-optional columns/tables are added, the main version number
        should be increased. If optional columns are added, one only needs to
        increase the minor version.

    :arg path: path to the sqlite file
    :arg mode: open mode of the database
    :arg timeout: time in seconds to wait when a database file is locked
    :cvar _VERSION: used to check if the version of this class is compatible
                    with the database file. The version info is written into
                    the sqlite files when a new database is created. This dict
                    may be extended by child classes. That way each class in a
                    hierarchy can have a separate version.
    :cvar _TABLES: defines the tables of the database. The keys of the
                   dictionary are the table names, the values contains a list
                   of tuples, where each tuple corresponds to a column. Its
                   first element contains the column name, the second the sql
                   column type.
    :type _TABKES: dict
    """

    _VERSION = {"Database": "1.0"}
    _TABLES = {
        # table name: [
        #   (column name, column type),
        #   ...
        # ],
        "db_info": [("class", "text primary key"), ("version", "text")]
    }

    def __init__(
        self, path: os.PathLike, mode=DBOpenMode.WRITE, timeout: float = 10.0
    ) -> None:
        self._path = Path(path).absolute()
        self._con = None  # for connection to database
        self._mode = mode
        self.__timeout = timeout

        # create a new database if there is none
        if not self._path.is_file():
            self.__create()

    def __enter__(self):
        self.__connect()
        self.__check_version()
        self.__check_tables()
        return self

    def __connect(self):
        """connect to database"""
        if self._mode == DBOpenMode.WRITE:
            self._con = sqlite3.connect(
                self._path.as_uri() + "?mode=rw",
                uri=True,
                detect_types=sqlite3.PARSE_COLNAMES,
                timeout=self.__timeout,
            )
        elif self._mode == DBOpenMode.READ:
            self._con = sqlite3.connect(
                self._path.as_uri() + "?mode=ro",
                uri=True,
                detect_types=sqlite3.PARSE_COLNAMES,
                timeout=self.__timeout,
            )
        else:
            raise NotImplementedError(
                f"Cannot open database with mode {self._mode}"
            )

    def __create(self):
        """creates a new database file and sets up the tables"""

        if self._mode == DBOpenMode.READ:
            raise DBOpenModeError("Cannot create a new database in read mode.")

        # sqlite will not create empty parent directories
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True)

        con = sqlite3.connect(self._path.as_uri() + "?mode=rwc", uri=True)

        # use connectino as context manager to ensure that the database remains
        # locked between the execution of the statements
        with con:
            for sql in self._sql_table_schema().values():
                con.execute(sql)

            for cls_name, version in self._VERSION.items():
                con.execute("INSERT INTO db_info VALUES(?,?)",
                            (cls_name, version))

        # we still need to close the connection
        con.close()

        logging.info("Created new database at %s.", self._path)

    def _sql_table_schema(self) -> dict[str, str]:
        """creates SQL command to create tables based on self._TABLES

        :return: dictionary of sql texts to create the tables with the table
                 names as keys
        """
        schemata = {}

        for table, column_definitions in self._TABLES.items():
            schema = ", ".join(
                [f"{col} {col_type}" for col, col_type in column_definitions]
            )
            schemata[table] = f"CREATE TABLE {table} ({schema})"

        return schemata

    def __get_file_version(self, cls: str) -> tuple[int, int]:
        """
        gets the version of the database file

        :param cls: class name for which to check the version
        :return: major version, minor version
        """
        cur = self._con.execute(
            "SELECT version FROM db_info WHERE class=(?)", (cls,)
        )
        file_version = cur.fetchone()
        cur.close()

        # check if there even is an entry for the class
        if file_version is None:
            raise IntegrityError(
                f"Database object of type {cls} is"
                f' incompatible with sqlite file "{self._path}"'
            )

        file_version = file_version[0].split(".")
        return int(file_version[0]), int(file_version[1])

    def __check_version(self):
        """compares the version of the database file with the version of
        the database class"""

        for cls, version in self._VERSION.items():
            try:
                file_version = self.__get_file_version(cls)
                class_version = version.split(".")
                class_version = int(class_version[0]), int(class_version[1])

                # missmatch of major version is an error, while minor version
                # missmatch only leads to warning
                if file_version[0] != class_version[0]:
                    raise IntegrityError(
                        f"The version of the database is "
                        f"{file_version[0]}.{file_version[1]} while the "
                        f"version of class {cls} is {class_version[0]}."
                        f"{class_version[1]}."
                    )

                if file_version[1] < class_version[1]:
                    if self._mode == DBOpenMode.WRITE:
                        self._update_version(file_version, class_version)
                        file_version = self.__get_file_version(cls)
                    else:
                        logging.info(
                            "Could not update the database from "
                            "version %d.%d to %d.%d, because the database was "
                            "opened in read-only mode.",
                            file_version[0],
                            file_version[1],
                            class_version[0],
                            class_version[1],
                        )

                # after updating, check again
                if file_version[1] != class_version[1]:
                    logging.warning(
                        "The version of the database is %d.%d while"
                        " the version of class %s is %d.%d.",
                        file_version[0],
                        file_version[1],
                        cls,
                        class_version[0],
                        class_version[1],
                    )

            except sqlite3.Error as e:
                raise DatabaseError(
                    "The db_info table of the database may "
                    "be corrupted."
                ) from e

    def _update_version(
        self, old_version: tuple[int, int], new_version: tuple[int, int]
    ):
        """This function is called if the minor version of the database file is
        lower than the version of the class. It can be used to update the table
        structure or the data in the database, before it is checked."""

    def __check_tables(self):
        """checks wether the tables in the current database file are
        consistent with self._TABLES
        """
        actual_sql = {
            name: sql
            for name, sql in self._con.execute("SELECT name, sql "
                                               "FROM sqlite_master")
        }

        def extract_cols(sql: str):
            """extracts colum names and types from SQL of form: `CREATE TABLE
            name(column1 type1 [constraint 1], ... [, table constraint])`
            where table constraints may be UNIQUE(colum names) or
            PRIMARY KEY(column name)

            :return: a map that maps the column names to a tuple containing the
                    column type (all lowercase) as first element and a
                    constraint ("primary key" or "unique" or None) as second
                    element
            """
            sql = sql.replace("\n", " ")
            cols_str = sql.split("(", maxsplit=1)[1].rsplit(")", maxsplit=1)[0]

            # use negative look ahead to ignore commas in brackets
            pattern = r",(?![^\(]*\))"
            cols_str = re.split(pattern, cols_str)

            cols = {}

            pos = 0  # position in comma separated list (cols_str)

            for col in cols_str:
                # if we reach SQLite keywords, we have reached the table
                # constraints part of the query
                col = col.strip()
                if col.lower().startswith(("unique", "primary key")):
                    break

                # identifier (column names) by be enclosed by ", `, or [ and ]
                if '"' in col:
                    _, name, type_constr_str = col.split('"')
                elif "`" in col:
                    _, name, type_constr_str = col.split("`")
                elif "[" in col:
                    name, type_constr_str = col.split("]")
                    name = name.split("[")[1]
                else:
                    name, type_constr_str = col.split(maxsplit=1)

                # separate type from column constraints
                type_constr_str = type_constr_str.split(maxsplit=1)
                col_type = type_constr_str[0].strip().lower()
                if len(type_constr_str) == 2:
                    col_constr = type_constr_str[1].strip().lower()
                else:
                    col_constr = None

                cols[name] = (col_type, col_constr)
                pos += 1

            # constraints may also be defined at the end
            for constraint in cols_str[pos:]:
                constr_type, columns = constraint.split("(")
                columns = columns.split(")")[0].split(",")
                constr_type = constr_type.strip().lower()

                for col in columns:
                    col = col.strip()
                    # remove possible delimiters
                    col = col.replace('"', "")
                    col = col.replace("`", "")
                    col = col.replace("[", "")
                    col = col.replace("]", "")

                    cols[col] = (cols[col][0], constr_type)

            return cols

        for table, row_definitions in self._TABLES.items():
            # check that all tables are there (it is ok, if there are
            # additional tables in the file)
            if table not in actual_sql:
                raise IntegrityError(f"Table {table} not in database.")

            cols = extract_cols(actual_sql[table])

            for expected_name, expected_type_constr in row_definitions:
                expected_type_constr = expected_type_constr.split(maxsplit=1)
                expected_type = expected_type_constr[0].lower()
                if len(expected_type_constr) == 2:
                    expected_constr = expected_type_constr[1].lower()
                else:
                    expected_constr = None

                if expected_name not in cols:
                    raise IntegrityError(
                        f"Table {table} is missing expected "
                        f"column {expected_name}."
                    )

                col_type, col_constr = cols[expected_name]

                if col_type != expected_type:
                    raise IntegrityError(
                        f"Column {expected_name} in table "
                        f"{table} has wrong type. Expected: {expected_type},"
                        f" got: {col_type}"
                    )

                if col_constr != expected_constr:
                    raise IntegrityError(
                        f"Column {expected_name} in table "
                        f"{table} has wrong constraint. Expected: "
                        f'"{expected_constr}", got: "{col_constr}"'
                    )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._con.commit()
        self._con.close()
        self._con = None

    def __getattribute__(self, __name: str) -> Any:
        # enforce the use of a context for methods starting with load, save or
        # list
        if __name.startswith(("load", "save", "list")):
            # check if the method was called within a context (this works b/c
            # self._con is set in __enter__ and unset in __exit__)
            if self._con is None:
                raise DatabaseError(
                    f"load/save/list methods can only be called "
                    "inside a context. You can open a context via \n"
                    f"with {self.__class__.__name__}(...) as db:\n"
                    "    # here you can call load/save/list"
                )

        # very lazy way to enforce read-only mode, if this does not catch
        # everything, sqlite will, but with a more cryptic error message
        if __name.startswith("save") and self._mode == DBOpenMode.READ:
            raise DBOpenModeError(
                "Cannot save object, because database was "
                "opened in read-only mode."
            )

        # now we actually call the method that we want
        return object.__getattribute__(self, __name)