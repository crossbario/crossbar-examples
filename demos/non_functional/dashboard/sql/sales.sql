CREATE SEQUENCE sales_id
/

CREATE TABLE sales
(
   id         INTEGER        NOT NULL,
   trans_dt   TIMESTAMP      NOT NULL,
   product    VARCHAR2(100)  NOT NULL,
   region     VARCHAR2(100)  NOT NULL,
   units      INTEGER        NOT NULL,
   price      NUMBER(10,3)   NOT NULL,
   CONSTRAINT pk_sales
      PRIMARY KEY (trans_dt, id),
   CONSTRAINT ck_region
      CHECK (region IN ('North', 'South', 'East', 'West')),
   CONSTRAINT ck_product
      CHECK (product IN ('Product A', 'Product B', 'Product C'))
)
ORGANIZATION INDEX
/


CREATE OR REPLACE TRIGGER trg_sales_onsale
   AFTER INSERT ON sales
      FOR EACH ROW
DECLARE
   l_event JSON := JSON();
BEGIN
   l_event.put('id', :new.id);
   l_event.put('trans_dt', TO_CHAR(:new.trans_dt, 'YYYY-MM-DD"T"HH24:MI:SS"Z"'));
   l_event.put('product', :new.product);
   l_event.put('region', :new.region);
   l_event.put('units', :new.units);
   l_event.put('price', :new.price);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#onSale', l_event);
END;
/


CREATE OR REPLACE TRIGGER trg_sales_agg_total
   AFTER INSERT ON sales
DECLARE
   l_units_total    JSON_LIST := JSON_LIST();
   l_asp_total      JSON_LIST := JSON_LIST();
   l_revenue_total  JSON_LIST := JSON_LIST();

   l_current_u TIMESTAMP := SYSTIMESTAMP AT TIME ZONE 'utc';
   l_current_l TIMESTAMP := l_current_u - INTERVAL '60' SECOND;
   l_last_u    TIMESTAMP := l_current_l;
   l_last_l    TIMESTAMP := l_last_u    - INTERVAL '60' SECOND;
BEGIN
   FOR r IN (
      SELECT
         COALESCE(c.dim, l.dim) dim,
         COALESCE(c.units, 0) c_units,
         COALESCE(l.units, 0) l_units,
         COALESCE(c.revenue, 0) c_revenue,
         COALESCE(l.revenue, 0) l_revenue,
         COALESCE(c.asp, 0) c_asp,
         COALESCE(l.asp, 0) l_asp FROM
      (
         -- total sales in current period
         SELECT
            'total' dim,
            SUM(units) units,
            ROUND(SUM(units * price), 0) revenue,
            ROUND(SUM(units * price) / SUM(units), 2) asp
         FROM
            sales
         WHERE
            trans_dt <= l_current_u AND trans_dt > l_current_l
     ) c FULL OUTER JOIN
     (
         -- total sales in previous period
         SELECT
            'total' dim,
            SUM(units) units,
            ROUND(SUM(units * price), 0) revenue,
            ROUND(SUM(units * price) / SUM(units), 2) asp
         FROM
            sales
         WHERE
            trans_dt <= l_last_u AND trans_dt > l_last_l
     ) l ON c.dim = l.dim
   )
   LOOP
      -- prepare "Total Units" event
      l_units_total.append(r.c_units);
      l_units_total.append(r.l_units);

      -- prepare "Total ASP" event
      l_asp_total.append(r.c_asp);
      l_asp_total.append(r.l_asp);

      -- prepare "Total Revenue" event
      l_revenue_total.append(r.c_revenue);
      l_revenue_total.append(r.l_revenue);
   END LOOP;

   -- publish prepared events
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#totalUnits', l_units_total);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#totalAsp', l_asp_total);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#totalRevenue', l_revenue_total);
END;
/


CREATE OR REPLACE TRIGGER trg_sales_agg_by_product
   AFTER INSERT ON sales
DECLARE
   l_units_by_product   JSON := JSON();
   l_asp_by_product     JSON := JSON();
   l_revenue_by_product JSON := JSON();
   l_vals               JSON_LIST;

   l_current_u TIMESTAMP := SYSTIMESTAMP AT TIME ZONE 'utc';
   l_current_l TIMESTAMP := l_current_u - INTERVAL '60' SECOND;
   l_last_u    TIMESTAMP := l_current_l;
   l_last_l    TIMESTAMP := l_last_u    - INTERVAL '60' SECOND;
BEGIN
   FOR r IN (
      SELECT
         COALESCE(c.product, l.product) product,
         COALESCE(c.units, 0) c_units,
         COALESCE(l.units, 0) l_units,
         COALESCE(c.revenue, 0) c_revenue,
         COALESCE(l.revenue, 0) l_revenue,
         COALESCE(c.asp, 0) c_asp,
         COALESCE(l.asp, 0) l_asp FROM
      (
         -- sales by product in current period
         SELECT
            product,
            SUM(units) units,
            ROUND(SUM(units * price), 0) revenue,
            ROUND(SUM(units * price) / SUM(units), 2) asp
         FROM
            sales
         WHERE
            trans_dt <= l_current_u AND trans_dt > l_current_l
         GROUP BY
            product
     ) c FULL OUTER JOIN
     (
         -- sales by product in previous period
         SELECT
            product,
            SUM(units) units,
            ROUND(SUM(units * price), 0) revenue,
            ROUND(SUM(units * price) / SUM(units), 2) asp
         FROM
            sales
         WHERE
            trans_dt <= l_last_u AND trans_dt > l_last_l
         GROUP BY
            product
     ) l ON c.product = l.product
   )
   LOOP
      -- prepare "Units by Product" event
      l_vals := JSON_LIST();
      l_vals.append(r.c_units);
      l_vals.append(r.l_units);
      l_units_by_product.put(r.product, l_vals);

      -- prepare "ASP by Product" event
      l_vals := JSON_LIST();
      l_vals.append(r.c_asp);
      l_vals.append(r.l_asp);
      l_asp_by_product.put(r.product, l_vals);

      -- prepare "Revenue by Product" event
      l_vals := JSON_LIST();
      l_vals.append(r.c_revenue);
      l_vals.append(r.l_revenue);
      l_revenue_by_product.put(r.product, l_vals);
   END LOOP;

   -- publish prepared events
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#unitsByProduct', l_units_by_product);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#aspByProduct', l_asp_by_product);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#revenueByProduct', l_revenue_by_product);
END;
/


CREATE OR REPLACE TRIGGER trg_sales_agg_by_region
   AFTER INSERT ON sales
DECLARE
   l_units_by_region    JSON := JSON();
   l_asp_by_region      JSON := JSON();
   l_revenue_by_region  JSON := JSON();
   l_vals               JSON_LIST;

   l_current_u TIMESTAMP := SYSTIMESTAMP AT TIME ZONE 'utc';
   l_current_l TIMESTAMP := l_current_u - INTERVAL '60' SECOND;
   l_last_u    TIMESTAMP := l_current_l;
   l_last_l    TIMESTAMP := l_last_u    - INTERVAL '60' SECOND;
BEGIN
   FOR r IN (
      SELECT
         COALESCE(c.region, l.region) region,
         COALESCE(c.units, 0) c_units,
         COALESCE(l.units, 0) l_units,
         COALESCE(c.revenue, 0) c_revenue,
         COALESCE(l.revenue, 0) l_revenue,
         COALESCE(c.asp, 0) c_asp,
         COALESCE(l.asp, 0) l_asp FROM
      (
         -- sales by region in current period
         SELECT
            region,
            SUM(units) units,
            ROUND(SUM(units * price), 0) revenue,
            ROUND(SUM(units * price) / SUM(units), 2) asp
         FROM
            sales
         WHERE
            trans_dt <= l_current_u AND trans_dt > l_current_l
         GROUP BY
            region
     ) c FULL OUTER JOIN
     (
         -- sales by region in previous period
         SELECT
            region,
            SUM(units) units,
            ROUND(SUM(units * price), 0) revenue,
            ROUND(SUM(units * price) / SUM(units), 2) asp
         FROM
            sales
         WHERE
            trans_dt <= l_last_u AND trans_dt > l_last_l
         GROUP BY
            region
     ) l ON c.region = l.region
   )
   LOOP
      -- prepare "Units by region" event
      l_vals := JSON_LIST();
      l_vals.append(r.c_units);
      l_vals.append(r.l_units);
      l_units_by_region.put(r.region, l_vals);

      -- prepare "ASP by region" event
      l_vals := JSON_LIST();
      l_vals.append(r.c_asp);
      l_vals.append(r.l_asp);
      l_asp_by_region.put(r.region, l_vals);

      -- prepare "Revenue by region" event
      l_vals := JSON_LIST();
      l_vals.append(r.c_revenue);
      l_vals.append(r.l_revenue);
      l_revenue_by_region.put(r.region, l_vals);
   END LOOP;

   -- publish prepared events
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#unitsByRegion', l_units_by_region);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#aspByRegion', l_asp_by_region);
   crossbar.publish('http://crossbar.io/crossbar/demo/dashboard#revenueByRegion', l_revenue_by_region);
END;
/
