DELETE FROM users;
DELETE FROM sqlite_sequence WHERE name = 'users';

INSERT INTO users (name, age, address, email, phone, password, role, dob) VALUES
('Ahmed Ali', 22, 'Cairo', 'ahmed1@gmail.com', '01010000001', 'pass123', 'customer', '2002-01-05'),
('Mohamed Hassan', 24, 'Alexandria', 'mohamed2@gmail.com', '01010000002', 'pass123', 'restaurant_owner', '2000-02-10'),
('Sara Mohamed', 21, 'Giza', 'sara3@gmail.com', '01010000003', 'pass123', 'customer', '2003-06-18');
