import pandas as pd


def export_to_sql_statements(
    df: pd.DataFrame, file_name_with_extension: str, table_name: str = "my_table"
) -> None:
    """
    Generates a raw SQL file containing a CREATE TABLE statement and INSERT INTO statements
    for the provided DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to export.
        file_name_with_extension (str): Full file name (including `.sql` extension) to save the SQL file.
        table_name (str): Table name for the SQL statements.
    """
    with open(file_name_with_extension, "w") as f:
        # Write a CREATE TABLE statement
        columns = ",\n".join([f"    `{col}` TEXT" for col in df.columns])
        create_statement = (
            f"CREATE TABLE IF NOT EXISTS {table_name} (\n{columns}\n);\n\n"
        )
        f.write(create_statement)

        # Write INSERT INTO statements
        for _, row in df.iterrows():
            values = [
                f"'{str(v).replace('\'', '\'\'')}'" if isinstance(v, str) else str(v)
                for v in row
            ]
            values_str = ", ".join(values)
            insert_statement = f"INSERT INTO {table_name} VALUES ({values_str});\n"
            f.write(insert_statement)


def export_dataframe(df, file_name, format=".csv", table_name="my_table", **kwargs):
    """
    Exports a Pandas DataFrame to a specified file format, including raw SQL `INSERT` statements.

    Parameters:
        df (pd.DataFrame): The DataFrame to export.
        file_name (str): The file name (without extension) to export the DataFrame to.
        format (str): The file format (e.g., '.csv', '.json', '.xlsx', '.sql', '.parquet', etc.).
        table_name (str): Table name for SQL `INSERT` statements (used only when format='.sql').
        **kwargs: Additional keyword arguments for Pandas export functions.

    Returns:
        str: The full file name of the exported file.
    """
    try:
        file_name_with_extension = f"{file_name}{format}"

        # Export logic for supported formats
        if format == ".csv":
            df.to_csv(file_name_with_extension, index=False, **kwargs)
        elif format == ".json":
            df.to_json(file_name_with_extension, orient="records", **kwargs)
        elif format == ".xlsx":
            df.to_excel(file_name_with_extension, index=False, **kwargs)
        elif format == ".parquet":
            df.to_parquet(file_name_with_extension, index=False, **kwargs)
        elif format == ".html":
            df.to_html(file_name_with_extension, index=False, **kwargs)
        elif format == ".pkl":
            df.to_pickle(file_name_with_extension, **kwargs)
        elif format == ".txt":
            df.to_csv(file_name_with_extension, index=False, sep="\t", **kwargs)
        elif format == ".sql":
            export_to_sql_statements(df, file_name_with_extension, table_name)
        else:
            raise ValueError(f"Unsupported file format: {format}")

        print(f"DataFrame exported successfully to {file_name_with_extension}")
        return file_name_with_extension

    except Exception as e:
        print(f"Error exporting DataFrame: {e}")
        return None
