import frappe
from frappe import _
from jedermann.events.utils import configure_left_right_pair_packed_item
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice


class CustomSalesInvoice(SalesInvoice):
	def validate(self):
		super().validate()
		configure_left_right_pair_packed_item(self)

def set_validate_dn_data(doc, method):
    delivery_notes = list(set([item.delivery_note for item in doc.items if item.delivery_note]))

    if len(delivery_notes) == 1:
        delivery_note = delivery_notes[0]
        doc.custom_delivery_note = delivery_note

        posting_date = frappe.db.get_value("Delivery Note", delivery_note, "posting_date")
        if posting_date:
            doc.custom_delivery_date = posting_date
    elif len(delivery_notes) > 1:
        delivery_notes = [frappe.get_desk_link("Delivery Note", item.delivery_note) for item in doc.items if item.delivery_note]
        doc.custom_delivery_note = ""
        doc.custom_delivery_date = ""

        if len(delivery_notes) == 2:
            formatted_notes = " and ".join(delivery_notes)
        elif len(delivery_notes) > 2:
            last_delivery_note = delivery_notes[-1]

            formatted_notes = ", ".join([d for d in delivery_notes[:-1]]) + " and " + last_delivery_note

        frappe.throw(
            _("Sales Invoice contains items from {0}. All items should reference only one Delivery Note.").format(
                formatted_notes
            )
        )
