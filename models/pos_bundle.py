from odoo import models, fields, api

class PosBundle(models.Model):
    _name = 'pos.bundle'
    _description = 'Paquetes de Productos (Bundles)'

    name = fields.Char(string="Nombre del Bundle", required=True)
    reference = fields.Char(string="Referencia/SKU del Bundle")
    description = fields.Text(string="Descripción")

    is_seasonal_offer = fields.Boolean(string="Mostrar en Catálogo de Ofertas (Navidad, etc.)", default=False)

    line_ids = fields.One2many('pos.bundle.line', 'bundle_id', string="Productos en el Bundle")
    total_normal_value = fields.Float(string="Valor Total Normal", compute='_compute_bundle_prices', store=True)
    bundle_price = fields.Float(string="Precio del Bundle", compute='_compute_bundle_prices', store=True,
                                readonly=False)

    @api.depends('line_ids.product_id', 'line_ids.quantity')
    def _compute_bundle_prices(self):
        for bundle in self:
            # Calculate what it would cost to buy everything individually
            normal_total = sum(line.product_id.base_price * line.quantity for line in bundle.line_ids)
            bundle.total_normal_value = normal_total

            # Apply 10% default if price hasn't been manually set yet
            if not bundle.bundle_price or bundle.bundle_price == 0:
                bundle.bundle_price = normal_total * 0.90


class PosBundleLine(models.Model):
    _name = 'pos.bundle.line'
    _description = 'Lineas de Bundle'

    bundle_id = fields.Many2one('pos.bundle', ondelete='cascade')
    product_id = fields.Many2one('pos.product', string="Producto", required=True)
    quantity = fields.Integer(string="Cantidad", default=1)
    product_price = fields.Float(related='product_id.base_price', readonly=True)