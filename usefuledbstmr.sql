-- SQLite
select * from factordefinition;

delete from factordefinition where abbreviation is NULL;

select * from unit;

select * from experiment;

select
    fd.name,
    fv.value
from 
    factorvalue fv, 
    factordefinition fd
where
    fv.factordefinitionid==fd._id;