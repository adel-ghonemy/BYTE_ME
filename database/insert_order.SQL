DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM sqlite_sequence WHERE name = 'order_items';
DELETE FROM sqlite_sequence WHERE name = 'orders';

INSERT INTO orders (user_id, restaurant_id, user_address_id, order_number, status, notes, total_price, payment_status) VALUES
(1, 1, NULL, 'ORD-1001', 'pending', 'First demo order', 180, 'pending'),
(2, 2, NULL, 'ORD-1002', 'preparing', 'Second demo order', 220, 'paid');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 180),
(2, 2, 1, 220);
