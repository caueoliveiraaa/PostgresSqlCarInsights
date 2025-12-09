-- Creates table Dealer
CREATE TABLE Dealer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- Creates table Car
CREATE TABLE Car (
    id SERIAL PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    color VARCHAR(30),
    price NUMERIC(12,2) NOT NULL,
    dealer_id INT REFERENCES Dealer(id)
);

-- Creates table Sale
CREATE TABLE Sale (
    id SERIAL PRIMARY KEY,
    car_id INT REFERENCES Car(id) ON DELETE CASCADE,
    dealer_id INT REFERENCES Dealer(id),
    customer_name VARCHAR(100) NOT NULL,
    customer_contact VARCHAR(100),
    sale_date DATE DEFAULT CURRENT_DATE,
    sale_price NUMERIC(12,2) NOT NULL,
    payment_method VARCHAR(30)
);

-- Creates table CarInfo
CREATE TABLE CarInfo (
    id SERIAL PRIMARY KEY,
    car_id INT REFERENCES Car(id) ON DELETE CASCADE,
    mpg INT,
    fuel_type VARCHAR(20),
    features TEXT
);
