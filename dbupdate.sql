ALTER TABLE projectresponsepreparation ADD COLUMN combinationweight REAL;

ALTER TABLE project ADD COLUMN domergecalculation TEXT;
ALTER TABLE project ADD COLUMN mergeformula TEXT;

ALTER TABLE envirovalue add COLUMN value FLOAT;

ALTER TABLE projectfactorpreparation ADD COLUMN isnegated TEXT;
ALTER TABLE projectfactorpreparation ADD COLUMN iscombined TEXT;
update projectfactorpreparation set isnegated=0  where isnegated ISNULL;
update projectfactorpreparation set iscombined=0  where iscombined ISNULL;
--select * from projectfactorpreparation;
