CREATE INDEX movie_title IF NOT EXISTS
FOR (m:Movie)
ON (m.title);

CREATE INDEX movie_year IF NOT EXISTS
FOR (m:Movie)
ON (m.year);

CREATE INDEX person_name IF NOT EXISTS
FOR (p:Person)
ON (p.name);

CREATE INDEX person_birth_year IF NOT EXISTS
FOR (p:Person)
ON (p.birthYear);

CREATE INDEX genre_name IF NOT EXISTS
FOR (g:Genre)
ON (g.genre);
