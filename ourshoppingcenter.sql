create database ourshoppingcenter;
use ourshoppingcenter;




create table customer
(cust_id varchar(20) primary key,
fname varchar(30) NOT NULL,
lname varchar(30) not null,
dob date NOT NULL,
gender set("M", "F", "O"),
address varchar(50),
email varchar(50) NOT NULL,
phone_number bigint(10) NOT NULL);



create table products
(pid varchar(20) primary key
,pname varchar(50) NOT NULL
,ptype varchar(30));

create table productsdetail
(SN int primary key auto_increment,
pid varchar(20) not null,
quantity int not null,
order_datetime datetime not null,
cp float not null,
sp float not null,
foreign key(pid) references products(pid));

create table products_sold
(
bill_num int not null,
pid varchar(20) not null,
quantity int not null,
cust_id varchar(20),
sold_datetime datetime not null,
primary key(bill_num,pid),
foreign key(cust_id) references customer(cust_id),
foreign key(pid) references products(pid));

