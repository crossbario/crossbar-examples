BEGIN
   BEGIN
      EXECUTE IMMEDIATE 'crossbar.remove_exports(''pkg_product'')';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP PACKAGE pkg_product';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP TABLE product';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;

   BEGIN
      EXECUTE IMMEDIATE 'DROP SEQUENCE product_id';
   EXCEPTION
      WHEN OTHERS THEN
         NULL;
   END;
END;
/
