// Copyright (c) 2025, Phamos GmbH and contributors
// For license information, please see license.txt

frappe.query_reports["Lade-Liste"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 1,
			"width": 150
		}
	]
};