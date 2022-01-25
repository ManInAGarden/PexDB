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

select * from commoninter;

select * from factorcombipreparation;

select * from commoninter;



-- drop table catalog;
-- drop table unit;
-- drop table responsedefinition;
-- drop table experimentdoc;
-- drop table experiment;
-- drop TABLE envirodefinition;
-- drop table commoninter;

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

.schema commoninter

.tables
