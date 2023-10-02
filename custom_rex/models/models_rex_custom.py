from odoo import api, Command, fields, models, _

class SaleOrderCustom(models.Model):
    _inherit = 'sale.order'

    stc_quantity = fields.Float(string='STC qty')
    stc_value = fields.Float(string='STC Value',store=True)
    veec_quantity = fields.Float(string='VEEC qty')
    veec_value = fields.Float(string='VEEC Value',store=True)
    stc_rebate = fields.Monetary(string="STC Rebate")
    veec_rebate = fields.Monetary(string="VEEC Rebate")
    solar_victoria_rebate = fields.Monetary(string="Solar Victoria Rebate")

    
    
    

    @api.onchange('stc_quantity','veec_quantity')
    def update_stc_quantity(self):
        # Get the value of stc_quantity from res.config.settings
        config_parameter = self.env['ir.config_parameter'].sudo()
        stc_value = config_parameter.get_param('custom_rex.stc_value', default=0.0)
        veec_value = config_parameter.get_param('custom_rex.veec_value', default=0.0)
        


        # Update the stc_quantity field in sale.order
        print(f"data in setting stc field --{stc_value}")
        self.stc_value = stc_value
        self.veec_value = veec_value


    @api.onchange('stc_quantity','veec_quantity')
    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed',)
    def _compute_tax_totals(self):
        qty = 0
        sum_ = 0
        mult_stc_veec = 0
        solar_victoria_rebate = 0
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            order.tax_totals = self.env['account.tax']._prepare_tax_totals(
                [x._convert_to_tax_base_line_dict() for x in order_lines],
                order.currency_id,
            )
            tota_dictionary = order.tax_totals['amount_total']
            print(f"-----------tota_dictionary--{tota_dictionary}")
            self.veec_rebate = float(self.veec_quantity)*float(self.stc_value)
            self.stc_rebate = float(self.stc_quantity)*float(self.veec_value)
            sum_ = float(float(self.veec_rebate)+float(self.stc_rebate)+float(self.solar_victoria_rebate))
            mult_stc_veec = float(tota_dictionary) - (float(sum_))
            mult_stc_veec = round(mult_stc_veec,2)
            formatted_value = f"{mult_stc_veec:.2f}"
            print(f"-----------tota_dictionary  rounded--{mult_stc_veec}")
            order.tax_totals.update({"formatted_amount_total":formatted_value})
            


class SaleOrderLineCustom(models.Model):
    _inherit = 'sale.order.line'



    clickable_link = fields.Html(string="Link", compute='_compute_clickable_link')   
    
    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True, ondelete='restrict', check_company=True, index='btree_not_null',
        domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]") 

    def _compute_clickable_link(self):
        for line in self:
            if line.product_template_id.website_url:
                product_link = line.product_template_id.website_url
                line.clickable_link = f"<a href='{product_link}' target='_blank'>Click here to view product</a>"
            else:
                line.clickable_link = ""


    product_url = fields.Char(string='Product URL',)

    


class SaleConfigSettingsCustom(models.TransientModel):
    _inherit = "res.config.settings"

    stc_value = fields.Float(string='STC Value', )
    veec_value = fields.Float(string='VEEC Value')


   
    def set_values(self):
        super(SaleConfigSettingsCustom, self).set_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        config_parameter.set_param('custom_rex.stc_value', self.stc_value)
        config_parameter.set_param('custom_rex.veec_value', self.veec_value)

    def get_values(self):
        res = super(SaleConfigSettingsCustom, self).get_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        stc_value = config_parameter.get_param('custom_rex.stc_value', default=0.0)
        veec_value = config_parameter.get_param('custom_rex.veec_value', default=0.0)
        res.update(
            stc_value=stc_value,
            veec_value=veec_value
        )
        print(f"data in setting stc field --{res}")
        return res
