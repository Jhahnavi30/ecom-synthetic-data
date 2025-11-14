SELECT
    u.name AS user_name,
    o.order_id,
    p.name AS product_name,
    oi.quantity,
    oi.item_price,
    pay.payment_method,
    o.order_date
FROM users u
JOIN orders o ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
JOIN payments pay ON pay.order_id = o.order_id
ORDER BY o.order_date DESC;


