# Dynamic Tables (Python)
A Python library for dynamically creating and managing PostgreSQL tables based on input data.

## 🚀 Features
- Automatically creates tables based on incoming data.
- Supports dynamic naming conventions.
- Provides easy database connectivity with PostgreSQL.
- Includes helper functions for querying and deleting tables.

---

## 📥 Installation
### **1️⃣ Install via GitHub (Recommended for Development)**
Clone the repository and install in editable mode:
```bash
git clone https://github.com/scottrodeo/dynamic-tables-python.git
cd dynamic-tables-python
pip install -e .
```

### **2️⃣ Install Directly via `pip`**
The package is available on PyPI, you can install it with:
```bash
pip install dynamic-tables
```

---

## 🏃‍♂️ Running the Example
### **1️⃣ Quick Run (Without Installation)**
If you don't want to install the package, you can directly run the example script:
```bash
python3 examples/example.py
```
💡 *This works because the script dynamically adjusts `sys.path`.*

### **2️⃣ Recommended (After Installation)**
If you've installed the package (`pip install -e .`), simply run:
```bash
python3 examples/example.py
```

---

## 📌 Example Usage
Once installed, you can use `dynamic_tables` in your Python scripts:

```python
from dynamic_tables import DynamicTables

# Initialize the dynamic table manager
tables = DynamicTables()

# Example: Creating and inserting data dynamically
tables.set_table_prefix("dtbl_")
tables.set_columns("domain TEXT, category TEXT, lang TEXT")
tables.set_dynamic_column("domain")

tables.input("wikipedia.org", "cats", "en")
tables.input("wikipedia.org", "dogs", "en")

# Show all tables
tables.show_tables()
```

---

## 🛠️ Available Functions
| Function | Description |
|----------|-------------|
| `set_columns("name TYPE, age TYPE")` | Define table schema |
| `set_table_prefix("prefix_")` | Set a custom table prefix |
| `set_dynamic_column("column_name")` | Set the column that determines dynamic table names |
| `input(value1, value2, ...)` | Insert a new row dynamically |
| `show_tables()` | List all dynamically created tables |
| `show_columns("table_name")` | Show column details for a specific table |
| `select_table("table_name")` | Retrieve all rows from a table |
| `delete_tables()` | Drop all tables matching the prefix |

---

## ⚡ Development
### **Running Tests**
To run the test suite:
```bash
pytest tests/
```

### **Linting**
Ensure your code follows best practices:
```bash
flake8 dynamic_tables/
```

---

## 🤝 Contributing
Contributions are welcome! If you'd like to improve `dynamic_tables`, follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🌎 Links
- **GitHub Repository:** [Dynamic Tables (Python)](https://github.com/scottrodeo/dynamic-tables-python)
- **Documentation:** *(To be added)*
- **Issue Tracker:** [Report Issues](https://github.com/scottrodeo/dynamic-tables-python/issues)

---

### **🚀 Happy Coding!**

