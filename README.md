
# MySQL Query Profiling Service

This project provides an end-to-end setup for profiling MySQL queries. The system measures CPU usage during query execution, generating detailed reports for performance analysis. It leverages Docker containers to streamline setup and isolate dependencies.

## Project Structure

```
MYSQL-QUERY-PROFILING
├── input-sql
│   └── testing-queries.sql        # SQL file containing queries to profile
├── mysql
│   ├── init-scripts
│   │   └── init.sql               # Script to initialize the MySQL database
│   ├── my.cnf                     # MySQL configuration file
│   └── Dockerfile                 # Dockerfile to build the MySQL container
├── output-report
│   └── report.txt                 # Generated query profiling report
├── python
│   ├── Dockerfile                 # Dockerfile to build the Python profiling service
│   ├── requirements.txt           # Python dependencies
│   └── run_queries.py             # Main Python script for query execution and profiling
├── docker-compose.yml             # Docker Compose file for service orchestration
└── README.md                      # Documentation (this file)
```

## Features

- **Query Profiling**: Captures execution time, CPU, memory, and block I/O metrics for each SQL query.
- **Automated Setup**: Uses Docker Compose to orchestrate MySQL and Python services.
- **Report Generation**: Outputs a detailed profiling report in `output-report/report.txt`.
- **Customizable Configuration**: Easily modify MySQL settings via `my.cnf` and initialize datasets with `init.sql`.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your system.
- Basic understanding of MySQL and Python.

### Step-by-Step Guide

1. Clone this repository:
   ```bash
   git clone https://github.com/lm2git/mysql-automated-query-profiler.git
   cd mysql-automated-query-profiler
   ```

2. Place your sql init dataset script in the `mysql/init-scripts/init.sql` , then place your SQL queries in the `input-sql/testing-queries.sql` file. 

3. Build and start the services using Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

4. Monitor the logs to ensure successful execution. The profiling report will be saved to `output-report/report.txt`.

5. Shut down the services after profiling:
   ```bash
   docker-compose down -v
   ```

## Configuration

### MySQL Init 

- **Initialization**: Modify `mysql/init-scripts/init.sql` with your query to build DB or generate your dataset. (in the project structure there is an example)
- **Initialization**: Modify `input-sql/testing-queries.sql` with your query to profile  (in the project structure there is an example)

## Output

### Report File

Profiling results are saved to `output-report/report.txt`.

**Metrics Captured**:
- CPU usage (user/system time).
- Memory usage during query execution. (not in report output)
- Block I/O (read/write performance). (not in report output)

## Customization

- **Input Queries**: Add or modify SQL queries in `input-sql/testing-queries.sql`.
- **MySQL Dataset**: Update `mysql/init-scripts/init.sql` to create larger or more complex datasets.


## Example Profiling Report

Below is an example of the profiling report:

```
--- Profile: SELECT * FROM users; ---

CPU Profiling:
Phase: starting, Duration: 0.001 seconds, CPU_user: 0.001 seconds, CPU_system: 0.000 seconds
Phase: executing, Duration: 0.020 seconds, CPU_user: 0.015 seconds, CPU_system: 0.005 seconds

Total CPU_user: 0.016 seconds
Total CPU_system: 0.005 seconds
```

## Future Enhancements

- Add support for advanced MySQL profiling using `EXPLAIN` and query execution plans.
- Enable visualization of profiling data using tools like Grafana.
- Automate performance alerts based on profiling thresholds.
