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


# PAGO DE PLANILLAS
DROP TABLE IF EXISTS SpreadsPay;
CREATE TABLE SpreadsPay (
	id int primary key auto_increment,
    payAccount varchar(6) not null,
    payName varchar(50) not null,
    amount float null,
    isMensualPayPlan boolean not null,
    userBusiness varchar(50) null,
    account varchar(6) not null,
    foreign key (userBusiness) references BusinessUser (comercialName),
    foreign key (account) references Account (id)
);

# PAGO DE PROVEEDORES
DROP TABLE IF EXISTS ProvidersPay;
CREATE TABLE ProvidersPay (
	id int primary key auto_increment,
    payAccount varchar(6) not null,
    payName varchar(50) not null,
    amount float null,
    isMensualPayPlan boolean not null,
    userBusiness varchar(50) null,
    account varchar(6) not null,
    foreign key (userBusiness) references BusinessUser (comercialName),
    foreign key (account) references Account (id)
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

# PESTAMOS
DROP TABLE IF EXISTS Loans;
CREATE TABLE Loans (
	id int primary key auto_increment,
    amount float not null,
    plan int not null,
    interest int not null,
    description varchar(50) not null,
    canceledQuotas int not null,
    authorized boolean not null,
	userCui bigint null,
    userBusiness varchar(50) null,
    foreign key (userCui) references SingleUser (cui),
    foreign key (userBusiness) references BusinessUser (comercialName)
);

# CUOTA
DROP TABLE IF EXISTS LoanQuotas;
CREATE TABLE LoanQuotas (
	id int primary key auto_increment,
    loan int not null,
    date Date not null,
    payDate Date null,
	amount float null,
    account varchar(6) null,
	foreign key (account) references Account (id),
    foreign key (loan) references Loans (id)
);

# TARJETAS
DROP TABLE IF EXISTS Cards;
CREATE TABLE Cards (
	id int primary key, 
	brand varchar(50),
    credit float not null,
    debit float not null,
    lowLimit float not null,
	highLimit float not null,
	userCui bigint null,
	userBusiness varchar(50) null,
    account varchar(6) not null,
    foreign key (userCui) references SingleUser (cui),
    foreign key (account) references Account (id),
    foreign key (userBusiness) references BusinessUser (comercialName)
);

DROP TABLE IF EXISTS Purchases;
CREATE TABLE Purchases (
	id  int primary key auto_increment,
    date date not null,
    description varchar(50) null,
    amount float not null,
    isDollar boolean not null,
    idCard int not null,
	foreign key (idCard) references Cards (id)
); 

DROP TABLE IF EXISTS CardTransaction;
CREATE TABLE CardTransaction (
	id int primary key auto_increment,
	purchase int not null,
    prefepoints float not null,
    cashback float not null,
    foreign key (purchase) references Purchases (id)
);

# USUARIOS
INSERT INTO SingleUser VALUES (1111111111111, 123456789012, "Empleado", "2001/05/13", "employ", "123",35678555 );
INSERT INTO SingleUser VALUES (2222222222222, 123456789012, "Empleado2", "2001/05/13", "employ2", "123",35678555 );
INSERT INTO BusinessUser VALUES ("empresa", "Sociedad Anonima", "Mi Empresa", "Alex Santos", "123",35678555 );

INSERT into MonetaryAccount values (333333, "Cuenta empresarial");
INSERT into AccountType(id, monetary) values (333333, 333333);
INSERT into Account values (333333,0,0,1,0, 0,0,null, "empresa", 15, 0);

INSERT into MonetaryAccount values (541234, "Cuenta 1");
INSERT into AccountType(id, monetary) values (541234, 541234);
INSERT into Account values (541234,0,0,1,0, 0,0,1111111111111, null, 15, 0);

INSERT into MonetaryAccount values (263769, "Cuenta 2");
INSERT into AccountType(id, monetary) values (263769, 263769);
INSERT into Account values (263769,0,0,1,0, 0,0,1111111111111, null, 15, 0);

INSERT into MonetaryAccount values (481366, "Cuenta 3");
INSERT into AccountType(id, monetary) values (481366, 481366);
INSERT into Account values (481366,0,0,1,0, 0,0,1111111111111, null, 15, 0);

INSERT into MonetaryAccount values (152352, "Cuenta 4");
INSERT into AccountType(id, monetary) values (152352, 152352);
INSERT into Account values (152352,0,0,1,0, 0,0,1111111111111, null, 15, 0);

INSERT into MonetaryAccount values (358054, "Cuenta 5");
INSERT into AccountType(id, monetary) values (358054, 358054);
INSERT into Account values (358054,0,0,1,0, 0,0,1111111111111, null, 15, 0);

INSERT into MonetaryAccount values (503944, "Cuenta 6");
INSERT into AccountType(id, monetary) values (503944, 503944);
INSERT into Account values (503944,0,0,1,0, 0,0,2222222222222, null, 15, 0);

INSERT into MonetaryAccount values (316167, "Cuenta 7");
INSERT into AccountType(id, monetary) values (316167, 316167);
INSERT into Account values (316167,0,0,1,0, 0,0,2222222222222, null, 15, 0);

INSERT into MonetaryAccount values (374296, "Cuenta 8");
INSERT into AccountType(id, monetary) values (374296, 374296);
INSERT into Account values (374296,0,0,1,0, 0,0,2222222222222, null, 15, 0);

INSERT into MonetaryAccount values (556658, "Cuenta 9");
INSERT into AccountType(id, monetary) values (556658, 556658);
INSERT into Account values (556658,0,0,1,0, 0,0,2222222222222, null, 15, 0);

INSERT into MonetaryAccount values (462978, "Cuenta 10");
INSERT into AccountType(id, monetary) values (462978, 462978);
INSERT into Account values (462978,0,0,1,0, 0,0,2222222222222, null, 15, 0);

select * from Account;
