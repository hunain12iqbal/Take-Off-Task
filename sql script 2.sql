SELECT
    pt.name AS article,
    pp.default_code,
    sw.name AS warehouse_name,
    sl.complete_name AS location_full_name,
    sq.quantity AS on_hand_quantity,
    (sq.quantity - sq.reserved_quantity) AS available_quantity
FROM
    stock_quant sq
JOIN
    product_product pp ON sq.product_id = pp.id
JOIN
    product_template pt ON pp.product_tmpl_id = pt.id
JOIN
    stock_location sl ON sq.location_id = sl.id
JOIN
    stock_warehouse sw ON sl.id = sw.lot_stock_id
WHERE
    (sq.quantity - sq.reserved_quantity) > 0  
AND
    sl.usage = 'internal';  
