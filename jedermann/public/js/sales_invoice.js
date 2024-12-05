frappe.ui.form.on('Sales Invoice', {
    setup(frm) {
        set_fields(frm)
    },
    custom_sales_invoice_type(frm) {
        set_fields(frm)
    }
})


var set_fields = function (frm) {
    if (frm.doc.custom_sales_invoice_type == "Korrekturrechnung") {
        frm.set_value("is_return", 1)

        frm.set_df_property("is_return", "hidden", 0);
        frm.set_df_property("is_debit_note", "hidden", 1);
        frm.set_df_property("return_against", "hidden", 0); 

    } else if (frm.doc.custom_sales_invoice_type == "Gutschrift") {
        frm.set_value("is_return", 1)

        frm.set_df_property("is_return", "hidden", 0);
        frm.set_df_property("is_debit_note", "hidden", 1);
        frm.set_df_property("return_against", "hidden", 1); 
        
    } else {
        frm.set_value("is_return", 0)

        frm.set_df_property("is_return", "hidden", 1);
        frm.set_df_property("is_debit_note", "hidden", 1);
        frm.set_df_property("return_against", "hidden", 1); 

    }
    frm.refresh_fields()
}