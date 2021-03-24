from odoo import api, models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    auth_id = fields.Char('Authentication Id' , readonly=False , related="company_id.auth_id" )
    tokent_id = fields.Char('Token Id' , readonly=False , related="company_id.tokent_id")





class ResCompany(models.Model):
    _inherit = 'res.company'

    auth_id = fields.Char('Authentication Id'  , readonly=False)
    tokent_id = fields.Char('Token Id' , readonly=False)