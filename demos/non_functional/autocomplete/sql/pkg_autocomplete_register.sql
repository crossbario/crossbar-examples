BEGIN
   --
   -- Crossbar.io needs execute rights on package
   --
   EXECUTE IMMEDIATE 'GRANT EXECUTE ON pkg_autocomplete TO ' || crossbar.REPOUSER;

   --
   -- Register package procedures as RPC endpoints with Crossbar.io
   --
   crossbar.remove_exports('pkg_autocomplete');
   crossbar.export('pkg_autocomplete', 'search', pkg_autocomplete.BASEURI || 'search');
   crossbar.export('pkg_autocomplete', 'count',  pkg_autocomplete.BASEURI || 'count');
   crossbar.export('pkg_autocomplete', 'get',    pkg_autocomplete.BASEURI || 'get');
END;
/
