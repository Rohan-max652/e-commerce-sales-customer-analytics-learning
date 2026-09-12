USE ecommerce_analytics;


-- =========================================================
-- 1. MONTHLY SALES PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW vw_monthly_sales AS
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(
        SUM(oi.quantity * (oi.unit_price - p.cost_price)),
        2
    ) AS profit,
    ROUND(
        100.0 * SUM(oi.quantity * (oi.unit_price - p.cost_price))
        / SUM(oi.quantity * oi.unit_price),
        2
    ) AS profit_margin_percent
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m');


-- =========================================================
-- 2. PRODUCT PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW vw_product_performance AS
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    ROUND(
        SUM(oi.quantity * (oi.unit_price - p.cost_price)),
        2
    ) AS total_profit,
    ROUND(
        100.0 * SUM(oi.quantity * (oi.unit_price - p.cost_price))
        / SUM(oi.quantity * oi.unit_price),
        2
    ) AS profit_margin_percent
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
    p.brand;


-- =========================================================
-- 3. CATEGORY PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW vw_category_performance AS
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS product_count,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    ROUND(
        SUM(oi.quantity * (oi.unit_price - p.cost_price)),
        2
    ) AS total_profit,
    ROUND(
        100.0 * SUM(oi.quantity * (oi.unit_price - p.cost_price))
        / SUM(oi.quantity * oi.unit_price),
        2
    ) AS profit_margin_percent
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.category;


-- =========================================================
-- 4. CUSTOMER RFM ANALYSIS
-- =========================================================

CREATE OR REPLACE VIEW vw_customer_rfm AS

WITH rfm_base AS (

    SELECT
        c.customer_id,
        c.customer_name,

        DATEDIFF(
            (SELECT MAX(order_date) FROM orders),
            MAX(o.order_date)
        ) AS recency_days,

        COUNT(DISTINCT o.order_id) AS frequency,

        ROUND(
            SUM(oi.quantity * oi.unit_price),
            2
        ) AS monetary_value

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
        *,
        NTILE(5) OVER (
            ORDER BY recency_days DESC
        ) AS recency_score,

        NTILE(5) OVER (
            ORDER BY frequency
        ) AS frequency_score,

        NTILE(5) OVER (
            ORDER BY monetary_value
        ) AS monetary_score

    FROM rfm_base
)

SELECT
    *,
    CONCAT(
        recency_score,
        frequency_score,
        monetary_score
    ) AS rfm_score,

    CASE

        WHEN recency_score >= 4
             AND frequency_score >= 4
             AND monetary_score >= 4
            THEN 'Champions'

        WHEN recency_score >= 3
             AND frequency_score >= 3
            THEN 'Loyal Customers'

        WHEN recency_score >= 4
             AND frequency_score <= 2
            THEN 'Potential Loyalists'

        WHEN recency_score <= 2
             AND monetary_score >= 3
            THEN 'At Risk'

        ELSE 'Others'

    END AS customer_segment

FROM rfm_scores;


-- =========================================================
-- 5. PAYMENT METHOD PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW vw_payment_performance AS
SELECT
    o.payment_method,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(
        SUM(oi.quantity * oi.unit_price),
        2
    ) AS total_revenue,
    ROUND(
        SUM(oi.quantity * oi.unit_price)
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status = 'Delivered'
GROUP BY o.payment_method;


-- =========================================================
-- 6. BRAND PERFORMANCE
-- =========================================================

CREATE OR REPLACE VIEW vw_brand_performance AS
SELECT
    p.brand,
    SUM(oi.quantity) AS units_sold,
    ROUND(
        SUM(oi.quantity * oi.unit_price),
        2
    ) AS total_revenue,
    ROUND(
        SUM(
            oi.quantity *
            (oi.unit_price - p.cost_price)
        ),
        2
    ) AS total_profit,
    ROUND(
        100.0 *
        SUM(
            oi.quantity *
            (oi.unit_price - p.cost_price)
        )
        / SUM(oi.quantity * oi.unit_price),
        2
    ) AS profit_margin_percent
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
JOIN products p
    ON oi.product_id = p.product_id
WHERE o.status = 'Delivered'
GROUP BY p.brand;


-- =========================================================
-- 7. PRODUCT REVENUE RANKING WITHIN CATEGORY
-- =========================================================

WITH product_sales AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM order_items oi
    JOIN orders o
        ON oi.order_id = o.order_id
    JOIN products p
        ON oi.product_id = p.product_id
    WHERE o.status = 'Delivered'
    GROUP BY
        p.product_id,
        p.product_name,
        p.category
)

SELECT
    product_id,
    product_name,
    category,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (
        PARTITION BY category
        ORDER BY revenue DESC
    ) AS category_rank
FROM product_sales
ORDER BY category, category_rank;