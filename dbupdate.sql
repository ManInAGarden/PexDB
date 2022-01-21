ALTER TABLE projectresponsepreparation ADD COLUMN combinationweight REAL;

ALTER TABLE project ADD COLUMN domergecalculation TEXT;
ALTER TABLE project ADD COLUMN mergeformula TEXT;

ALTER TABLE envirovalue add COLUMN value FLOAT;

.schema project
