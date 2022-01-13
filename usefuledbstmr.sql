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

select * from catalog order by type;

delete from catalog where type == "PICTURE_TYPE";


select * from factorvalue;

-- drop table catalog;
-- drop table unit;
-- drop table responsedefinition;
-- drop table experimentdoc;
-- drop table experiment;

select
    fv.value
from 
    factorvalue fv, 
    factordefinition fd
where
    fv.factordefinitionid==fd._id;

.schema experimentdoc

.tables
