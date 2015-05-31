DECLARE
   l_cnt NUMBER(10);
BEGIN
   EXECUTE IMMEDIATE 'TRUNCATE TABLE person';

   INSERT /*+ APPEND */ INTO person
      SELECT ROWNUM AS id,
             s.sname,
             s.uri,
             s.name,
             s.surname,
             s.givenname,
             s.birthdate,
             s.birthplace,
             s.deathdate,
             s.deathplace,
             s.descr
         FROM (SELECT * FROM person_load ORDER BY sname, uri) s;
   COMMIT;

   DBMS_STATS.gather_table_stats(ownname => sys_context('USERENV', 'CURRENT_SCHEMA'),
                                 tabname => 'PERSON',
                                 estimate_percent => NULL,
                                 method_opt => 'FOR ALL COLUMNS',
                                 degree => DBMS_STATS.AUTO_DEGREE,
                                 cascade => TRUE,
                                 force => TRUE);

   -- force full scan to warm up DB buffer cache
   SELECT COUNT(DISTINCT uri) INTO l_cnt FROM person;
END;
/
