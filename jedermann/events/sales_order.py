import frappe
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
from frappe.utils import get_datetime

class CustomSalesOrder(SalesOrder):
	@property
	def custom_week_number(self):
		if self.delivery_date:
			date = get_datetime(self.delivery_date)
			iso_calendar = date.isocalendar()
			week_number = iso_calendar[1]
			return week_number
