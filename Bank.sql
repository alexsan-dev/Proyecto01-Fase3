# CREAR BASE DE DATOS
DROP DATABASE IF EXISTS bank;
CREATE DATABASE IF NOT EXISTS bank;
USE bank;

# TABLA DE USUARIO INDIVIDUAL
DROP TABLE IF EXISTS SingleUser;
CREATE TABLE SingleUser(
	cui bigint,
    nit bigint not null,
	name varchar(30) not null,
    birth date not null,
    username varchar(30),
    password varchar(30) not null,
    phone int(8),
    PRIMARY KEY (cui, username)
);

# TABLA DE USUARIO EMPRESARIAL
DROP TABLE IF EXISTS BusinessUser;
CREATE TABLE BusinessUser(
	comercialName varchar(50) primary key,
    businessType varchar(50),
    name varchar(30) not null,
    agent varchar(30) not null,
    password varchar(30) not null,
    phone int
);

# CUENTA DE AHORRO
DROP TABLE IF EXISTS SavingAccount;
CREATE TABLE SavingAccount (
	id varchar(6) primary key,
    interest float
);

# CUENTA DE AHORRO A PLAZO
DROP TABLE IF EXISTS TimedSavingAccount;
CREATE TABLE TimedSavingAccount (
	id varchar(6) primary key, 
    interest float,
    plan date not null
);

# CUENTA MONETARIA
DROP TABLE IF EXISTS MonetaryAccount;
CREATE TABLE MonetaryAccount (
	id varchar(6) primary key,
    description varchar(50)
);

# TIPO DE CUENTA
DROP TABLE IF EXISTS AccountType;
CREATE TABLE AccountType (
	id varchar(6) primary key,
	saving varchar(6) null,
    timedSaving varchar(6) null, 
    monetary varchar(6) null,
    foreign key (saving) references SavingAccount (id),
    foreign key (timedSaving) references TimedSavingAccount (id),
    foreign key (monetary) references MonetaryAccount (id)
);

# TABLA DE CUENTA
DROP TABLE IF EXISTS Account;
CREATE TABLE Account(
	id varchar(6) primary key,
    state boolean default true not null,
	enableChecks boolean default true not null,
    isSingle boolean not null,
    credit float not null,
    debit float not null,
    isDollar boolean not null,
    userCui bigint null,
    userBusiness varchar(50) null,
    checks int not null,
    enableAuthChecks boolean not null,
    foreign key (userCui) references SingleUser (cui),
    foreign key (userBusiness) references BusinessUser (comercialName),
	foreign key (id) references AccountType (id)
);

# CUENTA DE TERCEROS
DROP TABLE IF EXISTS ThirdAccount;
CREATE TABLE ThirdAccount (
	id varchar(6) primary key,
    userCui bigint null,
    userBusiness varchar(50) null,
    thirdCui bigint null,
    thirdBusiness varchar(50) null,
    accountType varchar(50) null,
    foreign key (userCui) references SingleUser (cui),
    foreign key (userBusiness) references BusinessUser (comercialName)
);

# TRANSACCIONES
DROP TABLE IF EXISTS Transactions;
CREATE TABLE Transactions (
	id int primary key auto_increment,
    amount float not null,
    description varchar(20), 
    date date not null,
    originAccount varchar(6) not null,
    destAccount varchar(6) not null,
    isThird boolean not null,
	foreign key (originAccount) references Account (id)
);

# CHEQUES
DROP TABLE IF EXISTS AccountCheck;
CREATE TABLE AccountCheck (
	id int primary key auto_increment,
    name varchar(30) null,
    date date null,
    amount float null,
	account varchar(6) not null,
    chargedDate date null,
    charged boolean,
	foreign key (account) references Account (id)
);

# PREAUTORIZACION DE CHEQUES
DROP TABLE IF EXISTS AuthCheck;
CREATE TABLE AuthCheck (
	id int primary key,
    authorized boolean not null,
    foreign key (id) references AccountCheck (id)
);


