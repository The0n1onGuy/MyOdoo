from odoo import models, fields, api
import uuid

class PosProduct(models.Model):
    _name = 'pos.product'
    _description = 'POS Products'

    name = fields.Char(string="Nombre", required=True)
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), readonly=True)
    sku = fields.Char(string="SKU", required=True)
    base_price = fields.Float(string="Precio Base", digits=(10, 2), required=True)

    category_id = fields.Many2one('pos.category', string="Categoría", required=True)
    status_id = fields.Many2one('pos.status', string="Estado", required=True)

    discounted_price = fields.Float(
        string="Precio con Oferta",
        compute='_compute_discounted_price'
    )

    # Inverse relationship to see inventory from product
    inventory_id = fields.One2many('pos.inventory', 'product_id', string="Inventario")

    @api.depends('base_price')
    def _compute_discounted_price(self):
        now = fields.Datetime.now()
        for product in self:
            # Find active offers for this product or its category
            offer = self.env['pos.offer'].search([
                ('active', '=', True),
                '|',
                ('product_ids', 'in', product.id),
                ('category_ids', 'in', product.category_id.id),
                '|', ('start_date', '=', False), ('start_date', '<=', now),
                '|', ('end_date', '=', False), ('end_date', '>=', now)
            ], limit=1, order='discount_value desc')  # Take the best offer

            if offer:
                if offer.discount_type == 'percentage':
                    product.discounted_price = product.base_price * (1 - (offer.discount_value / 100))
                else:
                    product.discounted_price = product.base_price - offer.discount_value
            else:
                product.discounted_price = product.base_price


