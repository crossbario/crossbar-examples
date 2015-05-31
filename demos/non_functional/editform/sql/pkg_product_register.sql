BEGIN
   --
   -- Crossbar.io needs execute rights on package
   --
   EXECUTE IMMEDIATE 'GRANT EXECUTE ON pkg_product TO ' || crossbar.REPOUSER;

   --
   -- Register package procedures as RPC endpoints with Crossbar.io
   --
   crossbar.remove_exports('pkg_product');
   crossbar.export('pkg_product', 'crud_create', pkg_product.BASEURI || 'create');
   crossbar.export('pkg_product', 'crud_read',   pkg_product.BASEURI || 'read');
   crossbar.export('pkg_product', 'crud_update', pkg_product.BASEURI || 'update');
   crossbar.export('pkg_product', 'crud_delete', pkg_product.BASEURI || 'delete');
   crossbar.export('pkg_product', 'crud_upsert', pkg_product.BASEURI || 'upsert');
   crossbar.export('pkg_product', 'filter',      pkg_product.BASEURI || 'filter');
END;
/
