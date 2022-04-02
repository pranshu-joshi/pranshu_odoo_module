{
    'name': 'Fleet Management',
    'description': '''This modules is used to manage all kinds of automotives''',
    'version': '1.0',
    'category': 'Transport',
    'depends': ['base', 'mail'],
    'author': 'Pranshu Joshi',
    'data': [
        'security/cars_security.xml',
        'security/ir.model.access.csv',
        'views/cars_view.xml',
        'data/fleet_management_sequence.xml'
    ],
    'assets':{
        'web.assets_backend':['fleet_management/static/src/scss/cars.scss']
    },
    'installable': True,
    'auto_install': False,
    'application': True
}
