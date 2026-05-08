from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PosOffer(models.Model):
    _name = 'pos.offer'
    _description = 'Promociones y Ofertas'

    name = fields.Char(string="Nombre de la Oferta", required=True)
    discount_type = fields.Selection([
        ('percentage', 'Porcentaje (%)'),
        ('fixed', 'Monto Fijo ($)')
    ], string="Tipo de Descuento", default='percentage', required=True)

    discount_value = fields.Float(string="Valor del Descuento", required=True)
    active = fields.Boolean(default=True)

    # Relationships for the dual-logic
    category_ids = fields.Many2many('pos.category', string="Categorías Aplicables")
    product_ids = fields.Many2many('pos.product', string="Productos Seleccionados")

    start_date = fields.Datetime(string="Fecha Inicio")
    end_date = fields.Datetime(string="Fecha Fin")

    @api.constrains('discount_value')
    def _check_value(self):
        for rec in self:
            if rec.discount_type == 'percentage' and (rec.discount_value <= 0 or rec.discount_value > 100):
                raise ValidationError("El porcentaje debe estar entre 1 y 100.")