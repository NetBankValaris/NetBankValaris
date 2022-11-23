drop database if exists prot;

create database if not exists prot;
use prot;

drop table if exists validados;
drop table if exists registro;

create table if not exists validados (
usuario varchar(15) not null,
contraseña varchar(10) not null,
primary key(usuario) 
);
create table if not exists registro(
idReg int(11) auto_increment,
nomproy varchar(100) not null,
intdat varchar(100) not null,
nom varchar(100) not null,
descripcion varchar(100) not null,
arch blob not null,
fecha date not null,
usuario_ref varchar(15) not null,
verificado int(1),
primary key(idReg),
Constraint RegValRel Foreign Key (usuario_ref) references validados(usuario) on delete restrict on update restrict
);
insert into validados(usuario, contraseña) values ("Jose Juan", "JoseJuan08"), ("Regina", "Regina09"), ("Elvia Yuridia", "Mimor09");