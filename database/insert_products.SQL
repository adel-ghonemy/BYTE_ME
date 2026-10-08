DELETE FROM products;
DELETE FROM sqlite_sequence WHERE name = 'products';

INSERT INTO products (restaurant_id, category_id, name, calories, price, rating, description, image_url, stock, is_available) VALUES
(1, 1, 'Margherita Pizza', 850, 180, 4.7, 'Classic cheese pizza', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/57/Neapolitan_pizza_at_Trappica_%2848701940197%29.jpg/960px-Neapolitan_pizza_at_Trappica_%2848701940197%29.jpg', 25, 1),
(1, 1, 'Pepperoni Pizza', 950, 220, 4.8, 'Pepperoni & cheese pizza', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0c/Pepperoni_Pizza_%2829204589095%29.jpg/960px-Pepperoni_Pizza_%2829204589095%29.jpg', 20, 1),
(2, 2, 'Classic Burger', 700, 150, 4.5, 'Beef burger', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0b/RedDot_Burger.jpg/960px-RedDot_Burger.jpg', 30, 1),
(2, 2, 'Chicken Burger', 650, 140, 4.4, 'Grilled chicken burger', 'https://www.themealdb.com/images/media/meals/vdwloy1713225718.jpg', 25, 1),
(3, 3, 'Salmon Sushi', 450, 300, 4.9, 'Fresh salmon sushi', 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/60/Sushi_platter.jpg/960px-Sushi_platter.jpg', 15, 1);

INSERT INTO products (restaurant_id, category_id, name, calories, price, rating, description, stock, is_available) VALUES
(4, 4, ' Salad', 350, 120, 4.6, 'Fresh salad', 20, 1);
