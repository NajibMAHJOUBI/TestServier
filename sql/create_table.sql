
/*
  Création de la table Transaction
*/

CREATE TABLE IF NOT EXISTS Transaction (
   date DATE NOT NULL,
   order_id INT NOT NULL,
   client_id INT NOT NULL,
   prop_id INT NOT NULL,
   prod_price FLOAT NOT NULL, 
   prod_qty INT NOT NULL
);


INSERT INTO Transaction (date, order_id, client_id, prop_id, prod_price, prod_qty)
       VALUES ('01-01-2020', 1234, 999, 490756, 50, 1),
              ('01-01-2020', 1234, 999, 389728, 3.56, 4),
              ('01-01-2020', 3456, 845, 490756, 50, 2),
              ('01-01-2020', 3456, 845, 549380, 300, 1),
              ('01-01-2020', 3456, 845, 293718, 10, 6) ;  
              
/*
  Création de la table Product_Nomenclature
*/

CREATE TABLE IF NOT EXISTS Product_Nomenclature 
 (product_id INT NOT NULL, 
  product_type CHARACTER VARYING(6), 
  product_name CHARACTER VARYING(15)) ;
  
  
INSERT INTO Product_Nomenclature (product_id, product_type, product_name)
       VALUES (490756, 'MEUBLE', 'Chaise'),
              (389728, 'DECO', 'Boule de Noël'),
              (549380, 'MEUBLE', 'Canapé'),
              (549380, 'DECO', 'Mug') ; 
