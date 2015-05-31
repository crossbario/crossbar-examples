CREATE OR REPLACE PACKAGE pkg_autocomplete
AS
   /**
    * Backend for Autocomplete demo.
    *
    * Copyright (c) 2013 Tavendo GmbH. Licensed under the Apache 2.0 license.
    */

   /**
    * RPC/Event URI prefix
    */
   BASEURI CONSTANT VARCHAR2(200) := 'http://crossbar.io/crossbar/demo/autocomplete#';

   /**
    * Search for persons matching given name.
    *
    * Examples:
    *
    *   session.call("http://crossbar.io/crossbar/demo/autocomplete#search", "Gauss", {}).then(ab.log, ab.log);
    *   session.call("http://crossbar.io/crossbar/demo/autocomplete#search", "Gau", {after: 309461, limit: 5}).then(ab.log, ab.log);
    *   session.call("http://crossbar.io/crossbar/demo/autocomplete#search", "Gau", {before: 309461, limit: 5}).then(ab.log, ab.log);
    */
   FUNCTION search (p_name NVARCHAR2, p_params JSON) RETURN JSON_LIST;

   /**
    * Count number of persons matching given name, or return total number of records when given empty string.
    *
    * Examples:
    *
    *   session.call("http://crossbar.io/crossbar/demo/autocomplete#count", "Gauss").then(ab.log, ab.log);
    *   session.call("http://crossbar.io/crossbar/demo/autocomplete#count", "").then(ab.log, ab.log);
    */
   FUNCTION count (p_name NVARCHAR2) RETURN NUMBER;


   /**
    * Get person details for person with given ID.
    *
    * Examples:
    *
    *   session.call("http://crossbar.io/crossbar/demo/autocomplete#get", 309787).then(ab.log, ab.log);
    */
   FUNCTION get (p_id NUMBER) RETURN JSON;

END;
/
