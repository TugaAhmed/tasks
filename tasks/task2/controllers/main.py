from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
import json
import requests

class WebsiteSale2(WebsiteSale):

    def get_zipcode(self,auth_id=False , auth_token = False , zipcode = False , user_city = False):
        if auth_id and auth_token and zipcode and user_city :
            url = "https://us-zipcode.api.smartystreets.com/lookup?"
            parameters = {
            "auth-id" : auth_id,
            "auth-token" : auth_token ,
            "zipcode": zipcode ,}
            response = requests.get(url , params=parameters)
            if response.status_code == 200 :
                if 'invalid_zipcode' in response.json()[0] :
                    return 'invalid zip code'
                elif response.json()[0]['city_states'] :
                    city_list = [city['city'] for city in response.json()[0]['city_states']]
                    if user_city in city_list :
                        return 'city zipcode match'
                    else :
                        return 'city zipcode do not match'    
        else :
            return 'bad request'     

    @http.route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
    def payment(self, **post):
        payment = super(WebsiteSale2, self).payment()
        order = request.website.sale_get_order()
        render_values = self._get_shop_payment_values(order, **post)
        

        company_id = request.website.company_id
        auth_id = company_id.auth_id
        tokent_id = company_id.tokent_id
        zipcode = request.env['res.partner'].browse(render_values['partner']).zip
        user_city = request.env['res.partner'].browse(render_values['partner']).city
        message = self.get_zipcode(auth_id=auth_id , auth_token = tokent_id , zipcode = zipcode , user_city = user_city)
        render_values['message'] = message
        print("################################## render_values",render_values)
        return request.render("website_sale.payment", render_values)



    