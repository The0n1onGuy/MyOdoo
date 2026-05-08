{
    'name': "custom_crm",

    'summary': "Modulo CRM para gestion de visitas",

    'description': """
        Modulo CRM para gestion de visitas.....
    """,

    'author': "OnionCompany",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        'views/views.xml'
        ,'views/templates.xml'
        ,'demo/demo.xml'
        ,'reports/visit.xml'
        ,'security/ir.model.access.csv'
        ,'security/security.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}

