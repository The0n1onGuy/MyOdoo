from odoo import models, fields, api
import uuid


class PosCategory(models.Model):
    _name = 'pos.category'
    _description = 'Product Categories'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripción")