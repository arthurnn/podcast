
drop table if exists item;
create table item (
    id int(11) not null auto_increment,
    title varchar(255) not null,
    website varchar(500) not null,
    author varchar(255),
	price varchar(255),
	category varchar(255),
	lang varchar(255),
	email varchar(255) not null,
    created int(11) not null comment "unix timestamp",
    primary key (id),
    key (website)
) engine=innodb default charset=utf8;
