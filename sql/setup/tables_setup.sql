-- Create table Dealer
CREATE TABLE IF NOT EXISTS Dealer (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- Create table Car
CREATE TABLE IF NOT EXISTS Car (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL CHECK (year >= 1886),
    color VARCHAR(30),
    price NUMERIC(12,2) NOT NULL CHECK (price > 0),
    dealer_id INT REFERENCES Dealer(id)
);

-- Create table CarInfo
CREATE TABLE IF NOT EXISTS CarInfo (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    car_id INT REFERENCES Car(id) ON DELETE CASCADE,
    mpg INT NOT NULL CHECK (mpg > 0),
    fuel_type VARCHAR(20) NOT NULL,
    features TEXT
);

-- Create table Sale
CREATE TABLE IF NOT EXISTS Sale (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    car_id INT REFERENCES Car(id) ON DELETE CASCADE,
    dealer_id INT REFERENCES Dealer(id),
    customer_name VARCHAR(100) NOT NULL,
    customer_contact VARCHAR(100),
    sale_date DATE DEFAULT CURRENT_DATE,
    sale_price NUMERIC(12,2) NOT NULL,
    payment_method VARCHAR(30)
);
