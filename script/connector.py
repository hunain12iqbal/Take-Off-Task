import os
import xmlrpc.client
from dotenv import load_dotenv


load_dotenv()

ODOO_HOST = os.getenv("ODOO_HOST")
ODOO_PORT = os.getenv("ODOO_PORT")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USER = os.getenv("ODOO_USER")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

common = xmlrpc.client.ServerProxy(f"{ODOO_HOST}:{ODOO_PORT}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{ODOO_HOST}:{ODOO_PORT}/xmlrpc/2/object")


def create_and_confirm_so():
    # Retrieve partner and product by their XML IDs
    partner_id = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'res.partner', 'search', [[('id', '=', models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'ir.model.data', 'xmlid_to_res_id', ['take_off_custom.take_off_custom_partner']))]])
    product_id = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.template', 'search', [[('id', '=', models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'ir.model.data', 'xmlid_to_res_id', ['take_off_custom.take_off_custom_product_template']))]])
    if not partner_id or not product_id:
        print("Partner or Product not found!")
        return
    
    partner_id = partner_id[0]
    product_id = product_id[0]
    product_data = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.template', 'read', [product_id])
    
   
    so_id = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'create', [{
        'partner_id': partner_id,
        'order_line': [(0, 0, {
            'product_id': product_data[0].get('id'),
            'product_uom_qty': 1,  # Set quantity
            'price_unit': product_data[0].get('list_price'),  # Set unit price
        })]
    }])

    models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'action_confirm', [so_id])

    so = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'read', [so_id], {'fields': ['name', 'order_line']})
    so_name = so[0]['name']

    so_lines = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order.line', 'read', so[0]['order_line'], {'fields': ['product_id', 'price_unit', 'product_uom_qty']})
    
    print(f"Sale Order: {so_name}")
    print("Order Lines:")
    for line in so_lines:
        product_name = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.product', 'read', [line['product_id'][0]], {'fields': ['name']})[0]['name']
        print(f"  Product: {product_name}, Price: {line['price_unit']}, Quantity: {line['product_uom_qty']}")

    pickings = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.picking', 'search_read', [[('origin', '=', so_name)]], {'fields': ['name', 'state']})
    print("Transfers:")
    for picking in pickings:
        print(f"  Transfer: {picking['name']}, State: {picking['state']}")

if __name__ == "__main__":
    create_and_confirm_so()


