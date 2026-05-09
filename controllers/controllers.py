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

    @http.route('/ofertas', type='http', auth="public", website=True)
    def page_offers(self, **kw):
        # Fetch only bundles marked as seasonal
        seasonal_bundles = request.env['pos.bundle'].sudo().search([('is_seasonal_offer', '=', True)])
        normal_offers = request.env['pos.offer'].sudo().search([('active', '=', True)])
        return request.render('shopping_cart.page_offers', {
            'seasonal': seasonal_bundles
            ,'normal_offers': normal_offers
        })

    @http.route('/paquetes', type='http', auth="public", website=True)
    def page_bundles(self, **kw):
        # Fetch standard bundles (or all of them, depending on your preference)
        all_bundles = request.env['pos.bundle'].sudo().search([])
        return request.render('shopping_cart.page_bundles', {
            'bundles': all_bundles
        })

    @http.route('/productos', type='http', auth="public", website=True)
    def page_products(self, **kw):
        # Fetch all products
        all_products = request.env['pos.product'].sudo().search([])
        return request.render('shopping_cart.page_products', {
            'products': all_products
        })

    @http.route('/shop/checkout', type='jsonrpc', auth='public', methods=['POST'], csrf=False)
    def checkout(self, cart_data):
        # Implementation of processPurchase logic
        sale_order = request.env['pos.sale'].action_process_checkout(cart_data)
        return {'ticket': sale_order.ticket_number, 'total': sale_order.total_amount}