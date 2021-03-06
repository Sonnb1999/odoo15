{
    'name': 'Real Estate',
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'management Tutorials For Beginners',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': 'B.N.Son',
    'maintainer': '',
    'website': '',
    'live_test_url': '',
    'depends': ['sale_management', 'hr'],
    'demo': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences_data.xml',
        # 'data/partners.tag.csv',
        # 'data/cron.xml',
        # 'wizards/batch_update_student.xml',
        # 'wizards/batch_update_teacher.xml',
        # 'wizards/batch_update_course.xml',

        'views/menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
    ],
    # 'css': ['static/src/css/styles.css'],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
