import frappe
from frappe import _


def validate_left_right_pair_item(doc, method=None):
    if doc.custom_is_left_right_pair_item and len(doc.items) > 2:
        frappe.throw(_("Product Bundle is checked with 'Is Left Right Pair Item', it must contain only two List items in the package."))