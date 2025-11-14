# Synthetic E-Commerce Data Project

This project was completed as part of the Diligent A-SDLC Cursor exercise.

---

## ✔️ Tasks Completed

### 1️⃣ Generated Synthetic E-Commerce Data  
Using `generate_data.py`, the following synthetic datasets were generated and stored inside the `data/` directory:

- users.csv  
- products.csv  
- orders.csv  
- order_items.csv  
- payments.csv  

Each file contains realistic, randomly generated records suitable for e-commerce data analysis.

---

### 2️⃣ Ingested Data into SQLite  
The script `ingest_to_sqlite.py` reads all CSV files from the `data/` folder and loads them into a SQLite database named **ecommerce.db**.  
It automatically creates tables and inserts all the records.

---

### 3️⃣ SQL Join Query  
The file `join_query.sql` contains a SQL query that performs a multi-table JOIN across:

- users  
- orders  
- order_items  
- products  
- payments  

The query returns:

- user_name  
- order_id  
- product_name  
- quantity  
- item_price  
- payment_method  
- order_date  

The returned records are sorted in **descending order of order_date**.

---

## ✔️ How to Run the Project

### Step 1 — Install required dependencies:
```
pip install pandas faker
```

### Step 2 — Generate the synthetic CSV datasets:
```
python generate_data.py
```

### Step 3 — Ingest the datasets into SQLite:
```
python ingest_to_sqlite.py
```

### Step 4 — Run the SQL join query:
Open `ecommerce.db` in any SQLite viewer and execute:
```
.read join_query.sql
```


---

## 📁 Project Structure

/data/
   users.csv
   products.csv
   orders.csv
   order_items.csv
   payments.csv

generate_data.py
ingest_to_sqlite.py
join_query.sql
ecommerce.db
README.md


---

## 👤 Author
Jhahnavi K P
