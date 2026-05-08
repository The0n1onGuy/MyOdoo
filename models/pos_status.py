from odoo import models, fields, api
import uuid

class pos_status(models.Model):
    _name = 'pos.status'
    _description = 'Core Status Model'

    name = fields.Char(string="Nombre", required=True)
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), readonly=True)
    status_name = fields.Selection([
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('PENDIENTE', 'Pendiente')
    ], string="Estado", default='PENDIENTE')
