-- SQLite
select * from factordefinition;

delete from factordefinition where abbreviation is NULL;

select * from unit;

select * from experiment;

-- delete  from experiment;

select * from catalog;

select * from project;

select * from responsevalue;

-- drop table catalog;

select
    fv.value
from 
    factorvalue fv, 
    factordefinition fd
where
    fv.factordefinitionid==fd._id;

.schema factordefinition

.tables
