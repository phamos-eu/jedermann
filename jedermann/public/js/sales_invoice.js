frappe.ui.form.on('Sales Invoice', {
    custom_sales_invoice_type(frm) {
        if (frm.doc.custom_sales_invoice_type == "Korrekturrechnung") {
            frm.set_value("is_return", 1)
        } else if (frm.doc.custom_sales_invoice_type == "Gutschrift") {
            frm.set_value("is_return", 1)
        } else {
            frm.set_value("is_return", 0)
        }
    }
})
