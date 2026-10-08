DELETE FROM restaurant;
DELETE FROM sqlite_sequence WHERE name = 'restaurant';

INSERT INTO restaurant (name, opendate, address, type, phone) VALUES
('Pizza King', '2020-01-15', 'Cairo', 'Pizza', '01011111111'),
('Burger House', '2019-06-10', 'Alexandria', 'Fast Food', '01122222222'),
('Sushi Time', '2021-03-20', 'Giza', 'Japanese', '01233333333'),
('Grill Master', '2018-09-05', 'Mansoura', 'Grill', '01544444444'),
('Healthy Food', '2022-02-12', 'Tanta', 'Healthy', '01055555555');
