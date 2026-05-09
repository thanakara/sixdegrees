CREATE FULLTEXT INDEX person_name_ft IF NOT EXISTS
FOR (p:Person) ON EACH [p.name];

CREATE FULLTEXT INDEX movie_title_ft IF NOT EXISTS
FOR (m:Movie) ON EACH [m.title];
