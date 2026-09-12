-- E-Commerce Sales & Customer Analytics
-- Sales Analysis

USE ecommerce_analytics;


-- 1. Total Revenue from Delivered Orders

SELECT
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.status = 'Delivered';