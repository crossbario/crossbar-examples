CREATE OR REPLACE PACKAGE BODY pkg_autocomplete
AS
   FUNCTION search (p_name NVARCHAR2, p_params JSON) RETURN JSON_LIST
   AS
      l_id        PLS_INTEGER := 0;   -- return results after or before this ID
      l_forward   BOOLEAN := TRUE;    -- search direction
      l_limit     PLS_INTEGER := 10;  -- search result limit
      l_res       SYS_REFCURSOR;      -- search result
   BEGIN

      -- extract query parameters
      --
      IF p_params.exist('after') AND p_params.exist('before') THEN
         crossbar.raise(BASEURI || 'invalid_argument', 'Conflicting search parameters specified - only one of "after" or "before" may be given');
      END IF;

      IF p_params.exist('after') THEN
         IF p_params.get('after').is_number THEN
            l_id := p_params.get('after').get_number;
            l_forward := TRUE;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Search parameter "after" is of wrong type ' || p_params.get('after').get_type() || ' - expected a number.');
         END IF;
      END IF;

      IF p_params.exist('before') THEN
         IF p_params.get('before').is_number THEN
            l_id := p_params.get('before').get_number;
            l_forward := FALSE;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Search parameter "before" is of wrong type ' || p_params.get('before').get_type() || ' - expected a number.');
         END IF;
      END IF;

      IF p_params.exist('limit') THEN
         IF p_params.get('limit').is_number THEN
            l_limit := p_params.get('limit').get_number;
            IF l_limit < 1 THEN
               crossbar.raise(BASEURI || 'invalid_argument', 'Search parameter "limit" must be >= 1.');
            END IF;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Search parameter "limit" is of wrong type ' || p_params.get('limit').get_type() || ' - expected a number.');
         END IF;
      END IF;

      --
      -- perform paginated prefix matching query
      --
      IF l_forward THEN

         -- forward search given reference person l_id
         --
         OPEN l_res FOR
            SELECT id AS "id", sname AS "sname", name AS "name"
              FROM (SELECT id, sname, name, uri
                      FROM person
                     WHERE sname LIKE LOWER(p_name || '%') AND id > l_id ORDER BY sname, uri)
             WHERE ROWNUM <= l_limit;

      ELSE

         -- backward search given reference person l_id
         --
         OPEN l_res FOR
            SELECT id AS "id", sname AS "sname", name AS "name"
              FROM (SELECT id, sname, name, uri
                      FROM person
                     WHERE sname LIKE LOWER(p_name || '%') AND id < l_id ORDER BY sname DESC, uri DESC)
             WHERE ROWNUM <= l_limit
               ORDER BY sname, uri;

      END IF;

      RETURN json_dyn.executeList(l_res);

   END search;


   FUNCTION count (p_name NVARCHAR2) RETURN NUMBER
   AS
      l_count  NUMBER;
   BEGIN

      IF p_name IS NULL THEN
         --
         -- return total number of persons in database
         --
         SELECT COUNT(*) INTO l_count FROM person;
      ELSE
         --
         -- return number of persons with names having given search prefix
         --
         SELECT COUNT(*) INTO l_count FROM person
            WHERE sname LIKE LOWER(p_name || '%');
      END IF;

      RETURN l_count;

   END count;


   FUNCTION get (p_id NUMBER) RETURN JSON
   IS
      l_person    person%ROWTYPE;
      l_res       JSON;
   BEGIN

      BEGIN
         --
         -- get detail information for person
         --
         SELECT * INTO l_person FROM person WHERE id = p_id;
      EXCEPTION WHEN NO_DATA_FOUND THEN
         crossbar.raise(BASEURI || 'object_not_exists', 'Person with given ID does not exist.');
      END;

      l_res := new JSON();
      l_res.put('id', l_person.id);
      l_res.put('uri', l_person.uri);
      l_res.put('name', l_person.name);
      l_res.put('surname', l_person.surname);
      l_res.put('givenname', l_person.givenname);
      l_res.put('birthdate', l_person.birthdate);
      l_res.put('birthplace', l_person.birthplace);
      l_res.put('deathdate', l_person.deathdate);
      l_res.put('deathplace', l_person.deathplace);
      l_res.put('descr', l_person.descr);

      RETURN l_res;
   END get;

END;
/
