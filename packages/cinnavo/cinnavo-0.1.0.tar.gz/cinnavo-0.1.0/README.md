# Cinnavo

Cinnavo is a Python client package for interacting with the [Cinnavo API](https://api.cinnavo.com/). It simplifies the process of sending search queries and retrieving results, including AI-generated responses and optional full content extraction.

## Installation

Install the package via pip:

```bash
pip install cinnavo
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/cinnavo.git
```

## Usage

Here's a quick example to get started:

```python
from cinnavo import Cinnavo

# Initialize the client with your API key
client = Cinnavo(api_key="your-api-key-here")

# Perform a search query
response = client.search(
    query="Python package development",
    num_results=5,
    date_range="month",
    engine=["google", "bing"],
    categories="technology",
    ai_response=True,
    full_content=False
)

print(response)
```

## Contributing

Contributions and feedback are welcome! Please open issues or submit pull requests on the GitHub repository.

## License

This project is licensed under the MIT License.
