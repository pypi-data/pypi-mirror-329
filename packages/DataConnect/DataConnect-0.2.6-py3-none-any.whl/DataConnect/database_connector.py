import databricks.sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import time
import requests

class DatabaseConnector:
    def __init__(self, is_databricks, server_hostname, http_path=None, access_token=None, 
                 database_name=None, schema=None, secret_key=None, use_integrated_security=False, 
                 sqlserver_username=None, sqlserver_password=None, cluster_id=None):
        
        # Initialize connection attributes
        self.is_databricks = is_databricks
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token
        self.database_name = database_name
        self.schema = schema
        self.secret_key = secret_key
        self.use_integrated_security = use_integrated_security
        self.sqlserver_username = sqlserver_username
        self.sqlserver_password = sqlserver_password
        self.cluster_id = cluster_id

        # Generate the SQLAlchemy connection URL
        self.connection_url = self._generate_connection_url()
        
        # Test the database connection
        self.engine = self._test_connection()

    def _generate_connection_url(self):
        if self.is_databricks:
            # Connection URL for Databricks
            return (
                f"databricks://token:{self.access_token}"
                f"@{self.server_hostname}?http_path={self.http_path}"
                f"&catalog={self.database_name}&schema={self.schema}"
            )
        else:
            # Connection URL for SQL Server
            if self.use_integrated_security:
                return (
                    f"mssql+pyodbc://{self.server_hostname}/{self.database_name}"
                    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
                )
            else:
                return (
                    f"mssql+pyodbc://{self.sqlserver_username}:{self.sqlserver_password}"
                    f"@{self.server_hostname}/{self.database_name}"
                    "?driver=ODBC+Driver+17+for+SQL+Server"
                )

    def _test_connection(self):
        """
        Test the connection to the database. For Databricks, also check cluster status.
        """
        if self.is_databricks:
            # Step 1: Check Databricks cluster status
            print("Checking Databricks cluster status...")
            cluster_status = self._check_cluster_status()
            if cluster_status == "TERMINATED":
                print("Cluster is currently terminated. Attempting to start...")
                # Here you could send an API call to start the cluster, or just inform the user
            elif cluster_status == "PENDING":
                print("Cluster is starting. Waiting until it is active...")
            
            # Poll the cluster status every few seconds until it’s "RUNNING"
            while cluster_status not in ["RUNNING", "ERROR"]:
                time.sleep(5)  # Wait before checking again
                cluster_status, cluster_message = self._check_cluster_status()
                print(f"Cluster status: {cluster_status}")
                print(f"Cluster message: {cluster_message}")

            if cluster_status != "RUNNING":
                raise Exception("Cluster failed to start. Please check Databricks console.")

            print("Cluster is running. Establishing connection...")

        try:
            # Step 2: Connect to the database
            engine = create_engine(self.connection_url)
            session = sessionmaker(bind=engine)()
            session.execute(text("SELECT 1"))  # Test query to check connection
            session.close()
            print("Database connection established successfully.")
            return engine

        except Exception as e:
            raise Exception(f"Error connecting to the database: {e}")

    def _check_cluster_status(self):
        """
        Checks the status of the Databricks cluster if using Databricks.
        """
        
        # REST API endpoint for cluster status (substitute your cluster ID and Databricks workspace URL)
        # Replace with your cluster ID
        url = f"https://{self.server_hostname}/api/2.0/clusters/get?cluster_id={self.cluster_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers,verify=False)
        if response.status_code == 200:
            cluster_info = response.json()
            cluster_state = cluster_info.get("state")
            cluster_message = cluster_info.get("state_message", "")
            return cluster_state, cluster_message
        else:
            raise Exception(f"Failed to fetch cluster status. HTTP Status: {response.status_code}, Response: {response.text}")

    def get_session(self):
        """
        Provides a new session connected to the database.
        """
        Session = sessionmaker(bind=self.engine)
        return Session()
