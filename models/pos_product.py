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

    # Inverse relationship to see inventory from product
    inventory_id = fields.One2many('pos.inventory', 'product_id', string="Inventario")


