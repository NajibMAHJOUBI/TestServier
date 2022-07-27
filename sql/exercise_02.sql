
SELECT 
  t.client_id,
  SUM(CASE WHEN product_type = 'MEUBLE' THEN prod_price * prod_qty
           ELSE 0.0
      END
     ) AS ventes_meuble ,
  SUM(CASE WHEN product_type = 'DECO' THEN prod_price * prod_qty
           ELSE 0.0
      END
     ) AS ventes_deco  
  FROM Transaction AS t
  INNER JOIN Product_Nomenclature AS p
    ON t.prop_id = p.product_id
WHERE date BETWEEN '2020-01-01' AND '2020-12-31'    
GROUP BY t.client_id ; 