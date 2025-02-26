import pymysql

from dump.config_utils import load_config


class ConnectorMySQL:
    def __init__(
        self,
        db_config_name: str = "postgres",
    ) -> None:
        self.db_config_name = db_config_name

        self.__config = load_config(section=self.db_config_name)
        self.__config["port"] = int(self.__config["port"])

        self._conn = None
        self._cursor = None

    @property
    def conn(self):
        if self._conn is None:
            try:
                self._conn = pymysql.connect(**self.__config)
            except pymysql.Error as error:
                raise error
        return self._conn

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    @property
    def close(self):
        self._conn.close()

        self._conn = None
        self._cursor = None

    @property
    def commit(self):
        self.conn.commit()

    def execute(self, query: str):
        self.cursor.execute(query)
        self.conn.commit()

    def fetchall(self, query: str) -> list:
        self.execute(query)
        values = self.cursor.fetchall()
        self.conn.commit()

        return values
