## drop tables before add modification and recreate table with modification
DROP TABLE IF EXISTS estDans
DROP TABLE IF EXISTS Novel
DROP TABLE IF EXISTS Serie

## create a table and specify columns (wich have type and lenght) and primary key
CREATE TABLE IF NOT EXISTS Novel (
    code_ISBN CHAR(17) NOT NULL,
	name CHAR(17),
	author VARCHAR(200),
	annee YEAR,
	CONSTRAINT pk_novel PRIMARY KEY(code_ISBN)
);

CREATE TABLE IF NOT EXISTS Serie (
    code_serie INT NOT NULL AUTO_INCREMENT,
	nom_serie VARCHAR(200),
	CONSTRAINT pk_serie PRIMARY KEY(code_serie)
);

## create a table wich specify the relation between 2 tables
CREATE TABLE IF NOT EXISTS estDans (
    code_ISBN CHAR(17) NOT NULL,
	code_serie INT NOT NULL,
	nom_serie VARCHAR(200),
	CONSTRAINT pk_estDans PRIMARY KEY(code_ISBN, code_serie)
	FOREIGN KEY (code_ISBN) REFERENCES Novel(code_ISBN)
	FOREIGN KEY (code_serie) REFERENCES Serie(code_serie)
);

## add "editor" columns in the table "Novel", "editor" columns  have "Character" type and lenght=200
ALTER TABLE Novel ADD COLUMN editor VARCHAR(200);

## add default value to columns in the table by using DEFAULT

## Insert line of data into table "Novel"
INSERT INTO Novel (code_ISBN, name, author, annee) VALUES (1, "NEVERWHERE", "Neil Gaiman", "1983");

# Command to view all entire table "Novel"
SELECT * FROM Novel;

## Insert line of data into AUTO_INCREMENT table "Serie". You do not need to specy auto_increment columns
INSERT INTO Serie (nom_serie) VALUES ("le seigneur des anneaux");

## Select some element in table 
SELECT name, author FROM Novel;

## Select some element in table with condition
SELECT name, author FROM Novel
WHERE name = "name_we_want"
WHERE name LIKE "begin_of_name_we_want"
WHERE name NOT LIKE "begin_of_name_we_want"
WHERE name BETWEEN "begin" and "end";

## Update line in table

## modification of line in table
UPDATE Novel
SET annee = 1986
WHERE condition;

## Filtered table 

## deline of line in table
DELETE from Novel
WHERE condition;

## Make a request to database with INNER JOIN. 
## select all columns from table "Novel" and Join (make intersection) with table "estdans" on the columns Novel.code_ISBN and estdans.code_ISBN
select * from Novel INNER JOIN estdans on Novel.code_ISBN = estdans.code_ISBN;


## Make a request to database with INNER JOIN. 
## INNER JOIN method is used for intersection on some columns of multiple table
## When intersection is not find, we will not get any response
select * from Novel 
INNER JOIN estdans on Novel.code_ISBN = estdans.code_ISBN
INNER JOIN serie on estdans.code_serie = serie.code_serie
WHERE serie.nom_serie LIKE "Le Seigneur des anneaux";


## Make a request to database with CROSS JOIN. 
## CROSS JOIN method is used to make all possible tuple combination between multiple table
drop table if exists lecteur;
create table if not exists lecteur
(
	code_lecteur int NOT NULL AUTO_INCREMENT,
    nom_lecteur VARCHAR(200),
    constraint pk_lecteur primary key(code_lecteur)
);

insert into lecteur (nom_lecteur) VALUES ("Martin");
insert into lecteur (nom_lecteur) VALUES ("Jeanne");
insert into lecteur (nom_lecteur) VALUES ("Robert");
commit;

select * from lecteur cross join Novel;


## Make a request to database with LEFT JOIN. 
## LEFT JOIN method is used for intersection on some columns of multiple table
## When intersection is not find, we will get a response with NULL on those lines
select * from Novel left JOIN estdans on Novel.code_ISBN = estdans.code_ISBN;


## Make a request to database with NATURAL JOIN. 
## NATURAL JOIN method is used for intersection on some columns of multiple table
## To use this method, you need to ensure that the columns on wich you use this method have the same name
select * from Novel NATURAL JOIN estdans;


## Make a request to database with IN and NOT IN. 
## IN is same like OR, but it IN makes request syntax simple and easier than OR
select * from Novel where auteur like "JK Rowling" OR auteur like "JRR Tolkien";
select * from Novel where auteur in ('JK Rowling', 'JRR Tolkien');
select * from Novel where annee in ('1954', '1955', '1999');


## Make a sub-request to database with IN and NOT IN. 
select * from Novel 
where code_isbn in (select code_isbn from estdans);

select * from Novel 
where code_isbn not in (select code_isbn from estdans);


## Make a sub-request to database with EXISTS
## The goal of this subrequest is to ensure that the data we select exist or not 
select * from Novel as A
where exists (select code_isbn from estdans where estdans.code_ISBN = A.code_ISBN);

select * from Novel as A
where not exists (select code_isbn from estdans where estdans.code_ISBN = A.code_ISBN);


## Make a request to database with UNION.
## This method UNION help you to make union with 2 or multiples columns
## To use this method, you need to ensure that the number and type of columns are the same name
select * from Novel where auteur LIKE "Isaac Asimov"
UNION
select * from Novel where annee = "1999";


## Make a request to database with INTERSECT.
select * from Novel 
where auteur LIKE "JK Rowling"
and code_isbn in (select code_isbn from Novel where annee = "1999");


## Make a request to database with EXCEPT.
select * from Novel 
where auteur LIKE "JK Rowling"
and code_isbn not in (select code_isbn from Novel where annee = "1999");


## Create index in table
## The goal is to make easier the research of some element in the table
ALTER TABLE Novel
ADD INDEX name_of_inex (name_of_columns);

ALTER TABLE Novel
drop index name_of_inex;


## scalar function for date
# pour avoir la date du moment 
select curDate();
# pour avoir lheure du moment
select curTime();
# pour avoir la date et lheure du moment
select now();

## Get "string" and convert it into date with format of date
SELECT STR_TO_DATE("05,01,2021","%d,%m,%Y");

## Get the date and convert it in "string" with format of date
SELECT DATE_FORMAT(now(), '%W %M %Y');

