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

drop table if exists categoria;
create table if not exists categoria(
idcategoria int(3) auto_increment,
descrip varchar(45) not null,
PRIMARY KEY(`idcategoria`)
);

create table if not exists registro(
idreg int(11) auto_increment,
nomproy varchar(100) not null,
intdat varchar(100) not null,
nom varchar(100) not null,
descripcion varchar(100) not null,
extarch varchar(5) not null,
fecha date not null,
usuario_ref varchar(15) not null,
verificado int(1),
categoria_ref int(3),
primary key(`idreg`),
Constraint RegValRel Foreign Key (usuario_ref) references validados(usuario) on delete restrict on update restrict,
Constraint RegCatRel Foreign Key (categoria_ref) references categoria(idcategoria) on delete restrict on update restrict
);
insert into validados(usuario, contraseña) values ("Jose Juan", "JoseJuan08"), ("Regina", "Regina09"), ("Elvia Yuridia", "Mimor09");

insert into categoria(descrip) values ("Prototipos"), ("Emprendedor"), ("Robótico"), ("Industrial");
