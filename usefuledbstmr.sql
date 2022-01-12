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

delete from experimentdoc;

drop table experiment;

select * from factorvalue;

-- drop table catalog;
-- drop table unit;
-- drop table responsedefinition;
-- drop table experimentdoc;

select
    fv.value
from 
    factorvalue fv, 
    factordefinition fd
where
    fv.factordefinitionid==fd._id;

.schema experimentdoc

.tables
