from odoo import models, fields, api



class PosSale(models.Model):
    _name = 'pos.sale'
    _description = 'POS Sales Orders'


    ticket_number = fields.Char(string="Número de Ticket", required=True, copy=False)
    uuid = fields.Char(string="UUID", default=lambda self: str(uuid.uuid4()), readonly=True)
    sale_date = fields.Datetime(string="Fecha de Venta", default=fields.Datetime.now)
    payment_method = fields.Selection([
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia')
    ], string="Método de Pago")

    status_id = fields.Many2one('pos.status', string="Estado")
    detail_ids = fields.One2many('pos.sale.detail', 'sale_id', string="Detalles de Venta")

    # Equivalent to a Service/Repository aggregate:
    total_amount = fields.Float(string="Total", compute='_compute_total_amount', store=True)

    @api.depends('detail_ids.subtotal')
    def _compute_total_amount(self):
        for sale in self:
            sale.total_amount = sum(line.subtotal for line in sale.detail_ids)

    def action_process_checkout(self, cart_items):
        total_amount = 0
        # 1. Generate Ticket
        sale = self.create({
            'ticket_number': 'T-%s' % self.env['ir.sequence'].next_by_code('pos.sale.ticket'),
            'payment_method': 'TARJETA'  # Default for web
        })

        for item in cart_items:
            product = self.env['pos.product'].browse(item['productId'])
            inventory = self.env['pos.inventory'].search([('product_id', '=', product.id)], limit=1)

            # 2. FINAL INVENTORY CHECK (The "Bounce" logic)
            if inventory.current_stock < item['quantity']:
                raise UserError("Stock insuficiente para %s" % product.name)

            # 3. Calculate financial data & Create Sale Detail
            subtotal = product.base_price * item['quantity']
            total_amount += subtotal

            self.env['pos.sale.detail'].create({
                'sale_id': sale.id,
                'product_id': product.id,
                'quantity': item['quantity'],
                'sold_price': product.base_price,
                'subtotal': subtotal
            })

            # 4. Update Inventory and Create Audit Movement
            inventory.current_stock -= item['quantity']
            self.env['pos.inventory.movement'].create({
                'product_id': product.id,
                'movement_type': 'SALE',
                'quantity': -item['quantity'],
                'reason': "Ticket: %s" % sale.ticket_number
            })

        sale.write({'total_amount': total_amount})
        return sale



class PosSaleDetail(models.Model):
    _name = 'pos.sale.detail'
    _description = 'POS Sale Details'

    sale_id = fields.Many2one('pos.sale', string="Venta", ondelete='cascade')
    product_id = fields.Many2one('pos.product', string="Producto", required=True)
    quantity = fields.Integer(string="Cantidad", required=True, default=1)
    sold_price = fields.Float(string="Precio de Venta", digits=(10, 2), required=True)

    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'sold_price')
    def _compute_subtotal(self):
        for detail in self:
            detail.subtotal = detail.quantity * detail.sold_price