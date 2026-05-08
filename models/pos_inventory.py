from odoo import models, fields, api
import uuid

class PosInventory(models.Model):
    _name = 'pos.inventory'
    _description = 'POS Inventory'

    product_id = fields.Many2one('pos.product', string="Producto", required=True, ondelete='cascade')
    current_stock = fields.Integer(string="Stock Actual", default=0)
    min_stock = fields.Integer(string="Stock Mínimo", default=5)
    last_restock_date = fields.Datetime(string="Último Reabastecimiento")

class PosInventoryMovement(models.Model):
    _name = 'pos.inventory.movement'
    _description = 'Inventory Movements'

    product_id = fields.Many2one('pos.product', string="Producto", required=True)
    movement_type = fields.Selection([
        ('SALE', 'Venta'),
        ('RESTOCK', 'Reabastecimiento'),
        ('ADJUSTMENT', 'Ajuste')
    ], string="Tipo de Movimiento", required=True)
    quantity = fields.Integer(string="Cantidad", required=True)
    reason = fields.Text(string="Razón/Nota")
    movement_date = fields.Datetime(string="Fecha de Movimiento", default=fields.Datetime.now)