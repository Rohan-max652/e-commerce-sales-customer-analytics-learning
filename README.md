# E-Commerce Sales & Customer Analytics

## Project Overview

This project analyzes e-commerce sales and customer data to identify revenue trends, product performance, customer behavior, profitability, and geographic patterns.

The project follows an end-to-end data analytics workflow:

**Raw Data → Data Cleaning → Data Validation → MySQL → SQL Analysis → Python EDA → Power BI Dashboard → Business Insights**

The goal is to transform raw transactional data into meaningful business insights that can support sales, marketing, customer retention, and business decision-making.

---

## Business Objectives

- Analyze overall sales revenue and profitability
- Identify high-performing product categories and products
- Analyze monthly revenue trends
- Identify top-performing states and geographic markets
- Understand customer purchasing behavior
- Analyze customer purchase frequency and segmentation
- Evaluate payment-method performance
- Identify important customer and product insights
- Build an interactive Power BI dashboard for business reporting

---

## Dataset

The project uses a realistic synthetic e-commerce dataset representing an Indian online retail business.

### Tables

| Table | Description |
|---|---|
| Customers | Customer information such as age, gender, city and state |
| Products | Product, category, brand, cost price and selling price information |
| Orders | Order dates, customers, payment methods, discounts and order status |
| Order Items | Products purchased, quantities and unit prices |

### Dataset Size

- **Customers:** 10,000
- **Products:** 1,000
- **Orders:** 50,000
- **Order Items:** 102,559

The raw dataset intentionally contained several data-quality issues so that a realistic data-cleaning and validation workflow could be demonstrated.

---

## Data Cleaning & Validation

Python and Pandas were used to investigate and clean the raw datasets.

### Data-quality issues identified

- Duplicate customer records
- Missing customer ages
- Missing payment methods
- Inconsistent city capitalization
- Invalid order-item quantities
- Data relationship and integrity checks

### Cleaning actions

- Removed exact duplicate customer records
- Filled missing customer ages using the median age
- Standardized city names
- Replaced missing payment methods with `Unknown`
- Removed order-item records with invalid quantities
- Converted dates and numeric fields to appropriate data types
- Rechecked relationships between customers, orders, products and order items

After cleaning, all critical validation checks passed.

---

## Tools & Technologies

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **MySQL**
- **MySQL Workbench**
- **SQL**
- **Power BI**
- **Microsoft Excel**
- **VS Code**
- **Git / GitHub**

---

## Python Analysis

Python was used for:

- Data inspection
- Data-quality analysis
- Data cleaning
- Data validation
- Exploratory Data Analysis (EDA)
- Customer analysis
- Product analysis
- Sales and profitability analysis
- Customer segmentation
- Final business insights

The analysis includes revenue, profit, product performance, category performance, customer behavior, payment methods, age groups, gender, geography and purchasing frequency.

---

## SQL Analysis

MySQL was used to store and analyze the cleaned datasets.

SQL analysis includes:

- Overall business KPIs
- Revenue analysis
- Profit analysis
- Monthly sales trends
- Category performance
- Product performance
- Customer analysis
- State-level analysis
- Payment-method analysis
- Customer segmentation
- RFM analysis
- Window functions and product ranking
- Analytical SQL views

---

## Power BI Dashboard

The Power BI dashboard contains **3 pages** designed around different business questions.

### Page 1 — Sales Overview

Provides a high-level view of business performance.

Key visuals include:

- Total Revenue
- Total Profit
- Profit Margin
- Delivered Orders
- Average Order Value
- Monthly Revenue Trend
- Revenue by Category
- Profit by Category

### Page 2 — Product & Customer Performance

Focuses on the best-performing products and customers.

Key visuals include:

- Top 10 Products by Revenue
- Top 10 Customers by Revenue
- Top 10 Products by Profit
- Revenue by Payment Method
- Customer Segmentation

### Page 3 — Customer & Geographic Insights

Focuses on customer demographics, purchasing behavior and geographic performance.

Key visuals include:

- Revenue by State
- Revenue by Gender
- Revenue by Age Group
- Customer Purchase Frequency

---

## Key Business Results

The analysis of delivered orders produced the following overall results:

| KPI | Result |
|---|---:|
| Total Revenue | ₹78.47 Cr |
| Total Profit | ₹23.45 Cr |
| Profit Margin | 29.88% |
| Delivered Orders | 28,683 |
| Average Order Value | ₹27,357.58 |

### Category Insights

**Electronics** generated the highest revenue and profit among all product categories.

Revenue by category showed Electronics significantly ahead of the other categories, followed by Home & Kitchen and Sports.

### Geographic Insights

**Gujarat** was the highest-revenue state, followed by Kerala and Telangana.

### Payment Insights

**UPI** generated the highest revenue among the available payment methods.

### Customer Insights

The analysis identified differences in purchasing frequency and customer value across customer segments.

RFM analysis identified customer groups including:

- Champions
- Loyal Customers
- Potential Loyalists
- At Risk
- Lost Customers
- Others

### Customer Demographics

The **36–45 age group** generated the highest revenue among the analyzed age groups.

---

## Business Recommendations

Based on the analysis:

1. **Focus on Electronics**
   - Electronics is the strongest revenue and profit category, so inventory and promotional strategies can prioritize high-performing products.

2. **Strengthen High-Value Customer Retention**
   - Champions and loyal customers should receive targeted loyalty offers and personalized promotions.

3. **Re-engage At-Risk Customers**
   - At-risk customers represent an opportunity for retention campaigns, personalized discounts and targeted communication.

4. **Leverage UPI Adoption**
   - UPI is the strongest payment method by revenue, suggesting an opportunity to optimize the digital payment experience and related promotions.

5. **Focus on High-Performing States**
   - Gujarat, Kerala and Telangana can receive stronger regional marketing and inventory planning based on their sales performance.

6. **Target High-Revenue Age Groups**
   - The 36–45 customer segment shows strong revenue contribution and can be targeted with relevant products and campaigns.

---

## Project Structure

```text
e-commerce-sales-customer-analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── python/
│   ├── 01_data_inspection.py
│   ├── 01_eda.py
│   ├── 02_business_analysis.py
│   ├── 02_data_quality.py
│   ├── 03_data_cleaning.py
│   ├── 04_data_validation.py
│   ├── 05_mysql_connection_test.py
│   ├── 06_load_data_to_mysql.py
│   ├── 07_eda.py
│   ├── 08_discount_analysis.py
│   ├── 09_final_business_insights.py
│   └── generate_dataset.py
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 01_basic_business_analysis.sql
│   ├── 02_sales_analysis.sql
│   └── 03_advanced_analysis.sql
│
├── powerbi/
│   └── E-Commerce_Sales_Customer_Analytics.pbix
│
├── reports/
│   ├── business_insights.md
│   └── charts/
│
└── README.md