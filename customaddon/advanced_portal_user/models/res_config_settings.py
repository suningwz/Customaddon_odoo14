from odoo import fields, models, api

# hours = ([('0', '12 AM'), ('1', '1 AM'), ('2', '2 AM'), ('3', '3 AM'), ('4', '4 AM'), ('5', '5 AM'), ('6', '6 AM'),
#           ('7', '7 AM'), ('8', '8 AM'), ('9', '9 AM'), ('10', '10 AM'), ('11', '11 AM'), ('12', '12 PM'),
#           ('13', '1 PM'), ('14', '2 PM'), ('15', '3 PM'), ('16', '4 PM'), ('17', '5 PM'), ('18', '6 PM'),
#           ('19', '7 PM'), ('20', '8 PM'), ('21', '9 PM'), ('22', '10 PM'), ('23', '11 PM')])
# minutes = ([('0', '00:00'), ('15', '15:00'),
#             ('30', '30:00'), ('45', '45:00')])


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    has_setting_portal = fields.Boolean("Setting Time Check Portal", store=True)
    portal_time_in = fields.Char(string='Time In', config_parameter='advanced_portal_user.time_in')
    portal_time_out = fields.Char(string='Time Out', config_parameter='advanced_portal_user.time_out')