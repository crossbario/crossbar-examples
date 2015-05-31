DECLARE
   l_exists INTEGER;
BEGIN
   SELECT COUNT(*) INTO l_exists FROM user_tables WHERE LOWER(table_name) = 'person';
   IF l_exists = 0 THEN
      EXECUTE IMMEDIATE 'CREATE TABLE person ' ||
                        '(' ||
                        '   id             NUMBER(10,0)      NOT NULL,' ||
                        '   sname          NVARCHAR2(200)    NOT NULL,' ||
                        '   uri            VARCHAR2(1000)    NOT NULL,' ||
                        '   name           NVARCHAR2(200),' ||
                        '   surname        NVARCHAR2(200),' ||
                        '   givenname      NVARCHAR2(200),' ||
                        '   birthdate      DATE,' ||
                        '   birthplace     NVARCHAR2(1000),' ||
                        '   deathdate      DATE,' ||
                        '   deathplace     NVARCHAR2(1000),' ||
                        '   descr          NVARCHAR2(2000),' ||
                        '   PRIMARY KEY (sname, uri)' ||
                        ') ' ||
                        'ORGANIZATION INDEX COMPRESS ' ||
                        'STORAGE (BUFFER_POOL KEEP) ' ||
                        'OVERFLOW TABLESPACE USERS';
   END IF;

   SELECT COUNT(*) INTO l_exists FROM user_indexes WHERE LOWER(index_name) = 'idx_person_id';
   IF l_exists = 0 THEN
      EXECUTE IMMEDIATE 'CREATE UNIQUE INDEX idx_person_id ON person (id)';
   END IF;

   SELECT COUNT(*) INTO l_exists FROM user_tables WHERE LOWER(table_name) = 'person_load';
   IF l_exists = 0 THEN
      EXECUTE IMMEDIATE 'CREATE TABLE person_load ' ||
                        '(' ||
                        '   sname          NVARCHAR2(200)    NOT NULL,' ||
                        '   uri            VARCHAR2(1000)    NOT NULL,' ||
                        '   name           NVARCHAR2(200)    NOT NULL,' ||
                        '   surname        NVARCHAR2(200),' ||
                        '   givenname      NVARCHAR2(200),' ||
                        '   birthdate      DATE,' ||
                        '   birthplace     NVARCHAR2(1000),' ||
                        '   deathdate      DATE,' ||
                        '   deathplace     NVARCHAR2(1000),' ||
                        '   descr          NVARCHAR2(2000)' ||
                        ')';
   END IF;
END;
/
