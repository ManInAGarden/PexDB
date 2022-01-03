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

drop table experiment;

select * from factorvalue;

-- drop table catalog;
-- drop table unit;
-- drop table responsedefinition;

select
    fv.value
from 
    factorvalue fv, 
    factordefinition fd
where
    fv.factordefinitionid==fd._id;

.schema experimentdoc

.tables
