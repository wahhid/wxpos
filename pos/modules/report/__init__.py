import pos
from pos.modules import Module

class ModuleLoader(Module):
    dependencies = ('base',)
    name = 'Generate PDF Reports for various modules'

    def menu(self):
        import pos.modules
        
        items = []
        if pos.modules.isInstalled('sales'):
            from pos.modules.report.panels import SalesReportPanel
            items.append({'parent': 'Reports', 'label': 'Sales', 'page': SalesReportPanel})
        if pos.modules.isInstalled('customer'):
            from pos.modules.report.panels import CustomersReportPanel
            items.append({'parent': 'Reports', 'label': 'Customers', 'page': CustomersReportPanel})
        if pos.modules.isInstalled('stock'):
            from pos.modules.report.panels import StockReportPanel
            from pos.modules.report.panels import StockDiaryReportPanel
            items.append({'parent': 'Reports', 'label': 'Stock', 'page': StockReportPanel})
            items.append({'parent': 'Reports', 'label': 'Stock Diary', 'page': StockDiaryReportPanel})
        if pos.modules.isInstalled('user'):
            from pos.modules.report.panels import UsersReportPanel
            items.append({'parent': 'Reports', 'label': 'Users', 'page': UsersReportPanel})
        
        return [[{'label': 'Reports', 'rel': -1, 'priority': 3}],
                items]
