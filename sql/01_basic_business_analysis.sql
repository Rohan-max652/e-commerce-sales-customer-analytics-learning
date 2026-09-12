USE ecommerce_analytics;

-- ============================================================
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
-- BASIC BUSINESS ANALYSIS
-- ============================================================

-- 1. Total number of customers
SELECT COUNT(*) AS total_customers
FROM customers;


-- 2. Total number of products
SELECT COUNT(*) AS total_products
FROM products;


-- 3. Total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- 4. Total number of order items
SELECT COUNT(*) AS total_order_items
FROM order_items;


-- 5. Order status distribution
SELECT
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
ORDER BY order_count DESC;


-- 6. Payment method distribution
SELECT
    payment_method,
    COUNT(*) AS order_count
FROM orders
GROUP BY payment_method
ORDER BY order_count DESC;


-- 7. Total revenue from delivered orders
SELECT
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered';


-- 8. Average Order Value (AOV) for delivered orders
SELECT
    ROUND(
        SUM(oi.quantity * oi.unit_price)
        / COUNT(DISTINCT oi.order_id),
        2
    ) AS average_order_value
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered';


-- ============================================================
-- 9. MONTHLY SALES ANALYSIS
-- ============================================================

SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY sales_month;


-- ============================================================
-- 10. CATEGORY-WISE SALES & PROFIT ANALYSIS
-- ============================================================

SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost_price)), 2) AS profit,
    ROUND(
        100 * SUM(oi.quantity * (oi.unit_price - p.cost_price))
        / SUM(oi.quantity * oi.unit_price),
        2
    ) AS profit_margin_percent
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category
ORDER BY revenue DESC;


-- ============================================================
-- 11. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    SUM(oi.quantity) AS units_sold,
    ROUND(
        SUM(oi.quantity * (oi.unit_price - p.cost_price)),
        2
    ) AS profit
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.brand
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 12. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_method,
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS order_percentage
FROM orders
GROUP BY payment_method
ORDER BY total_orders DESC;


-- ============================================================
-- 13. TOP 10 CUSTOMERS BY REVENUE
-- ============================================================

SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.state,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city,
    c.state
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 14. CUSTOMER PURCHASE FREQUENCY
-- ============================================================

SELECT
    CASE
        WHEN delivered_orders = 1 THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS customer_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM (
    SELECT
        c.customer_id,
        COUNT(DISTINCT o.order_id) AS delivered_orders
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    WHERE o.status = 'Delivered'
    GROUP BY c.customer_id
) AS customer_orders
GROUP BY customer_type
ORDER BY customer_count DESC;


-- ============================================================
-- 15. SALES BY STATE
-- ============================================================

SELECT
    c.state,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    ROUND(
        SUM(oi.quantity * (oi.unit_price - p.cost_price)),
        2
    ) AS total_profit
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY c.state
ORDER BY total_revenue DESC;


-- ============================================================
-- 16. RFM CUSTOMER ANALYSIS
-- ============================================================

WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
    GROUP BY
        c.customer_id,
        c.customer_name
)

SELECT
    customer_id,
    customer_name,
    last_order_date,
    frequency,
    monetary
FROM customer_rfm
ORDER BY monetary DESC
LIMIT 10;


-- ============================================================
-- 17. RFM SCORING
-- ============================================================

WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
    GROUP BY
        c.customer_id,
        c.customer_name
),

rfm_scores AS (
    SELECT
        customer_id,
        customer_name,
        last_order_date,
        frequency,
        monetary,

        6 - NTILE(5) OVER (
            ORDER BY last_order_date
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary
        ) AS monetary_score

    FROM customer_rfm
)

SELECT
    customer_id,
    customer_name,
    last_order_date,
    frequency,
    monetary,
    recency_score,
    frequency_score,
    monetary_score,
    CONCAT(
        recency_score,
        frequency_score,
        monetary_score
    ) AS rfm_score
FROM rfm_scores
ORDER BY monetary DESC
LIMIT 10;


-- ============================================================
-- 18. CUSTOMER SEGMENTATION USING RFM
-- ============================================================

WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.quantity * oi.unit_price) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
    GROUP BY
        c.customer_id,
        c.customer_name
),

rfm_scores AS (
    SELECT
        customer_id,
        customer_name,
        last_order_date,
        frequency,
        monetary,

        NTILE(5) OVER (
            ORDER BY DATEDIFF('2026-08-31', last_order_date) DESC,
                 customer_id
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency,
                customer_id
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary,
                customer_id
        ) AS monetary_score

    FROM customer_rfm
),

segmented_customers AS (
    SELECT
        customer_id,
        customer_name,
        recency_score,
        frequency_score,
        monetary_score,

        CASE
            WHEN recency_score >= 4
                 AND frequency_score >= 4
                 AND monetary_score >= 4
                THEN 'Champions'

            WHEN recency_score >= 3
                 AND frequency_score >= 4
                THEN 'Loyal Customers'

            WHEN recency_score >= 4
                 AND frequency_score BETWEEN 2 AND 3
                THEN 'Potential Loyalists'

            WHEN recency_score >= 4
                 AND frequency_score = 1
                THEN 'New Customers'

            WHEN recency_score <= 2
                 AND frequency_score >= 3
                THEN 'At Risk'

            WHEN recency_score = 1
                 AND frequency_score <= 2
                THEN 'Lost Customers'

            ELSE 'Other'
        END AS customer_segment

    FROM rfm_scores
)

SELECT
    customer_segment,
    COUNT(*) AS customer_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_percentage
FROM segmented_customers
GROUP BY customer_segment
ORDER BY customer_count DESC;


-- ============================================================
-- 19. CUSTOMER SEGMENT VALUE ANALYSIS
-- ============================================================

WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.customer_name,
        MAX(o.order_date) AS last_order_date,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.quantity * oi.unit_price) AS monetary
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
    GROUP BY
        c.customer_id,
        c.customer_name
),

rfm_scores AS (
    SELECT
        customer_id,
        NTILE(5) OVER (
            ORDER BY DATEDIFF('2026-08-31', last_order_date) DESC,
                customer_id
        ) AS recency_score,
        NTILE(5) OVER (
            ORDER BY frequency,
                customer_id
        ) AS frequency_score,
        NTILE(5) OVER (
            ORDER BY monetary,
                customer_id
        ) AS monetary_score
    FROM customer_rfm
),

segmented_customers AS (
    SELECT
        customer_id,

        CASE
            WHEN recency_score >= 4
                 AND frequency_score >= 4
                 AND monetary_score >= 4
                THEN 'Champions'

            WHEN recency_score >= 3
                 AND frequency_score >= 4
                THEN 'Loyal Customers'

            WHEN recency_score >= 4
                 AND frequency_score BETWEEN 2 AND 3
                THEN 'Potential Loyalists'

            WHEN recency_score >= 4
                 AND frequency_score = 1
                THEN 'New Customers'

            WHEN recency_score <= 2
                 AND frequency_score >= 3
                THEN 'At Risk'

            WHEN recency_score = 1
                 AND frequency_score <= 2
                THEN 'Lost Customers'

            ELSE 'Other'
        END AS customer_segment

    FROM rfm_scores
)

SELECT
    sc.customer_segment,
    COUNT(DISTINCT sc.customer_id) AS customer_count,

    COUNT(DISTINCT o.order_id) AS delivered_orders,

    ROUND(
        SUM(oi.quantity * oi.unit_price),
        2
    ) AS total_revenue,

    ROUND(
        SUM(
            oi.quantity * (oi.unit_price - p.cost_price)
        ),
        2
    ) AS total_profit,

    ROUND(
        SUM(oi.quantity * oi.unit_price)
        / COUNT(DISTINCT sc.customer_id),
        2
    ) AS revenue_per_customer

FROM segmented_customers sc

JOIN orders o
    ON sc.customer_id = o.customer_id

JOIN order_items oi
    ON o.order_id = oi.order_id

JOIN products p
    ON oi.product_id = p.product_id

WHERE o.status = 'Delivered'

GROUP BY sc.customer_segment

ORDER BY total_revenue DESC;