-- SQLite
select * from factordefinition;

delete from factordefinition where abbreviation is NULL;

select * from unit;

select * from experiment;

-- delete  from experiment;

select * from catalog;

select * from project;

select * from responsedefinition;

select * from projectresponsepreparation;

select * from responsevalue;

select * from experimentdoc;

update envirodefinition set name = 'case temperature' where name = 'case temperatur';

select * from envirodefinition;


select * from catalog order by type;

delete from catalog where type == "PICTURE_TYPE";


select * from factorvalue;

select * from envirodefinition;

-- drop table catalog;
-- drop table unit;
-- drop table responsedefinition;
-- drop table experimentdoc;
-- drop table experiment;
-- drop TABLE envirodefinition;

select
    fv.value
from 
    factorvalue fv, 
    factordefinition fd
where
    fv.factordefinitionid==fd._id;

.schema experimentdoc

.schema projectfactorpreparation

.schema projectresponsepreparation

.schema project

.tables
