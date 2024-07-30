{
    'name': 'Inventory Reports Custom',
    'version': '1.0',
    'author': 'TamkeenTech',
    'summary': 'Additional Reports for Warehouse Module',
    'description': """ 
    This Module Contains :
     1- Inventory Report which display Products Qtys.
   """,
    'depends': ['socpa_stock_custom'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/reports_view.xml',
        'wizard/incoming_outgoing_report.xml',
        'wizard/exchange_request_report.xml',
        'wizard/inventory_adjustment_report.xml',
        'wizard/scrap_report_wizard.xml',
        'wizard/internal_transfer_report.xml',
        'report/custom_paperformat.xml',
        'report/incoming_outgoing_template.xml',
        'report/incoming_outgoing_price_template.xml',
        'report/exchane_request_report.xml',
        'report/scrap_report.xml',
        'report/inventory_adjustment_report.xml',
        'report/internal_transfer_report.xml',
        'report/exchange_request_report.xml',
        'report/report_stock_inventory.xml',
        'report/stock_picking_report.xml'

    ],
    'installable': True,
    'application': False,
}
