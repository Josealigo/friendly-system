CREATE TABLE covid.confirmed(
    id int primary key auto_increment,
    country_region varchar(50),
    province_state varchar(50),
    lat decimal(10,7),
    `long` decimal(10,7),
    event_date datetime(6),
    cases int
);

CREATE TABLE covid.deaths(
    id int primary key auto_increment,
    country_region varchar(50),
    province_state varchar(50),
    lat decimal(10,7),
    `long` decimal(10,7),
    event_date datetime(6),
    cases int
);

CREATE TABLE covid.recovered(
    id int primary key auto_increment,
    country_region varchar(50),
    province_state varchar(50),
    lat decimal(10,7),
    `long` decimal(10,7),
    event_date datetime(6),
    cases int
);