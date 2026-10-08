DELETE FROM products;
DELETE FROM sqlite_sequence WHERE name = 'products';

INSERT INTO products (restaurant_id, category_id, name, calories, price, rating, description, image_url, stock, is_available) VALUES
(1, 1, 'Margherita Pizza', 850, 180, 4.7, 'Classic cheese pizza', 'https://example.com/margherita.jpg', 25, 1),
(1, 1, 'Pepperoni Pizza', 950, 220, 4.8, 'Pepperoni & cheese pizza', 'https://example.com/pepperoni.jpg', 20, 1),
(2, 2, 'Classic Burger', 700, 150, 4.5, 'Beef burger', 'https://example.com/classic-burger.jpg', 30, 1),
(2, 2, 'Chicken Burger', 650, 140, 4.4, 'Grilled chicken burger', 'https://example.com/chicken-burger.jpg', 25, 1),
(3, 3, 'Salmon Sushi', 450, 300, 4.9, 'Fresh salmon sushi', 'https://example.com/salmon-sushi.jpg', 15, 1);

INSERT INTO products (restaurant_id, category_id, name, calories, price, rating, description, stock, is_available) VALUES
(4, 4, ' Salad', 350, 120, 4.6, 'Fresh salad', 20, 1);
