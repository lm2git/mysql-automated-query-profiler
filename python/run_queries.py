import mysql.connector
import time
import os
from decimal import Decimal

db_config = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'testuser'),
    'password': os.getenv('DB_PASSWORD', 'testpassword'),
    'database': os.getenv('DB_DATABASE', 'testdb'),
}

# Output directory for the reports
output_dir = './reports'
report_file = os.path.join(output_dir, 'report.txt')

# Path to the SQL queries file
queries_file_path = './inputs/testing-queries.sql'

def wait_for_mysql_connection(db_config, max_retries=100, delay=5):
    """
    Waits until MySQL is ready for connection.
    """
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(**db_config)
            connection.close()
            print("Successfully connected to MySQL.")
            return True
        except mysql.connector.Error as err:
            print(f"Unable to connect to MySQL, attempt {attempt + 1} of {max_retries}. Error: {err}")
            time.sleep(delay)
    return False

def read_queries_from_file(file_path):
    """
    Reads queries from the .sql file and returns them as a list.
    """
    try:
        with open(file_path, 'r') as file:
            # Read the file content and split queries by semicolon
            queries = file.read().split(';')
            # Filter out any empty queries
            return [query.strip() for query in queries if query.strip()]
    except FileNotFoundError:
        print(f"Error: file {file_path} not found.")
        return []

def execute_query(cursor, query):
    """
    Executes an SQL query and collects execution profiles.
    """
    try:
        # Enable profiling
        cursor.execute("SET PROFILING = 1;")
        print("Profiling enabled.")

        # Execute the main query
        print(f"Executing query: {query}")
        cursor.execute(query)
        
        # Ensure results are read before running additional queries
        cursor.fetchall()  # Consume results from the previous query
        print("Query executed successfully.")

        # Retrieve query profiles
        print("Running SHOW PROFILE CPU to get CPU details.")
        cursor.execute("SHOW PROFILE CPU;")
        cpu_profile = cursor.fetchall()

        print("Running SHOW PROFILE MEMORY to get memory details.")
        cursor.execute("SHOW PROFILE MEMORY;")
        memory_profile = cursor.fetchall()

        print("Running SHOW PROFILE BLOCK IO to get I/O details.")
        cursor.execute("SHOW PROFILE BLOCK IO;")
        block_io_profile = cursor.fetchall()

        # Calculate totals for CPU and Memory
        cpu_user_total = sum(Decimal(row[1]) for row in cpu_profile)  # Sum of the CPU_user column
        cpu_system_total = sum(Decimal(row[2]) for row in cpu_profile)  # Sum of the CPU_system column
        memory_total = sum(Decimal(row[1]) for row in memory_profile)  # Sum of the Memory Allocation column

        # Combine profiles and totals into a dictionary for easy access
        profile_details = {
            'cpu': {
                'profile': cpu_profile,
                'total_cpu_user': cpu_user_total,
                'total_cpu_system': cpu_system_total,
            },
            'memory': {
                'profile': memory_profile,
                'total_memory': memory_total,
            },
            'block_io': block_io_profile if block_io_profile else [],
        }

        return profile_details

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return {}

def save_report(profiles, report_file):
    """
    Saves the query profiles report to a file.
    """
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, 'w') as f:
        for query, profile in profiles.items():
            f.write(f"--- Profile: {query} ---\n")

            # Write CPU profile, if available
            if profile.get('cpu'):
                f.write("\n CPU Profiling:\n")
                for stage, *values in profile['cpu']['profile']:
                    f.write(f"Stage: {stage}, Duration: {values[0]} seconds, CPU_user: {values[1]} seconds, CPU_system: {values[2]} seconds\n")
                f.write(f"\nTotal CPU_user: {profile['cpu']['total_cpu_user']} seconds\n")
                f.write(f"Total CPU_system: {profile['cpu']['total_cpu_system']} seconds\n")
            else:
                f.write("No CPU data available.\n")

            # Write MEMORY profile, if available
            # if profile.get('memory'):
            #     f.write("\n Memory Profiling:\n")
            #     for stage, value in profile['memory']['profile']:
            #         f.write(f"Stage: {stage}, Memory Allocation: {value} seconds\n")
            #     f.write(f"\nTotal Memory Allocation: {profile['memory']['total_memory']} seconds\n")
            # else:
            #     f.write("No memory data available.\n")

            # Write BLOCK IO profile, if available
            # if profile.get('block_io'):
            #     f.write("\n Block I/O Profiling:\n")
            #     for stage, *values in profile['block_io']:
            #         f.write(f"Stage: {stage}, I/O Time: {values[0]} seconds, Read: {values[1]}, Write: {values[2]}\n")
            # else:
            #     f.write("No I/O data available.\n")

            f.write("\n")  # Space between queries

    print(f"Report saved at: {report_file}")

def main():
    """
    Connects to the database, executes queries, and saves reports.
    """
    # Create the reports directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Wait for MySQL to be ready
    if not wait_for_mysql_connection(db_config):
        print("Unable to connect to MySQL. Stopping script.")
        return

    # Read queries from the file
    queries = read_queries_from_file(queries_file_path)
    if not queries:
        print("No queries to execute. Stopping script.")
        return

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        profiles = {}
        for query in queries:
            try:
                # Execute query and collect profiles
                profile_details = execute_query(cursor, query)
                profiles[query] = profile_details
            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
                continue

        # Save profiles to the report
        if profiles:
            save_report(profiles, report_file)
        else:
            print("No profiles to save.")

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    finally:
        # Close connection
        if cursor:
            try:
                cursor.close()
            except mysql.connector.Error as err:
                print(f"Error closing cursor: {err}")
        if connection:
            try:
                connection.close()
            except mysql.connector.Error as err:
                print(f"Error closing connection: {err}")

if __name__ == "__main__":
    main()
