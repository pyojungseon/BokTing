create table MatchTBL
(
telegramID nvarchar(10) NOT NULL,
name nvarchar(30) NOT NULL,	
partnerID	nvarchar(10) NOT NULL,
partnerName nvarchar(30) NOT NULL,
coupling  nvarchar(1)  NOT NULL,
del nvarchar(1) NOT NULL,
regDate timestamp NOT NULL,
modDate timestamp NOT NULL
);

create table SugTBL
(
telegramID nvarchar(10) NOT NULL,
msg nvarchar(1000) NOT NULL,	
regDate timestamp NOT NULL,
modDate timestamp NOT NULL
);


create table NoticeTBL
(
seq int NOT NULL AUTO_INCREMENT,
msg nvarchar(1000) NOT NULL,	
send nvarchar(1) NOT NULL,
regDate timestamp NOT NULL,
modDate timestamp NOT NULL,
PRIMARY KEY(seq)
);

