import pandas as pd
from sqlalchemy import create_engine, exc, engine
from snowflake.sqlalchemy import URL
import streamlit as st


def connect_to_snowflake(
    username: str,
    password: str,
    account: str,
    warehouse: str,
    database: str,
    schema: str,
) -> engine:
    """
    Connect to Snowflake using the specified credentials.
    Parameters:
    - username (str): Snowflake username
    - password (str): Snowflake password
    - account (str): Snowflake account name
    - warehouse (str): Snowflake warehouse name
    - database (str): Snowflake database name
    - schema (str): Snowflake schema name
    Returns:
    - Engine: SQLAlchemy Engine object for the connection
    """

    try:
        conn = create_engine(
            URL(
                user=username,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                schema=schema,
            )
        )
        return conn
    except exc.SQLAlchemyError as err:
        st.error(f"Error connecting to Snowflake: {err}")
        return None


def load_data_to_snowflake(df: pd.DataFrame, conn: engine, table: str) -> None:
    """
    Load data from a CSV file into a table in Snowflake.
    Parameters:
    - filepath (str): Path to the CSV file
    - engine (Engine): SQLAlchemy Engine object for the connection
    - table (str): Snowflake table name
    Returns:
    - None
    """
    try:
        # Load data to Snowflake
        df.to_sql(table, conn, if_exists="replace", index=False)
        st.success("Data loaded to Snowflake successfully")
        st.snow()
    except Exception as err:
        print(f"Error loading data to Snowflake: {err}")


def connect_to_postgres(
    username: str, password: str, host: str, port: str, database: str
) -> engine:
    """
    Connect to PostgreSQL using the specified credentials.
    Parameters:
    - username (str): PostgreSQL username
    - password (str): PostgreSQL password
    - host (str): PostgreSQL host name
    - port (str): PostgreSQL port
    - database (str): PostgreSQL database name
    Returns:
    - Engine: SQLAlchemy Engine object for the connection
    """
    try:
        conn = create_engine(
            f"postgresql://{username}:{password}@{host}:{port}/{database}"
        )
        return conn
    except exc.SQLAlchemyError as err:
        st.error(f"Error connecting to PostgreSQL: {err}")
        return None


def load_data_to_postgres(df: pd.DataFrame, conn: engine, table: str) -> None:
    """
    Load data from a CSV file into a table in PostgreSQL.
    Parameters:
    - df (pd.DataFrame): DataFrame containing the data to load
    - conn (engine): SQLAlchemy Engine object for the connection
    - table (str): PostgreSQL table name
    Returns:
    - None
    """
    try:
        # Load data to PostgreSQL
        df.to_sql(table, conn, if_exists="replace", index=False)
        st.success("Data loaded to PostgreSQL successfully")
        st.balloons()
    except Exception as err:
        st.error(f"Error loading data to PostgreSQL: {err}")


def main():
    st.title("Load Data to Databases")

    # Data to load to database(s)
    df = pd.read_csv("philox-testset-1.csv")

    # Get user input for data storage option
    storage_option = st.selectbox(
        "Select data storage option:", ["Snowflake", "PostgreSQL"]
    )

    @st.cache(allow_output_mutation=True)
    def reset_form_fields():
        user = ""
        password = ""
        account = ""
        warehouse = ""
        database = ""
        schema = ""
        table = ""
        host = ""
        port = ""

    if storage_option == "Snowflake":
        st.subheader("Enter Snowflake Credentials")
        # Get user input for Snowflake credentials
        user = st.text_input("Username:", value="TONY")
        password = st.text_input("Password:", type="password")
        account = st.text_input("Account:", value="jn27194.us-east4.gcp")
        warehouse = st.text_input("Warehouse:", value="NAH")
        database = st.text_input("Database:", value="SNOWVATION")
        schema = st.text_input("Schema:", value="PUBLIC")
        table = st.text_input("Table:")

        # Load the data to Snowflake
        if st.button("Load data to Snowflake"):
            if (
                user
                and password
                and account
                and warehouse
                and database
                and schema
                and table
            ):
                conn = connect_to_snowflake(
                    username=user,
                    password=password,
                    account=account,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                )
                if conn:
                    load_data_to_snowflake(df, conn, table)
            else:
                st.warning("Please enter all Snowflake credentials")

    elif storage_option == "PostgreSQL":
        st.subheader("Enter PostgreSQL Credentials")
        # Get user input for PostgreSQL credentials
        user = st.text_input("Username:", value="postgres")
        password = st.text_input("Password:", type="password")
        host = st.selectbox("Host:", ["localhost", "other"])
        if host == "other":
            host = st.text_input("Enter host:")
        port = st.text_input("Port:", value="5432")
        database = st.text_input("Database:", value="snowvation")
        table = st.text_input("Table:")

        # Load the data to PostgreSQL
        if st.button("Load data to PostgreSQL"):
            if user and password and host and port and database and table:
                conn = connect_to_postgres(
                    username=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database,
                )
                if conn:
                    load_data_to_postgres(df, conn, table)
            else:
                st.warning("Please enter all PostgreSQL credentials and table name")

    # Reset form fields when storage_option changes
    reset_form_fields()


if __name__ == "__main__":
    main()
