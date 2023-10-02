# -*- coding: utf-8 -*-
{
    'name': "Custom rex",

    'summary': '',
    'sequence': -1,

    'description': """
        Customized res_partner fields required-
        
    """,

    'author': "javaid.afridi34@gmail.com",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','sale','website_sale'],

    # always loaded
'data': [   
        'reports/report_saleorder_document.xml',
        'views/custom_views.xml',   
    ],
    # only loaded in demonstration mode
    
}
