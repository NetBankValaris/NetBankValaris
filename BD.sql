create database Prot;
use prot;
create table registro(
idReg int(11) auto_increment primary key,
nombre varchar(30) not null,
NomProy varchar(45) not null,
Descripcion varchar(200),
img blob not null,
fecha date not null
);