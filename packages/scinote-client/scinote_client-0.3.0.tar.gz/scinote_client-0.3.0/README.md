# SciNote Client

SciNote Client is a Python library for interacting with the SciNote API. This
library allows you to programmatically manage SciNote inventories, including
creating and managing inventories, columns, items, and more.

## Installation

You can install the SciNote Client library using pip:

```bash
pip install -e src/scinote-client
```

## Usage

The library requires 2 environment variables to be configured:

* `SCINOTE_BASE_URL` - The API endpoint
* `SCINOTE_API_KEY` - The API key, generated in the SciNote admin console.

Here's a basic example of how to use the SciNote Client:

```python
from scinote_client.client.api.teams_client import CreateClient

# Initialize the client
teams_client = CreateClient()

# Get a list of teams
teams = teams_client.get_teams()
for team in teams:
  print(team.id)
```

## Documentation

For detailed documentation, please refer to the [official documentation](https://scinote-eln.github.io/scinote-api-docs/#introductiono).
