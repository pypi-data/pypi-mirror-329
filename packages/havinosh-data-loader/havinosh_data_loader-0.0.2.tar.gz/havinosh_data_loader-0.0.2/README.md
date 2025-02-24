# **📦 havinosh_data_loader: CSV to PostgreSQL Ingestion**  
**Seamlessly load CSV files into PostgreSQL dynamically.**  

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supported-green)  
![License](https://img.shields.io/badge/License-MIT-yellowgreen)  
![Status](https://img.shields.io/badge/Status-Active-brightgreen)  

---

## 🚀 **Overview**  
`havinosh_data_loader` is a Python package designed to automatically **detect CSV structure**, **create tables**, and **insert data into PostgreSQL** with minimal effort. Just drop your CSV files into a folder, and `loader` will handle everything dynamically.  

---

## 📌 **Features**  
✅ **Automatic Table Creation** – Reads CSV headers and maps them to PostgreSQL columns  
✅ **Dynamic Schema Detection** – Infers data types automatically  
✅ **Batch Data Insertion** – Efficiently loads large datasets  
✅ **Error Handling** – Logs errors and provides detailed debugging  
✅ **Environment Configurations** – Uses `.env` for secure database credentials  
✅ **Modular & Extensible** – Well-structured for easy modifications  

---

## 📂 **Project Structure**  
```
havinosh_data_loader/
│── havinosh_data_loader/                   # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Database configuration
│   ├── process_csv.py        # CSV processing logic
│   ├── db_utils.py           # PostgreSQL connection utilities
│   ├── exception.py          # Custom exception handling
│   ├── logger.py             # Logging setup
│── scripts/                  # Command-line scripts
│   ├── ingest.py             # Main ingestion script
│── tests/                    # Unit tests
│   ├── test_process_csv.py
│── csv_files/                # CSV storage (ignored in production)
│── setup.py                  # Package setup script
│── requirements.txt          # Dependencies
│── README.md                 # Documentation
│── .gitignore                # Ignore unnecessary files
│── LICENSE                   # License details
```

---

## 🛠 **Installation**  

### **1️⃣ Install via pip**  
Once published to PyPI, you can install `loader` using:  
```sh
pip install havinosh_data_loader
```

### **2️⃣ Install from Source**  
Clone the repository and install dependencies:  
```sh
git clone https://github.com/IAMDSVSSANGRAL/havinosh_data_loader.git  
cd loader  
pip install -r requirements.txt  
```

---

## ⚙ **Usage**  

### **1️⃣ Set Up Your Environment**  
Create a **`.env`** file in the root directory and add:  
```ini
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### **2️⃣ Using the CLI**  
Place your CSV files inside the **`csv_files/`** directory and run the ingestion script:
```sh
python scripts/ingest.py
```
Alternatively, if using the CLI command:
```sh
loader --folder csv_files
```

### **3️⃣ Using the Python Package in Your Script**  
You can also use `havinosh_data_loader` programmatically within a Python script:

```python
from havinosh_data_loader.process_csv import CSVProcessor

# Define the folder where CSV files are stored
csv_folder = "csv_files/"

# Initialize the processor
processor = CSVProcessor(csv_folder)

# Start the ingestion process
processor.process_files()
```

---

## 🧪 **Testing**  
Run unit tests using:  
```sh
pytest tests/
```

---

## 📜 **License**  
This project is licensed under the **MIT License** – see the [`LICENSE`](LICENSE) file for details.  

---

## 🤝 **Contributing**  
Contributions are welcome! Please follow these steps:  
1. **Fork** the repository  
2. **Create a branch** (`feature-xyz`)  
3. **Commit your changes**  
4. **Push** and submit a **Pull Request**  

---

## 📬 **Contact**  
📧 Email: support@havinosh.com  
🌐 GitHub: [VISHAL SINGH SANGRAL](https://github.com/IAMDSVSSANGRAL)  

---

### **🚀 Happy Data Ingestion!**

