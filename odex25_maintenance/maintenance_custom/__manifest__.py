{
    'name':'Maintenance Custom ',
    'version':'1.0',
    'summary':'Maintenance Custom system',
    'sequence': 1,
    'description':
    """
    """,
    'depends':['sale', 'maintenance','hr_maintenance'],
    'data':[
            'security/ir.model.access.csv',
            'data/ir_sequences_data.xml',
            'views/maintenance_view.xml',
            'wizard/maintenance_report_wiz_view.xml',
            'reports/equipment_report.xml',
            'reports/spare_part_report.xml',
            'reports/general_maintenance_report.xml',
            'reports/report_maintenance_request.xml',
            'reports/maintenance_report.xml',
            'reports/maintenance_team_report.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable':
    True,
    'application':
    True,
}
