from odoo import http
from odoo.http import request
from odoo.http import Response
import json

class PosStorefront (http.Controller):
    @http.route('/shop', type='http', auth='public', website=True)
    def shop_main(self, **kwargs):
        # 1. Offer Catalog: Seasonal bundles and products with active offers
        seasonal_bundles = request.env['pos.bundle'].search([('is_seasonal_offer', '=', True)])

        # 2. Bundles Archive: All bundles for browsing
        all_bundles = request.env['pos.bundle'].search([('is_seasonal_offer', '=', False)])

        # 3. Individual Products: Archive for single elements
        individual_products = request.env['pos.product'].search([])

        return request.render('shopping_cart.combined_store_view', {
            'seasonal': seasonal_bundles,
            'bundles': all_bundles,
            'products': individual_products,
        })
    ###def shop_index(self, **kwargs):
        # Fetch active products to populate the selection view
        products = request.env['pos.product'].search([('status_id.status_name', '=', 'ACTIVO')])
        return request.render('shopping_cart.storefront_layout', {
            'products': products,
        })




    @http.route('/shop/checkout', type='jsonrpc', auth='public', methods=['POST'], csrf=False)
    def checkout(self, cart_data):
        # Implementation of processPurchase logic
        sale_order = request.env['pos.sale'].action_process_checkout(cart_data)
        return {'ticket': sale_order.ticket_number, 'total': sale_order.total_amount}