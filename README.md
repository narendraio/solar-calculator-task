# 🔆 Solar Calculation App (Frappe)

A simple Frappe-based app to calculate solar power metrics like overall average usage and monthly tariffs for each customer. Built as part of a test task.

---

## 📦 Features

-   Add entries with KW, KWH, timestamp, and tariff period
-   Auto-calculate overall average (KW + KWH)
-   Compute monthly tariff breakdown per customer
-   Data stored and rendered in JSON format

---

## 🚀 Installation

### ⚙️ Prerequisites

-   Python 3.10.x
-   Node.js (>= 16)
-   Yarn
-   Redis
-   MariaDB
-   wkhtmltopdf
-   [Frappe Bench CLI](https://frappeframework.com/docs/v14/user/en/installation)

---

### 🧑‍💻 Setup Instructions

```bash
# 1. Clone this repo
git clone https://github.com/narendraio/solar-calculator-task.git
cd solar-calculator-task

# 2. Initialize Frappe Bench (if not already inside a bench)
bench init solar_bench --frappe-branch version-14
cd solar_bench

# 3. Get app into the bench
bench get-app test_narendra ../solar-calculator-task/apps/test_narendra

# 4. Create a new site
bench new-site solar.local

# 5. Install the app
bench --site solar.local install-app test_narendra

# 6. Add site to bench config
echo "solar.local" >> sites/apps.txt

# 7. Start development server
bench start
```
