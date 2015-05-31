CREATE SEQUENCE product_id
   START WITH 100
   INCREMENT BY 1
/

CREATE TABLE product
(
   id             NUMBER(10,0)      NOT NULL,
   name           VARCHAR2(200)     NOT NULL,
   order_number   VARCHAR2(200)     NOT NULL,
   weight         NUMBER,
   item_size      NUMBER,
   in_stock       NUMBER,
   price          NUMBER,
   PRIMARY KEY (id)
)
/

BEGIN
   INSERT INTO product (id, name, order_number, weight, item_size, in_stock, price)
   SELECT 1, 'Laptop', 'ELD-037485-LC', 3, 5, 45, 499 FROM dual UNION ALL
   SELECT 2, 'Notebook', 'ELD-078943-NC', 2, 4, 120, 699 FROM dual UNION ALL
   SELECT 3, 'Tablet', 'ELD-034812-TB', 0.7, 3, 88, 399 FROM dual UNION ALL
   SELECT 4, 'Desktop', 'ELD-057684-DC', 10, 8, 67, 599 FROM dual UNION ALL
   SELECT 5, 'Smartphone', 'ELD-089958-SP', 0.15, 1, 134, 399 FROM dual UNION ALL
   SELECT 6, 'Featurephone', 'ELD-089743-FP', 0.1, 1, 578, 59 FROM dual UNION ALL
   SELECT 7, 'Printer', 'ELD-045362-PR', 5, 6, 300, 199 FROM dual UNION ALL
   SELECT 8, 'Scanner', 'ELD-056783-SC', 2, 4, 23, 99 FROM dual UNION ALL
   SELECT 9, 'NAS', 'ELD-048938-NS', 6, 6, 40, 599 FROM dual UNION ALL
   SELECT 10, 'Server', 'ELD-012457-SV', 20, 10, 1, 1599 FROM dual UNION ALL
   SELECT 11, 'Mainframe', 'ELD-000012-MF', 1000, 100, 0, 100000 FROM dual UNION ALL
   SELECT 12, 'SSD - 64GB', 'STP-067884-SS', 0.1, 1, 23, 99 FROM dual UNION ALL
   SELECT 13, 'SSD - 128GB', 'STP-067886-SS', 0.1, 1, 456, 199 FROM dual UNION ALL
   SELECT 14, 'SSD - 256GB', 'STP-067888-SS', 0.1, 1, 12, 299 FROM dual UNION ALL
   SELECT 15, 'HDD - 500GB', 'STP-045689-HD', .5, 1, 68, 50 FROM dual UNION ALL
   SELECT 16, 'HDD - 1TB', 'STP-045691-HD', 0.5, 1, 45, 99 FROM dual UNION ALL
   SELECT 17, 'HDD - 2TB', 'STP-045693-HD', 0.5, 1, 78, 150 FROM dual UNION ALL
   SELECT 18, 'HDD - 3TB', 'STP-045695-HD', 0.6, 1, 4, 200 FROM dual;
   COMMIT;
END;   
/
