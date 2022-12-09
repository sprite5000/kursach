SELECT user FROM mysql.user;
CREATE DATABASE sasha;
USE sasha;
CREATE USER 'sasha_app'@'localhost' IDENTIFIED BY 'sasha_pass';
GRANT ALL PRIVILEGES ON sasha.* TO 'sasha_app'@'localhost';

CREATE TABLE IF NOT EXISTS status
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(41) NOT NULL,
    isLegal boolean NOT NULL default false,
    isSimpleTax boolean NOT NULL default false,
    code int NOT NULL
);

CREATE TABLE IF NOT EXISTS taxpayers
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(31) NOT NULL,
    surname varchar(31) NOT NULL,
    address varchar(61) NOT NULL,
    idPassport varchar(15) NOT NULL,
    idStatus int NOT NULL,
    phoneNumber varchar(15) NOT NULL,
    email varchar(35) NOT NULL,
    password varchar(111) NOT NULL,
    FOREIGN KEY (idStatus) REFERENCES status (id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS sources
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(31) NOT NULL,
    description TEXT,
    country varchar(31)
);

INSERT INTO sources(name, description, country)
VALUES ('Заработная плата', 'описание', 'Беларусь'),
('Выигрыш', 'описание', 'Беларусь'),
('Проценты от вклада', 'описание', 'Беларусь'),
('Доход производства', 'описание', 'Беларусь'),
('Доход хозяйства', 'описание', 'Беларусь'),
('Инвестиции из-вне', 'описание', 'Германия');

CREATE TABLE IF NOT EXISTS incomes
(
    id int primary key NOT NULL AUTO_INCREMENT,
    value decimal NOT NULL,
    idSource int NOT NULL,
    idPayer int NOT NULL,
    description TEXT,
    FOREIGN KEY (idSource) REFERENCES sources (id) ON DELETE CASCADE,
    FOREIGN KEY (idPayer) REFERENCES taxpayers (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS expenses
(
    id int primary key NOT NULL AUTO_INCREMENT,
    value decimal NOT NULL,
    country varchar(31),
    idPayer int NOT NULL,
    description TEXT,
    FOREIGN KEY (idPayer) REFERENCES taxpayers (id) ON DELETE CASCADE
);

INSERT INTO status (name, isLegal, isSimpleTax, code)
VALUES ('ЗАО', true, true, 211287),
('ИП', false, true, 311386),
('ООО', true, true, 211486),
('ОАО', true, true, 292236),
('ЧУП', true, true, 228466),
('Самозанятый', false, false, 218536);

INSERT INTO status(id, name, isLegal, isSimpleTax, code)
VALUES (0, 'Не определено', false, false, 111111);






















CREATE TABLE IF NOT EXISTS cars
(
    id int primary key NOT NULL AUTO_INCREMENT,
    vin varchar(17) NOT NULL,
    number varchar(9) NOT NULL,
    mark varchar(31) NOT NULL,
    model varchar(31) NOT NULL,
    year int NOT NULL,
    fuel enum('бензин', 'дизель', 'гибрид', 'электричество') NOT NULL default 'бензин'
);

CREATE TABLE IF NOT EXISTS car_type
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(21) NOT NULL,
    cost decimal NOT NULL
);

CREATE TABLE IF NOT EXISTS life_type
(
    id int primary key NOT NULL AUTO_INCREMENT,
    name varchar(21) NOT NULL,
    cost decimal NOT NULL,
    duration int NOT NULL
);

CREATE TABLE user_car
(
    id int primary key NOT NULL AUTO_INCREMENT,
    idcar int NOT NULL,
    iduser int NOT NULL,
    idtype int NOT NULL,
    timing timestamp default NOW(),
    FOREIGN KEY (idcar) REFERENCES cars (id) ON DELETE CASCADE,
    FOREIGN KEY (iduser) REFERENCES clients (id) ON DELETE CASCADE,
    FOREIGN KEY (idtype) REFERENCES car_type (id) ON DELETE CASCADE
);

CREATE TABLE user_life
(
    id int primary key NOT NULL AUTO_INCREMENT,
    iduser int NOT NULL,
    idtype int NOT NULL,
    timing timestamp default NOW(),
    FOREIGN KEY (iduser) REFERENCES clients (id) ON DELETE CASCADE,
    FOREIGN KEY (idtype) REFERENCES life_type (id) ON DELETE CASCADE
);


INSERT INTO car_type (name, cost)
VALUES ('КАСКО', 85),
       ('Cтандарт', 55),
       ('Про', 125),
       ('Cпортивная', 155);

INSERT INTO life_type (name, cost, duration)
VALUES ('Детский', 45, 12),
       ('Cтандарт', 55, 12),
       ('Путешествия', 55, 2),
       ('Cпортивная', 65, 6);


