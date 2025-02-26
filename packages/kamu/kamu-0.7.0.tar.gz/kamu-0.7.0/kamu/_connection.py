import adbc_driver_manager.dbapi
import pandas


class KamuConnection:
    """
    Base interface all connections implement
    """

    def url(self) -> str:
        """
        Returns the URL this connection was created with
        """
        raise NotImplementedError()

    def query(self, sql) -> pandas.DataFrame:
        """
        Execute SQL query and return result as Pandas DataFrame.
        """
        raise NotImplementedError()

    def as_adbc(self) -> adbc_driver_manager.dbapi.Connection:
        """
        Returns the underlying ADBC connection.

        Use this method when working with libraries that expect ADBC connection.

        Examples
        --------
        >>> import pandas
        >>> import kamu
        >>>
        >>> with kamu.connect() as con:
        >>>     pandas.read_sql("select 1", con.as_adbc())
        """
        raise NotImplementedError()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def close(self):
        """
        Close the connection and release all resources
        """
