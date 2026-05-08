from odoo import models, fields, api
import uuid

class Gen_Status(models.Model):
    _name = 'nexus.status'
    _description = 'Core Status Model'

    name = fields.Char(string="Nombre", required=True)
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), readonly=True)
    status_name = fields.Selection([
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('PENDIENTE', 'Pendiente')
    ], string="Estado", default='PENDIENTE')
