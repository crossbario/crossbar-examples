BEGIN
   BEGIN
      EXECUTE IMMEDIATE 'crossbar.remove_exports(''pkg_autcomplete'')';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP PACKAGE pkg_autcomplete';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;
/*
   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE person';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE person_load';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;
*/
END;
/
