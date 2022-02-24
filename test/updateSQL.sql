alter table UserTBL change telegramID telegramID varchar(11);

alter table UserTBL drop primary key;
alter table UserTBL modify column telegramID varchar(11) PRIMARY KEY;


alter table UserTBL drop foreign key [name];

select * from information_schema.table_constraints where constraint_schema ='BokTing_T';

alter table UserTBL add sameGroup varchar(1) not null default 'N';
alter table UserTBL MODIFY COLUMN sameGroup varchar(1) AFTER enable;

alter table MatchTBL add accept varchar(1) not null default 'Y';
alter table MatchTBL add seq int default '1';

alter table MatchTBL MODIFY COLUMN accept varchar(1) AFTER coupling;
alter table MatchTBL MODIFY COLUMN seq int FIRST;

alter table MatchTBL drop accept;

alter table ReqTBL add comment varchar(2000);
alter table ReqTBL MODIFY COLUMN comment varchar(2000) AFTER area;
