CREATE OR REPLACE PACKAGE pkg_product
AS
   /**
    * Backend for Editform and Gridfilter demos.
    *
    * Copyright (c) 2013 Tavendo GmbH. Licensed under the Apache 2.0 license.
    */

   /**
    * RPC/Event URI prefix
    */
   BASEURI CONSTANT VARCHAR2(200) := 'http://crossbar.io/crossbar/demo/product#';

   /**
    * Get objects. This procedure can drive ExtJS grids and properly
    * does query pagination.
    */
   FUNCTION crud_read (p_params JSON) RETURN JSON_LIST;

   /**
    * Create a new object.
    */
   FUNCTION crud_create (p_obj JSON, p_sess CROSSBAR_SESSION) RETURN JSON;

   /**
    * Update existing object.
    */
   FUNCTION crud_update (p_obj JSON, p_sess CROSSBAR_SESSION) RETURN JSON;

   /**
    * Create or Update existing object.
    */
   FUNCTION crud_upsert (p_obj JSON, p_sess CROSSBAR_SESSION) RETURN JSON;

   /**
    * Delete an object given by ID.
    */
   FUNCTION crud_delete (p_id NUMBER, p_sess CROSSBAR_SESSION) RETURN JSON;

   /**
    * Get objects by filter.
    *
    * Example:
    *   session.call("http://crossbar.io/crossbar/demo/koform#filter", {name: {value: 'S', type: 'prefix'}}, 10).then(ab.log, ab.log);
    *
    *      NAME         TYPE
    *      --------------------------------------
    *      name         prefix, includes
    *      price        gte, lte
    */
   FUNCTION filter (p_filter JSON, p_limit NUMBER) RETURN JSON_LIST;
END;
/
