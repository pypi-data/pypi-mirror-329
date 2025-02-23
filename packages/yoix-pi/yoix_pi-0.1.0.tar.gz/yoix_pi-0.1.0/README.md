# Yoix Persistent Includes

BBEdit-style persistent includes for Python.

## Installation

You can install Yoix Persistent Includes using pip:

```bash
pip install yoix-pi
```

## Usage

### Python API

```python
from yoix_pi.processor import process_persistent_includes

config = {
    'partials_dir': 'path/to/partials',
    'public_dir': 'path/to/public'
}

process_persistent_includes(config)
```

### Command Line

You can also use the command-line interface:

```bash
# Using default directories (includes/partials and public)
yoixpi

# Specify custom directories
yoixpi --partials path/to/partials --public path/to/public

# Using short options
yoixpi -p path/to/partials -b path/to/public

# Show help
yoixpi --help
```

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/crock/yoix-pi
cd yoix-pi

# Install in development mode with test dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.