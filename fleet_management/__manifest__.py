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
        'views/update_price_wiz_view.xml',
        'views/alt_report_wiz_view.xml',
        'views/overall_report_wiz_view.xml',
        'views/cars_view.xml',
        'views/update_price_wiz_inherit_view.xml',
        'views/update_features_new.xml',
        'views/update_company_view.xml',
        'data/fleet_management_sequence.xml',
        'views/car_report_template.xml',
        'report/cars_analysis_report.xml',
        'report/car_report.xml',
        'report/overall_car_report.xml',
        'views/report_wiz_view.xml',
        'views/car_xls_wiz.xml',
        'views/car_overall_report_template.xml',
    ],
    'assets':{
        'web.assets_backend':['fleet_management/static/src/scss/cars.scss']
    },
    'installable': True,
    'auto_install': False,
    'application': True
}
