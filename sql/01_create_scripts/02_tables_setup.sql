-- Create table Dealer
create table if not exists Dealer (
    id int generated always as identity primary key,
    name varchar(100) not null,
    address varchar(200),
    city varchar(100),
    state varchar(50),
    phone varchar(20),
    email varchar(100)
);

-- Create table Car
create table if not exists Car (
    id int generated always as identity primary key,
    brand varchar(50) not null,
    model varchar(50) not null,
    year int not null check (year >= 1886),
    color varchar(30),
    price numeric(12,2) not null check (price > 0),
    dealer_id int references Dealer(id)
);

-- Create table CarInfo
create table if not exists CarInfo (
    id int generated always as identity primary key,
    car_id int references Car(id) on delete cascade,
    mpg int not null check (mpg > 0),
    fuel_type varchar(20) not null,
    features text
);

-- Create table Sale
create table if not exists Sale (
    id int generated always as identity primary key,
    car_id int references Car(id) on delete cascade,
    dealer_id int references Dealer(id),
    customer_name varchar(100) not null,
    customer_contact varchar(100),
    sale_date date default current_date,
    sale_price numeric(12,2) not null,
    payment_method varchar(30)
);
