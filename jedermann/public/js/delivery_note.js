frappe.ui.form.on("Delivery Note", {
    refresh: function(frm) {
        if (!frm.doc.is_return && (frm.doc.status != "Closed" || frm.is_new())) {
			if (frm.doc.docstatus === 0) {
				frm.add_custom_button(
					__("Sales Order"),
					function () {
						if (!frm.doc.customer) {
							frappe.throw({
								title: __("Mandatory"),
								message: __("Please Select a Customer"),
							});
						}
						erpnext.utils.map_current_doc({
							method: "jedermann.events.sales_order.make_delivery_note",
							args: {
								for_reserved_stock: 1,
							},
							source_doctype: "Sales Order",
							target: frm,
							setters: {
								customer: frm.doc.customer,
							},
							get_query_filters: {
								docstatus: 1,
								status: ["not in", ["Closed", "On Hold"]],
								per_delivered: ["<", 99.99],
								company: frm.doc.company,
								project: frm.doc.project || undefined,
							},
							allow_child_item_selection: true,
							child_fieldname: "items",
							child_columns: ["item_code", "qty"],
						});
					},
					__("Get Items From")
				);
			}
		}
    }
})

frappe.ui.form.on('Delivery Note Item', {
    custom_packing_uom(frm, cdt, cdn) {
        var item = frappe.get_doc(cdt, cdn);
        if(item.item_code && item.custom_packing_uom) {
            return frm.call({
                method: "erpnext.stock.get_item_details.get_conversion_factor",
                args: {
                    item_code: item.item_code,
                    uom: item.custom_packing_uom
                },
                callback: function(r) {
                    if(!r.exc) {
                        frappe.model.set_value(cdt, cdn, 'custom_packing_conversion_factor', r.message.conversion_factor);
                    }
                }
            });
        }
    }    
})
