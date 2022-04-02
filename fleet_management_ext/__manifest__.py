{
    'name': 'Fleet Management Extension',
    'descripstion': '''This module is the extension of the fleet management module and ''',
    'version': '1.0',
    'category': 'Transport',
    'depends': ['fleet_management'],
    'author': 'Pranshu Joshi',
    'data': [
        'security/ir.model.access.csv',
        'views/cars_view.xml',
        'views/inheriting_view.xml',
        'views/template_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
