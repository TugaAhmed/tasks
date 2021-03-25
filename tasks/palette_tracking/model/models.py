from odoo import api, models, fields


class palette_tracking(models.Model):
    _name = 'pallet.tracking'


    picking_id = fields.Many2one('stock.picking' , string='Picking',required=True)
    partner_id = fields.Many2one('res.partner', string='Partner' )
    license_plate = fields.Char('License Plate')
    picking_partner_id = fields.Many2one('res.partner',string='Picking Partner',related='picking_id.partner_id')
    picking_date_done = fields.Datetime('Picking Date Done',related='picking_id.date_done')
    pallet_count_plus = fields.Integer('Pallet Count Plus')
    pallet_count_minus = fields.Integer('Pallet Count Minus')
    balance = fields.Integer(string='Balance' , compute="get_balance")


    @api.depends('pallet_count_plus','pallet_count_minus')
    def get_balance(self):
    	self.balance = 0.0
    	for record in self :
    		record.balance = record.pallet_count_plus - record.pallet_count_minus