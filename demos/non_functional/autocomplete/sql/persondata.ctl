load data
characterset utf8
replace
into table person_load
fields terminated by ";" optionally enclosed by '"'
trailing nullcols
(
   sname,
   uri,
   name,
   surname,
   givenname,
   birthdate "TO_DATE(:birthdate, 'YYYY-MM-DD')",
   birthplace,
   deathdate "TO_DATE(:deathdate, 'YYYY-MM-DD')",
   deathplace,
   descr CHAR(4000)
)
