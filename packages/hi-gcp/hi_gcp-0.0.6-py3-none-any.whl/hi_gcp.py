# ************************************************************************************
# ***                C O N F I D E N T I A L  --  B A M A                          ***
# ************************************************************************************
# *                                                                                  *
# *                Project Name : GCP Utilities                             *
# *                                                                                  *
# *                File Name : gcp_classes_windsurf.py                               *
# *                                                                                  *
# *                Programmer : Jinwen Liu                                          *
# *                                                                                  *
# *                Start Date : December 20, 2024                                    *
# *                                                                                  *
# *                Last Update : December 20, 2024                                   *
# *                                                                                  *
# *                Version : 1.0.0                                                  *
# *                                                                                  *
# *-------------------------------------------------------------------------------*
# * Functions:                                                                      *
# *   BigQueryClient -- Main class for interacting with Google BigQuery            *
# *   - __init__ -- Initializes the BigQuery client                                *
# *   - show -- Prints the current state of the BigQuery client                     *
# *   - close -- Closes the BigQuery client and cleans up resources                *
# *   - set_key_file -- Sets the key file for the BigQuery client                  *
# *   - set_table_id -- Sets the table ID for the BigQuery client                  *
# *   - head -- Returns the first N rows of the current table                      *
# *   - set_sql -- Sets the SQL query string                                       *
# *   - run_sql -- Runs the SQL query                                              *
# *   - show_sql -- Executes a SQL query and displays the results                  *
# *   - delete_table -- Deletes a table from the BigQuery dataset                  *
# *  - clean_table -- Deletes all records from a table while preserving its structure
# *   - sql2df -- Executes a SQL query and returns the result as a pandas DataFrame*
# *   - df2table -- Loads a pandas DataFrame into a BigQuery table                 *
# *   - table2df -- Retrieves data from a BigQuery table and converts it into a    *
#                  pandas DataFrame                                               *
#   - table2storage -- Extracts data from a BigQuery table and saves it to Google *
#                      Cloud Storage                                              *
# *******************************************************************************
# gcp_classes.py improved by windsurf version 2
from typing import Optional, Dict, List, Any, Union
import pandas as pd
from google.cloud import bigquery, storage
from google.oauth2 import service_account
from google.api_core import exceptions as google_exceptions
import datetime
import pandas_gbq
import os
from google.api_core import exceptions
import pyarrow.parquet as parquet
from pathlib import Path
import json
import dotenv

class BigQueryClient:
    def __init__(
        self,
        project_id: str = None,
        dataset_id: str = None,
        table_id: str = None,
        key_file: Optional[str] = None,
        admin_password: str = None
    ):

        # These three environment variables are must
        self.project_id: str = project_id or os.getenv('GCP_PROJECT_ID')
        if not self.project_id:
            raise Exception("project_id must be provided or set in GCP_PROJECT_ID environment variable")

        self.dataset_id: str = dataset_id or os.getenv('BQ_DATASET_ID')
        if not self.dataset_id:
            raise Exception("dataset_id must be provided or set in BQ_DATASET_ID environment variable")

        # Get key_file from environment if not provided
        self.key_file: Optional[str] = key_file or os.getenv('GCP_KEY_FILE')
        if not self.key_file:
            raise Exception("key_file must be provided or set in GCP_KEY_FILE environment variable")


        self.bucket_name = ''
        self.table_id = table_id or 'you_need_to_set_table_id'  # Use provided table_id or default to 'corr_pair'
        try:
            self.sql = f"SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}` LIMIT 10"
        except:
            self.sql = None
        self.output_path = '/tmp/data/bigquery_output/'
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)
        
        self.credentials = None
        # self.full_table_id = None
        self.job_config = None
        # will create a folder by default to store temp data
        self.default_path = Path('/tmp/data/bigquery/')
        if not self.default_path.exists():
            self.default_path.mkdir(parents=True)

        if self.key_file:
            self.credentials = service_account.Credentials.from_service_account_file(
                self.key_file,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            self.client = bigquery.Client(
                credentials=self.credentials,
                project=self.project_id,
            )
        
        try:
            self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        except:
            self.full_table_id = None

        try:
            self.client = bigquery.Client(credentials=self.credentials)
        except:
            self.client = None                                                
        
        # Initialize admin password for sensitive operations
        self._admin_password = admin_password or os.getenv('BQ_ADMIN_PASSWORD')
        if not self._admin_password:
            self._admin_password = "default_admin_password"  # You should change this in production

    # ==============================================================================
    def show(self) -> None:
        """Print the current state of the BigQueryClient.
        
        Displays all relevant configuration and state information including:
        - GCP configuration (project, dataset, table)
        - Client status
        - File paths and storage information
        - Current SQL query
        """
        # Use a consistent format for better readability
        config_info = {
            "GCP Configuration": {
                "Project ID": self.project_id,
                "Dataset ID": self.dataset_id,
                "Table ID": self.table_id or "Not set",
                "Full Table ID": self.full_table_id or "Not set",
                "Bucket Name": self.bucket_name or "Not set"
            },
            "Query Configuration": {
                "Current SQL": self.sql or "Not set"
            },
            "Client Status": {
                "BigQuery Client": "Initialized" if self.client else "Not initialized",
                "Credentials": "Set" if self.credentials else "Not set"
            },
            "File Configuration": {
                "Default Path": str(self.default_path),
                "Key File": self.key_file or "Not set",
                "Output Path": str(self.output_path) if self.output_path else "Not set"
            }
        }

        # Print with clear section formatting
        for section, details in config_info.items():
            print(f"\n{section}:")
            print("-" * (len(section) + 1))
            for key, value in details.items():
                print(f"{key:15}: {value}")
    # ==============================================================================
    def close(self) -> None:
        """Close the BigQuery client and clean up resources.
        
        This method ensures proper cleanup of the BigQuery client connection
        and associated resources. If no client exists, it will return silently.
        
        The method will attempt to clean up all resources even if an error occurs
        during client closure.
        """
        if not hasattr(self, 'client') or self.client is None:
            return
        
        try:
            self.client.close()
        except Exception as e:
            print(f"Warning: Error while closing client: {str(e)}")
        finally:
            # Clean up instance variables even if close() fails
            self.client = None
            self.credentials = None
            self.job_config = None
            self.full_table_id = None
            self.sql = None
    # ==============================================================================
    def set_key_file(self, key_file):
        self.key_file = key_file
        self.credentials = service_account.Credentials.from_service_account_file(
                            self.key_file,
                            scopes=["https://www.googleapis.com/auth/cloud-platform"],
                            )
        if self.credentials:
            self.client = bigquery.Client(credentials=self.credentials,
                                            project=self.credentials.project_id)
        if self.credentials.project_id:
            self.project_id = self.credentials.project_id            


    def set_table_id(self, table_id: str) -> None:
        """
        Set the BigQuery table ID and update the default SQL query.

        Args:
            table_id (str): The ID of the table to use.

        Raises:
            ValueError: If table_id is None or empty.
        """
        if not isinstance(table_id, str) or not table_id.strip():
            raise ValueError("table_id must be a non-empty string")
            
        self.table_id = table_id.strip()
        
        # Update the full table ID
        self.full_table_id = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        
        # Update the default SQL query
        self.sql = f"SELECT * FROM `{self.full_table_id}` LIMIT 10"
        
        print(f"Table ID set to: {self.table_id}")
        print(f"Full table ID updated: {self.full_table_id}")
        print(f"Default SQL query updated: {self.sql}")


    # ==============================================================================
    def head(self, limit: int = 10) -> pd.DataFrame:
        """
        Return the first N rows of the current table.

        Args:
            limit (int, optional): Number of rows to return. Defaults to 10.
                                 Must be a positive integer.

        Returns:
            pandas.DataFrame: DataFrame containing the first N rows of the table.

        Raises:
            ValueError: If table_id is not set or if limit is invalid.
            google.api_core.exceptions.GoogleAPIError: If the query fails.
        """
        if not hasattr(self, 'table_id') or self.table_id is None:
            raise ValueError("table_id must be set before calling head()")
            
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer")

        query = f"SELECT * FROM `{self.project_id}.{self.dataset_id}.{self.table_id}` LIMIT {limit}"
        print(f"Executing query: {query}")
        
        try:
            return self.client.query(query).to_dataframe()
        except Exception as e:
            raise Exception(f"Failed to execute query: {str(e)}") from e
        
    # ==============================================================================
    def set_sql(self, sql: str) -> None:
        """Set the SQL query string.

        Args:
            sql (str): The SQL query to execute.

        Raises:
            ValueError: If sql is None or empty.
        """
        if not sql or not isinstance(sql, str):
            raise ValueError("sql must be a non-empty string")
        self.sql = sql

    # ==============================================================================
    def run_sql(self, sql=None):
        if sql is None:
            sql = self.sql
        self.client.query(sql)
        print ("query run complete")

    # ==============================================================================
    def show_sql(self, sql: str = None) -> None:
        """
        Executes a SQL query and displays the results as a DataFrame. 
        If the query doesn't have a LIMIT clause, adds LIMIT 10.

        Args:
            sql (str, optional): SQL query to execute. If not provided, uses the stored SQL query.

        Returns:
            None. Displays the query results as a DataFrame.

        Raises:
            ValueError: If no SQL query is available.
            Exception: If the query execution fails.
        """
        if sql is None:
            sql = self.sql
            
        if not sql:
            raise ValueError("No SQL query provided or stored")

        try:
            # Convert query to lowercase for case-insensitive search
            sql_lower = sql.lower()
            
            # If query doesn't have LIMIT, add LIMIT 10
            if 'limit' not in sql_lower:
                sql = f"{sql} LIMIT 10"
                print(f"Added LIMIT 10 to query: {sql}")
            
            # Execute query and convert to DataFrame
            df = self.client.query(sql).to_dataframe()
            print(f"\nQuery results ({len(df)} rows):")
            print(df)
            
        except Exception as e:
            raise Exception(f"Failed to execute query: {str(e)}") from e

    # ==============================================================================
    # Added PROTECTED_TABLES class attribute
    PROTECTED_TABLES = {
        'pair_corr_V3',  # Main correlation pairs table
        'fear_and_greed_index', # Stock metadata
        'stock_prices', # Daily price data
        "test" # to test
    }

    def delete_table(self, table_id: str, password: str) -> None:
        """
        Delete a table from the BigQuery dataset.

        Args:
            table_id (str): ID of the table to delete.
            password (str): Admin password required for deletion.

        Raises:
            ValueError: If table_id is empty, invalid, or protected, or if password is incorrect.
            Exception: If deletion fails.
        """
        # Verify password
        if password != self._admin_password:
            raise ValueError("Incorrect admin password provided")

        try:
            # Validate table_id
            if not isinstance(table_id, str) or not table_id.strip():
                raise ValueError("table_id must be a non-empty string")
            
            # Check if table is protected
            if table_id in self.PROTECTED_TABLES:
                raise ValueError(f"Cannot delete protected table '{table_id}'. Protected tables: {sorted(self.PROTECTED_TABLES)}")

            # Delete table
            table_path = f"{self.project_id}.{self.dataset_id}.{table_id}"
            self.client.delete_table(table_path, not_found_ok=True)
            print(f"Successfully deleted table '{table_id}' from dataset '{self.dataset_id}'")
            
        except Exception as e:
            raise Exception(f"Failed to delete table '{table_id}': {str(e)}") from e


    def clean_table(self, table_id: str, password: str) -> None:
        """
        Clean all records from a table while preserving its structure.

        Args:
            table_id (str): ID of the table to clean. This parameter is required.
            password (str): Admin password required for cleaning.

        Raises:
            ValueError: If password is incorrect.
            Exception: If cleaning fails or table_id is not provided.
        """
        # Verify password
        if password != self._admin_password:
            raise ValueError("Incorrect admin password provided")

        if not table_id:
            raise ValueError("table_id must be provided")
            
        try:
            # Construct the DELETE query
            query = f"DELETE FROM `{self.project_id}.{self.dataset_id}.{table_id}` WHERE true"
            
            # Execute the query
            query_job = self.client.query(query)
            query_job.result()  # Wait for the job to complete
            
            print(f"Successfully cleaned all records from table '{table_id}'.")
        except Exception as e:
            raise Exception(f"Failed to clean table '{table_id}': {str(e)}") from e


    def add_columns(
            self,
            table_id: str,
            new_columns: Dict[str, str]
        ) -> None:
        """
        Add new columns to an existing BigQuery table.

        Args:
            table_id (str): ID of the table to modify.
            new_columns (Dict[str, str]): Dictionary mapping column names to their BigQuery data types.
                Example: {'new_col1': 'STRING', 'new_col2': 'INTEGER'}

        Raises:
            ValueError: If table_id is empty or new_columns is empty/invalid.
            Exception: If adding columns fails.
        """
        if not table_id:
            raise ValueError("table_id must be provided")
        if not new_columns or not isinstance(new_columns, dict):
            raise ValueError("new_columns must be a non-empty dictionary")

        try:
            # Get the table reference
            table_ref = self.client.dataset(self.dataset_id).table(table_id)
            table = self.client.get_table(table_ref)

            # Create SchemaField objects for the new columns
            new_schema_fields = [
                bigquery.SchemaField(name, type_)
                for name, type_ in new_columns.items()
            ]

            # Combine existing schema with new columns
            original_schema = table.schema
            updated_schema = original_schema + new_schema_fields

            # Update the table with the new schema
            table.schema = updated_schema
            self.client.update_table(table, ['schema'])

            print(f"Successfully added columns {list(new_columns.keys())} to table '{table_id}'")
        except Exception as e:
            raise Exception(f"Failed to add columns to table '{table_id}': {str(e)}") from e


    # ==============================================================================
    def sql2df(self, sql: str = None) -> pd.DataFrame:
        """
        Execute a SQL query and return the results as a pandas DataFrame.

        Args:
            sql (str, optional): SQL query to execute. If not provided, uses the stored SQL query.

        Returns:
            pd.DataFrame: DataFrame containing the query results.

        Raises:
            ValueError: If no SQL query is available or if query is empty.
            Exception: If query execution fails.
        """
        if sql is None:
            if not hasattr(self, 'sql') or not self.sql:
                raise ValueError("No SQL query provided and no default SQL query set")
            sql = self.sql

        if not isinstance(sql, str) or not sql.strip():
            raise ValueError("SQL query must be a non-empty string")

        try:
            # Execute query and return as DataFrame
            df = self.client.query(sql).to_dataframe()
            
            print(f"Successfully executed query and retrieved {len(df)} rows")
            return df
            
        except Exception as e:
            raise Exception(f"Failed to execute query: {str(e)}") from e

    # ==============================================================================
    def df2table(
        self,
        df: pd.DataFrame,
        table_id: str,
        loading_method: str = 'load_parquet',
        if_exists: str = 'append',
        add_dump_date: bool = True
    ) -> None:
        """
        Load a pandas DataFrame into a BigQuery table using service account authentication.

        Args:
            df (pd.DataFrame): The DataFrame to be loaded.
            table_id (str): The ID of the table in BigQuery.
            loading_method (str, optional): Method to use for loading data.
                Options are 'load_parquet' (default) or 'load_csv'.
            if_exists (str, optional): Action to take if table exists.
                Options are 'append' (default), 'replace', or 'fail'.
            add_dump_date (bool, optional): If True, adds a 'data_dump_date' column 
                with current timestamp. Defaults to True.

        Raises:
            ValueError: If df is empty or table_id is invalid.
            Exception: If the upload fails.

        Example:
            >>> client.df2table(df, 'my_table')  # Appends data using parquet
            >>> client.df2table(df, 'my_table', loading_method='load_csv', if_exists='replace')  # Replaces using CSV
        """
        # Validate inputs
        if df is None or df.empty:
            raise ValueError("DataFrame cannot be None or empty")
        if not isinstance(table_id, str) or not table_id.strip():
            raise ValueError("table_id must be a non-empty string")
        if loading_method not in ['load_parquet', 'load_csv']:
            raise ValueError("loading_method must be either 'load_parquet' or 'load_csv'")
        if if_exists not in ['append', 'replace', 'fail']:
            raise ValueError("if_exists must be one of: 'append', 'replace', 'fail'")

        try:
            # Create a copy of the DataFrame to avoid modifying the original
            upload_df = df.copy()
            
            # Add data_dump_date column if requested
            if add_dump_date:
                upload_df['data_dump_datetime'] = pd.Timestamp.now(tz='UTC')
                upload_df['data_dump_date'] = pd.Timestamp.now(tz='UTC').date()
                upload_df['data_dump_time'] = pd.Timestamp.now(tz='UTC').strftime("%H:%M:%S %Z%z")
                
            
            # Construct the full table ID
            full_table_id = f"{self.project_id}.{self.dataset_id}.{table_id}"
            
            # Upload to BigQuery using service account credentials
            pandas_gbq.to_gbq(
                upload_df,
                full_table_id,
                project_id=self.project_id,
                if_exists=if_exists,
                api_method=loading_method,
                credentials=self.credentials  # Use service account credentials
            )
            
            print(f"Successfully loaded {upload_df.shape[0]} rows into {full_table_id}")
            
        except Exception as e:
            raise Exception(f"Failed to load DataFrame to BigQuery: {str(e)}") from e

    # ==============================================================================
    def table2df(self, table_id: str = None) -> pd.DataFrame:
        """
        Retrieve data from a BigQuery table and convert it into a pandas DataFrame.

        Args:
            table_id (str, optional): The ID of the table to retrieve data from.
                                    If not provided, uses the instance's table_id.

        Returns:
            pd.DataFrame: DataFrame containing the table data.

        Raises:
            ValueError: If no valid table_id is available or table doesn't exist.
            Exception: If data retrieval fails.
        """
        # Use instance table_id if none provided
        if table_id is None:
            if not hasattr(self, 'table_id') or not self.table_id:
                raise ValueError("No table_id provided and no default table_id set")
            table_id = self.table_id

        if not isinstance(table_id, str) or not table_id.strip():
            raise ValueError("table_id must be a non-empty string")

        try:
            # Construct the full table ID
            full_table_id = f"{self.project_id}.{self.dataset_id}.{table_id}"
            
            # Create the query
            query = f"SELECT * FROM `{full_table_id}`"
            
            # Execute query and return as DataFrame
            df = self.client.query(query).to_dataframe()
            
            print(f"Successfully retrieved {len(df)} rows from {full_table_id}")
            return df
            
        except Exception as e:
            raise Exception(f"Failed to retrieve data from table {table_id}: {str(e)}") from e



    # ==============================================================================
    def table2storage(
            self,
            table_id: str,
            storage_path: str,
            location: str = 'us-west1'
        ) -> None:
        """
        Extracts data from a BigQuery table and saves it to Google Cloud Storage.
        For large tables, the output will be automatically sharded into multiple files.

        Args:
            table_id (str): The ID of the table in BigQuery dataset.
            storage_path (str): Base GCS path in format 'bucket/folder_1/folder_2'.
                Files will be saved as: bucket/folder_1/folder_2/{table_id}/{table_id}_{date}-*.parquet
            location (str, optional): GCS bucket location. Defaults to 'us-west1'.

        Raises:
            ValueError: If parameters are invalid.
            Exception: If extraction fails or storage operations fail.
        """
        try:
            # Validate table_id
            if not isinstance(table_id, str) or not table_id.strip():
                raise ValueError("table_id must be a non-empty string")
            
            # Initialize storage client
            storage_client = storage.Client(credentials=self.credentials)
            
            # Construct table reference
            table_path = f"{self.project_id}.{self.dataset_id}.{table_id}"
            
            # Get current date for filename
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Remove any trailing slashes and construct the final storage path
            storage_path = storage_path.rstrip('/')
            destination_uri = f"gs://{storage_path}/{table_id}/{table_id}_{current_date}-*.parquet"
            
            # Get bucket name from storage path
            bucket_name = storage_path.split('/')[0]
            
            # Ensure bucket exists
            bucket = storage_client.bucket(bucket_name)
            if not bucket.exists():
                bucket = storage_client.create_bucket(bucket_name, location=location)
                print(f"Created bucket '{bucket_name}' in {location}")
            
            # Configure and run extraction job
            job_config = bigquery.job.ExtractJobConfig(
                destination_format="PARQUET"
            )
            
            extract_job = self.client.extract_table(
                table_path,
                destination_uri,
                location=location,
                job_config=job_config
            )
            
            # Wait for job completion
            extract_job.result()
            
            print(f"Successfully extracted table '{table_id}' to: {destination_uri}")
            print("Note: Large tables are automatically sharded into multiple files")
            
        except Exception as e:
            raise Exception(f"Failed to extract table '{table_id}' to storage: {str(e)}") from e


class StorageClient:
    def __init__(self, 
            key_file: Optional[str] = None
            ):
        self.key_file = key_file

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.key_file
        self.client = storage.Client()

    # create bucket from Browser, with more configurations
    # def create_bucket(self, bucket_name, location='us'):
    #     try:
    #         bucket = self.client.create_bucket(bucket_name, location=location)
    #         bucket.versioning_enabled = True
    #         bucket.patch()
    #         print(f"Created bucket '{bucket_name}' in {location} with versioning enabled")
    #         return bucket
    #     except google_exceptions.Conflict:
    #         print(f"Error: Bucket '{bucket_name}' already exists")
    #         return None
    #     except Exception as e:
    #         raise Exception(f"Failed to create bucket '{bucket_name}': {str(e)}") from e

    
    def file2bucket(self, bucket_name, file_path, blob_name):
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            print(f"Uploaded {file_path} to {bucket_name}/{blob_name}")
        except Exception as e:
            raise Exception(f"Failed to upload {file_path} to {bucket_name}/{blob_name}: {str(e)}") from e


# if __name__ == '__main__':
#     gg = BigQueryClient(
#         project_id = "prismatic-sunup-409818",
#         dataset_id = "finance_dataset",
#         # table_id = "test_df2table_2",
#         key_file='/Users/jinwenliu/github/keys/py2bigquery.json'
#     )


# if __name__ == '__main__':
#     # dotenv.load_dotenv('/Users/jinwenliu/github/.env/.env', override=True)
#     # service_account_file = os.getenv('GCP_SERVICE_ACCOUNT_FILE')
#     sc = StorageClient(
#         key_file='/Users/jinwenliu/github/.env/keys/gcp-bring-you-home.json'
#     )

#     sc.file2bucket(
#         bucket_name='web-scrawl', 
#         file_path='/Users/jinwenliu/github/BringYouHome/scrawler/humantraffickinghotline.org/data/all_states_data_2025-02-22.json', 
#         blob_name='humantraffickinghotline.org/hi-gcp-storage-client-test.json')
