create database Prot;
use prot;
create table registro(
idReg int(11) auto_increment primary key,
NomProy varchar(100) not null,
intdat varchar(100) not null,
Nom varchar(100) not null,
descripcion varchar(100) not null,
Arch blob not null,
fecha date not null,
varificado int(1) 
);
create table validados (
    usuario varchar(15) primary key not null,
    contraseña varchar(10) not null
);