CREATE OR REPLACE PACKAGE BODY pkg_product
AS
   FUNCTION crud_read (p_params JSON) RETURN JSON_LIST
   AS
      l_res    SYS_REFCURSOR;
      l_start  PLS_INTEGER := 0;
      l_limit  PLS_INTEGER := 10;
   BEGIN

      -- extract query parameters
      --
      IF p_params.exist('start') AND p_params.get('start').is_number THEN
         l_start := p_params.get('start').get_number;
      END IF;
      IF p_params.exist('limit') AND p_params.get('limit').is_number THEN
         l_limit := p_params.get('limit').get_number;
      END IF;

      -- perform paginated query
      --
      OPEN l_res FOR
         SELECT id AS "id",
                name AS "name",
                order_number AS "orderNumber",
                weight AS "weight",
                item_size AS "size",
                in_stock AS "inStock",
                price AS "price"
           FROM (SELECT /*+ FIRST_ROWS */ ROWNUM rnum, a.*
                   FROM (SELECT * FROM product ORDER BY id ASC) a
                  WHERE ROWNUM <= l_start + l_limit)
          WHERE rnum >= l_start + 1;

      RETURN json_dyn.executeList(l_res);

   END crud_read;


   FUNCTION crud_create (p_obj JSON, p_sess CROSSBAR_SESSION) RETURN JSON
   IS
      l_id              product.id%TYPE;
      l_name            product.name%TYPE;
      l_order_number    product.order_number%TYPE;
      l_weight          product.weight%TYPE;
      l_item_size       product.item_size%TYPE;
      l_in_stock        product.in_stock%TYPE;
      l_price           product.price%TYPE;

      l_res             JSON := JSON();

      l_exclude         crossbar_sessionids := crossbar_sessionids();
      l_event_id        NUMBER;
   BEGIN

      -- read/sanitize requested object attributes
      --

      -- mandatory attribute "name" of type "string"
      --
      IF p_obj.exist('name') THEN
         IF p_obj.get('name').is_string THEN
            l_name := p_obj.get('name').get_string;
            IF l_name IS NULL THEN
               crossbar.raise(BASEURI || 'invalid_argument', 'Invalid value "' || l_name || '" for object property "name".');
            END IF;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid type "' || p_obj.get('name').get_type() || '" for object property "name". Expected a string.');
         END IF;
      ELSE
         crossbar.raise(BASEURI || 'invalid_argument', 'Missing object property "name".');
      END IF;

      -- mandatory attribute "orderNumber" of type "string"
      --
      IF p_obj.exist('orderNumber') THEN
         IF p_obj.get('orderNumber').is_string THEN
            l_order_number := p_obj.get('orderNumber').get_string;
            IF l_order_number IS NULL OR NOT REGEXP_LIKE(l_order_number, '^[A-Z]{3,3}-[0-9]{6,6}-[A-Z]{2,2}$') THEN
               crossbar.raise(BASEURI || 'invalid_argument', 'Invalid value "' || l_order_number || '" for object property "orderNumber". Must match the regular expression ^[A-Z]{3,3}-[0-9]{6,6}-[A-Z]{2,2}$.');
            END IF;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid type "' || p_obj.get('orderNumber').get_type() || '" for object property "orderNumber". Expected a string.');
         END IF;
      ELSE
         crossbar.raise(BASEURI || 'invalid_argument', 'Missing object property "orderNumber".');
      END IF;

      -- optional attribute "weight" of type "number"
      --
      IF p_obj.exist('weight') THEN
         IF p_obj.get('weight').is_number THEN
            l_weight := p_obj.get('weight').get_number;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid type "' || p_obj.get('weight').get_type() || '" for object property "weight". Expected a number.');
         END IF;
      END IF;

      -- optional attribute "size" of type "number"
      --
      IF p_obj.exist('size') THEN
         IF p_obj.get('size').is_number THEN
            l_item_size := p_obj.get('size').get_number;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid type "' || p_obj.get('size').get_type() || '" for object property "size". Expected a number.');
         END IF;
      END IF;

      -- optional attribute "inStock" of type "number"
      --
      IF p_obj.exist('inStock') THEN
         IF p_obj.get('inStock').is_number THEN
            l_in_stock := p_obj.get('inStock').get_number;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid type "' || p_obj.get('inStock').get_type() || '" for object property "inStock". Expected a number.');
         END IF;
      END IF;

      -- optional attribute "price" of type "number"
      --
      IF p_obj.exist('price') THEN
         IF p_obj.get('price').is_number THEN
            l_price := p_obj.get('price').get_number;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid type "' || p_obj.get('price').get_type() || '" for object property "price". Expected a number.');
         END IF;
      END IF;

      l_id := product_id.NEXTVAL;

      INSERT INTO product (id, name, order_number, weight, item_size, in_stock, price)
         VALUES (l_id, l_name, l_order_number, l_weight, l_item_size, l_in_stock, l_price);

      -- See comments on COMMIT in procedure crud_update().
      COMMIT;

      -- provide sanitized object attributes in RPC result and event
      --
      l_res.put('id', l_id);
      l_res.put('name', l_name);
      l_res.put('orderNumber', l_order_number);
      l_res.put('weight', l_weight);
      l_res.put('size', l_item_size);
      l_res.put('inStock', l_in_stock);
      l_res.put('price', l_price);

      l_exclude.extend();
      l_exclude(1) := p_sess.sessionid;
      l_event_id := crossbar.publish(BASEURI || 'oncreate', l_res, p_exclude => l_exclude);

         -- for debugging only
         l_res.put('_eventId', l_event_id);

      RETURN l_res;

   END crud_create;


   FUNCTION crud_update (p_obj JSON, p_sess CROSSBAR_SESSION) RETURN JSON
   IS
      l_current         product%ROWTYPE;

      l_id              product.id%TYPE;
      l_name            product.name%TYPE;
      l_order_number    product.order_number%TYPE;
      l_weight          product.weight%TYPE;
      l_item_size       product.item_size%TYPE;
      l_in_stock        product.in_stock%TYPE;
      l_price           product.price%TYPE;

      l_res             JSON := JSON();
      l_is_modified     BOOLEAN := FALSE;

      l_exclude         crossbar_sessionids := crossbar_sessionids();
      l_event_id        NUMBER;
   BEGIN
      -- get existing object
      --
      IF p_obj.exist('id') AND p_obj.get('id').is_number THEN
         l_id := p_obj.get('id').get_number;
      ELSE
         crossbar.raise(BASEURI || 'invalid_argument', 'Missing object ID property or wrong type.');
      END IF;

      BEGIN
         SELECT * INTO l_current FROM product WHERE id = l_id;
      EXCEPTION WHEN NO_DATA_FOUND THEN
         crossbar.raise(BASEURI || 'object_not_exists', 'Object to update does not exist.');
      END;

      -- sanitize request attribute values
      --
      IF p_obj.exist('name') AND p_obj.get('name').is_string THEN
         l_name := p_obj.get('name').get_string;
      ELSE
         l_name := l_current.name;
      END IF;

      IF p_obj.exist('orderNumber') AND p_obj.get('orderNumber').is_string THEN
         l_order_number := p_obj.get('orderNumber').get_string;
      ELSE
         l_order_number := l_current.order_number;
      END IF;

      IF p_obj.exist('weight') AND p_obj.get('weight').is_number THEN
         l_weight := p_obj.get('weight').get_number;
      ELSE
         l_weight := l_current.weight;
      END IF;

      IF p_obj.exist('size') AND p_obj.get('size').is_number THEN
         l_item_size := p_obj.get('size').get_number;
      ELSE
         l_item_size := l_current.item_size;
      END IF;

      IF p_obj.exist('inStock') AND p_obj.get('inStock').is_number THEN
         l_in_stock := p_obj.get('inStock').get_number;
      ELSE
         l_in_stock := l_current.in_stock;
      END IF;

      IF p_obj.exist('price') AND p_obj.get('price').is_number THEN
         l_price := p_obj.get('price').get_number;
      ELSE
         l_price := l_current.price;
      END IF;

      -- determine change set
      --
      IF l_name != l_current.name OR
         (l_name IS NULL     AND l_current.name IS NOT NULL) OR
         (l_name IS NOT NULL AND l_current.name IS NULL)
         THEN
         l_res.put('name', l_name);
         l_is_modified := TRUE;
      END IF;

      IF l_order_number != l_current.order_number OR
         (l_order_number IS NULL     AND l_current.order_number IS NOT NULL) OR
         (l_order_number IS NOT NULL AND l_current.order_number IS NULL)
      THEN
         l_res.put('orderNumber', l_order_number);
         l_is_modified := TRUE;
      END IF;

      IF l_weight != l_current.weight OR
         (l_weight IS NULL     AND l_current.weight IS NOT NULL) OR
         (l_weight IS NOT NULL AND l_current.weight IS NULL)
      THEN
         l_res.put('weight', l_weight);
         l_is_modified := TRUE;
      END IF;

      IF l_item_size != l_current.item_size OR
         (l_item_size IS NULL     AND l_current.item_size IS NOT NULL) OR
         (l_item_size IS NOT NULL AND l_current.item_size IS NULL)
      THEN
         l_res.put('size', l_item_size);
         l_is_modified := TRUE;
      END IF;

      IF l_in_stock != l_current.in_stock OR
         (l_in_stock IS NULL     AND l_current.in_stock IS NOT NULL) OR
         (l_in_stock IS NOT NULL AND l_current.in_stock IS NULL)
      THEN
         l_res.put('inStock', l_in_stock);
         l_is_modified := TRUE;
      END IF;

      IF l_price != l_current.price OR
         (l_price IS NULL     AND l_current.price IS NOT NULL) OR
         (l_price IS NOT NULL AND l_current.price IS NULL)
      THEN
         l_res.put('price', l_price);
         l_is_modified := TRUE;
      END IF;

      -- if changed, update and fire event ..
      --
      IF l_is_modified THEN

         UPDATE product
            SET
               name = l_name,
               order_number = l_order_number,
               weight = l_weight,
               item_size = l_item_size,
               in_stock = l_in_stock,
               price = l_price
               WHERE id = l_id;

         /*
          * Pushing an event from Crossbar.io happens in an autonomous
          * transaction. Nevertheless, we commit before pushing
          * the event, since the event might be received by
          * subscribers earlier than this procedure can return
          * and an subscriber might immediately issue a read
          * that would then receive the before data.
          */
         COMMIT;

         l_res.put('id', l_id);

         l_exclude.extend();
         l_exclude(1) := p_sess.sessionid;
         l_event_id := crossbar.publish(BASEURI || 'onupdate', l_res, p_exclude => l_exclude);

         -- for debugging only
         l_res.put('_eventId', l_event_id);

      END IF;

      RETURN l_res;

   END crud_update;


   FUNCTION crud_upsert (p_obj JSON, p_sess CROSSBAR_SESSION) RETURN JSON
   IS
   BEGIN
      IF p_obj.exist('id') THEN
         RETURN crud_update(p_obj, p_sess);
      ELSE
         RETURN crud_create(p_obj, p_sess);
      END IF;
   END crud_upsert;


   FUNCTION crud_delete (p_id NUMBER, p_sess crossbar_session) RETURN JSON
   IS
      l_current         product%ROWTYPE;
      l_res             JSON := JSON();
      l_exclude         crossbar_sessionids := crossbar_sessionids();
      l_event_id        NUMBER;
   BEGIN
      BEGIN
         SELECT * INTO l_current FROM product WHERE id = p_id;
      EXCEPTION WHEN NO_DATA_FOUND THEN
         crossbar.raise(BASEURI || 'object_not_exists', 'Object to delete does not exist.');
      END;

      DELETE FROM product WHERE id = p_id;

      -- See comments on COMMIT in procedure crud_update().
      COMMIT;

      l_res.put('id', p_id);

      l_exclude.extend();
      l_exclude(1) := p_sess.sessionid;
      l_event_id := crossbar.publish(BASEURI || 'ondelete', l_res, p_exclude => l_exclude);

      -- for debugging only
      l_res.put('_eventId', l_event_id);

      RETURN l_res;

   END crud_delete;


   FUNCTION filter (p_filter JSON, p_limit NUMBER) RETURN JSON_LIST
   AS
      l_res             SYS_REFCURSOR;
      l_limit           PLS_INTEGER := 10;

      l_name               VARCHAR2(200);
      l_name_type          VARCHAR2(30);

      l_order_number       VARCHAR2(200);
      l_order_number_type  VARCHAR2(30);

      l_price           NUMBER;
      l_price_type      VARCHAR2(30);
      l_price_sign      NUMBER;

      l_weight          NUMBER;
      l_weight_type     VARCHAR2(30);
      l_weight_sign     NUMBER;

      l_size            NUMBER;
      l_size_type       VARCHAR2(30);
      l_size_sign       NUMBER;

      l_instock         NUMBER;
      l_instock_type    VARCHAR2(30);
      l_instock_sign    NUMBER;
   BEGIN

      -- extract filter query parameters
      --

      --
      -- limit
      --
      IF p_limit IS NOT NULL AND p_limit > 0 THEN
         l_limit := p_limit;
      END IF;

      --
      -- name
      --
      IF p_filter.exist('name') THEN
         l_name := json_ext.get_string(p_filter, 'name.value');
         IF l_name IS NULL THEN
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid or missing filter value "name" filter');
         END IF;

         l_name_type := json_ext.get_string(p_filter, 'name.type');
         IF l_name_type = 'prefix' THEN
            l_name := l_name || '%';
         ELSIF l_name_type = 'includes' THEN
            l_name := '%' || l_name || '%';
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid filter type "' || l_name_type || '" for "name" filter');
         END IF;
      ELSE
         l_name := '%';
      END IF;

      --
      -- order number
      --
      IF p_filter.exist('orderNumber') THEN
         l_order_number := json_ext.get_string(p_filter, 'orderNumber.value');
         IF l_order_number IS NULL THEN
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid or missing filter value "orderNumber" filter');
         END IF;

         l_order_number_type := json_ext.get_string(p_filter, 'orderNumber.type');
         IF l_order_number_type = 'prefix' THEN
            l_order_number := l_order_number || '%';
         ELSIF l_order_number_type = 'includes' THEN
            l_order_number := '%' || l_order_number || '%';
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid filter type "' || l_order_number_type || '" for "orderNumber" filter');
         END IF;
      ELSE
         l_order_number := '%';
      END IF;

      --
      -- price
      --
      IF p_filter.exist('price') THEN
         l_price := json_ext.get_number(p_filter, 'price.value');
         IF l_price IS NULL THEN
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid or missing filter value "price" filter');
         END IF;

         l_price_type := json_ext.get_string(p_filter, 'price.type');
         IF l_price_type = 'gte' THEN
            l_price_sign := 1;
         ELSIF l_price_type = 'lte' THEN
            l_price_sign := -1;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid filter type "' || l_price_type || '" for "price" filter');
         END IF;
      ELSE
         l_price := -1e10;
         l_price_sign := 1;
      END IF;

      --
      -- weight
      --
      IF p_filter.exist('weight') THEN
         l_weight := json_ext.get_number(p_filter, 'weight.value');
         IF l_weight IS NULL THEN
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid or missing filter value "weight" filter');
         END IF;

         l_weight_type := json_ext.get_string(p_filter, 'weight.type');
         IF l_weight_type = 'gte' THEN
            l_weight_sign := 1;
         ELSIF l_weight_type = 'lte' THEN
            l_weight_sign := -1;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid filter type "' || l_weight_type || '" for "weight" filter');
         END IF;
      ELSE
         l_weight := -1e10;
         l_weight_sign := 1;
      END IF;

      --
      -- size
      --
      IF p_filter.exist('size') THEN
         l_size := json_ext.get_number(p_filter, 'size.value');
         IF l_size IS NULL THEN
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid or missing filter value "size" filter');
         END IF;

         l_size_type := json_ext.get_string(p_filter, 'size.type');
         IF l_size_type = 'gte' THEN
            l_size_sign := 1;
         ELSIF l_size_type = 'lte' THEN
            l_size_sign := -1;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid filter type "' || l_size_type || '" for "size" filter');
         END IF;
      ELSE
         l_size := -1e10;
         l_size_sign := 1;
      END IF;

      --
      -- instock
      --
      IF p_filter.exist('instock') THEN
         l_instock := json_ext.get_number(p_filter, 'instock.value');
         IF l_instock IS NULL THEN
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid or missing filter value "instock" filter');
         END IF;

         l_instock_type := json_ext.get_string(p_filter, 'instock.type');
         IF l_instock_type = 'gte' THEN
            l_instock_sign := 1;
         ELSIF l_instock_type = 'lte' THEN
            l_instock_sign := -1;
         ELSE
            crossbar.raise(BASEURI || 'invalid_argument', 'Invalid filter type "' || l_instock_type || '" for "instock" filter');
         END IF;
      ELSE
         l_instock := -1e10;
         l_instock_sign := 1;
      END IF;

      -- perform paginated query
      --
      OPEN l_res FOR
         SELECT * FROM (
            SELECT id AS "id",
                   name AS "name",
                   order_number AS "orderNumber",
                   weight AS "weight",
                   item_size AS "size",
                   in_stock AS "inStock",
                   price AS "price"
              FROM product WHERE
                  LOWER(name) LIKE LOWER(l_name) AND
                  LOWER(order_number) LIKE LOWER(l_order_number) AND
                  (l_instock_sign * in_stock) >= (l_instock_sign * l_instock) AND
                  (l_size_sign * item_size) >= (l_size_sign * l_size) AND
                  (l_weight_sign * weight) >= (l_weight_sign * l_weight) AND
                  (l_price_sign * price) >= (l_price_sign * l_price)
                  ORDER BY id ASC)
          WHERE rownum <= l_limit;

      RETURN json_dyn.executeList(l_res);

   END filter;

END;
/
