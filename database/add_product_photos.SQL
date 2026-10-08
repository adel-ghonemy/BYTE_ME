-- A photo link for each dish. Run it once:
--   sqlite3 database/database.db < database/add_product_photos.SQL
-- The photos come from Wikipedia / Wikimedia Commons and TheMealDB.

-- This dish's name starts with a space in the database.
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/94/Salad_platter.jpg/960px-Salad_platter.jpg' WHERE name = ' Salad';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/5/57/Neapolitan_pizza_at_Trappica_%2848701940197%29.jpg/960px-Neapolitan_pizza_at_Trappica_%2848701940197%29.jpg' WHERE name = 'Margherita Pizza';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0c/Pepperoni_Pizza_%2829204589095%29.jpg/960px-Pepperoni_Pizza_%2829204589095%29.jpg' WHERE name = 'Pepperoni Pizza';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/2/23/Glass_of_Cola.jpg/960px-Glass_of_Cola.jpg' WHERE name = 'Cola';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/0b/RedDot_Burger.jpg/960px-RedDot_Burger.jpg' WHERE name = 'Classic Burger';
UPDATE products SET image_url = 'https://www.themealdb.com/images/media/meals/vdwloy1713225718.jpg' WHERE name = 'Chicken Burger';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/05/Orangejuice.jpg/960px-Orangejuice.jpg' WHERE name = 'Orange Juice';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/6/60/Sushi_platter.jpg/960px-Sushi_platter.jpg' WHERE name = 'Salmon Sushi';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/9/9f/California_Sushi_%2826571101885%29.jpg/960px-California_Sushi_%2826571101885%29.jpg' WHERE name = 'California Roll';
UPDATE products SET image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/36/Green_tea_3_appearances.jpg' WHERE name = 'Green Tea';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/3/38/Koofteh_tabrizi.jpg/960px-Koofteh_tabrizi.jpg' WHERE name = 'Grilled Kofta';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/0/00/Shawarma_2.jpg/960px-Shawarma_2.jpg' WHERE name = 'Chicken Shawarma';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/4/41/Tunisian_Tea_with_pine_nuts.jpg/960px-Tunisian_Tea_with_pine_nuts.jpg' WHERE name = 'Mint Tea';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/7/76/Chicken_Salad_Chick_Classic_Carol_scoop%2C_Jan_2020.jpg/960px-Chicken_Salad_Chick_Classic_Carol_scoop%2C_Jan_2020.jpg' WHERE name = 'Chicken Salad';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/7/74/Fruktsallad_%28Fruit_salad%29.jpg/960px-Fruktsallad_%28Fruit_salad%29.jpg' WHERE name = 'Fruit Bowl';
UPDATE products SET image_url = 'https://thumb.wikimedia.org/wikipedia/commons/thumb/1/10/Lemonade_-_27682817724.jpg/960px-Lemonade_-_27682817724.jpg' WHERE name = 'Fresh Lemonade';
