insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Algorithm')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Data Structure')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Operating System')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'System Programming')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'DBMS')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'RDBMS')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Computer Networks')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Algebra')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Geometry')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Statistics')) ;
insert into ABC_booktype (typeName_id) (select id from ABC_refbooks where novelType like (select id from ABC_subject where subject like 'Calculas')) ;
