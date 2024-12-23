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
