# OdooQuery

A Python library that provides enhanced query functionality on top of odoorpc for higher-level operations with Odoo.

## Installation

```bash
pip install odooquery
```

## Usage

```python
from odooquery import OdooQuery

# Initialize the connection
query = OdooQuery(host='localhost', port=8069, database='mydb', user='admin', password='admin')

# Use enhanced query functions
results = query.find_records('res.partner', [('is_company', '=', True)])
```

## Features

- Enhanced query interface for Odoo
- Simplified record operations
- Type-safe query building

## Requirements

- Python 3.12+
- odoorpc>=0.9.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.
