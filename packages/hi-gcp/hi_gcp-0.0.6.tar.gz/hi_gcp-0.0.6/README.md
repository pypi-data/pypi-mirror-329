# hi-gcp

A Python utility package for working with Google Cloud Platform (GCP) services, primarily focusing on BigQuery operations. Features more robust to prevent accidentallly delete or clean tables.

## Installation

```bash
pip install hi-gcp
```

## Features

- Easy-to-use BigQuery client wrapper
- Simplified query execution and data retrieval
- Efficient data loading and export operations
- Additional step for sensitive operations (table deletion and cleaning)
- Environment variable support for configuration

## Usage

```python
from hi_gcp import BigQueryClient

# Initialize the client

gg = BigQueryClient(
    project_id = "project_id",
    dataset_id = "dataset_id",
    table_id = "table_id",
    key_file='path/to/service_account_key.json'
)

# Execute a query
df = gg.sql2df("SELECT * FROM `project_id.dataset_id.table_id` LIMIT 100")
```

## License

MIT License