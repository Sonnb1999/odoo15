{
    'name': 'internship',
    'version': '15.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'management Tutorials For Beginners',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': 'Odoo Mates',
    'maintainer': '',
    'website': '',
    'live_test_url': '',
    'depends': ['project'],
    'demo': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/partner_tag_data.xml',
        # 'data/partners.tag.csv',
        # 'data/cron.xml',
        'wizards/batch_update_student.xml',
        'wizards/batch_update_teacher.xml',
        'views/menu.xml',
        'views/courses.xml',
        'views/partners.xml',
        'views/instructors.xml',
        'views/teachers.xml',
        'views/plans.xml',
        'views/classes.xml',
        'views/students.xml',
        'views/councils.xml',
        'views/my_custom_assets.xml', 
    ],
    # 'css': ['static/src/css/styles.css'],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}