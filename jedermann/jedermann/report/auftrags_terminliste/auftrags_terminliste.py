# Copyright (c) 2025, Phamos GmbH and contributors
# For license information, please see license.txt

from frappe import _
import frappe


def execute(filters=None):
	columns = get_column()
	data = get_data(filters)
	return columns, data


def get_column():
	return [
		{
			"label": _("Vers.Termin"),
			"fieldname": "version_termin",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": "Auftrag",
			"fieldname": "po_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Intern",
			"fieldname": "intern",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 120
		},
		{
			"label": "Artikel-Nr.",
			"fieldname": "item_code",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Customer Item Code",
			"fieldname": "customer_item_code",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": "Bezeichnung",
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 260
		},
		{
			"label": "BM",
			"fieldname": "bm",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": "GM",
			"fieldname": "gm",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": "OM",
			"fieldname": "om",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": "Lief-Termin",
			"fieldname": "delivery_date",
			"fieldtype": "Date"
		}
	]


def get_data(filters):
	SalesOrder = frappe.qb.DocType("Sales Order")
	SalesOrderItem = frappe.qb.DocType("Sales Order Item")

	data = (
		frappe.qb.from_(SalesOrder)
		.inner_join(SalesOrderItem)
		.on(SalesOrderItem.parent == SalesOrder.name)
		.select(
			SalesOrder.po_no,
			SalesOrder.name.as_("intern"),
			SalesOrder.delivery_date,
			SalesOrderItem.item_name,
			SalesOrderItem.item_code,
			SalesOrderItem.customer_item_code,
			SalesOrderItem.qty.as_("bm"),
			SalesOrderItem.delivered_qty.as_("gm"),
			(SalesOrderItem.qty - SalesOrderItem.delivered_qty).as_("om")
		)
		.where(SalesOrder.customer == filters.customer)
		.where(SalesOrder.docstatus == 1)
		.where((SalesOrderItem.qty - SalesOrderItem.delivered_qty) > 0)
		.orderby(SalesOrder.creation, order=frappe.qb.asc)
		.orderby(SalesOrder.name, order=frappe.qb.asc)
		.run(as_dict=1, debug=1)
	)

	return data