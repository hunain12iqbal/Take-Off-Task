UPDATE stock_quant
SET quantity = quantity + 1 
WHERE product_id = (SELECT id FROM product_product WHERE id = 44)  -- Replace with your product's internal reference
AND location_id = (SELECT id FROM stock_location WHERE name = 'Stock');  -- Assuming 'Stock' location
