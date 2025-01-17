from frappe import _
import frappe
from erpnext.stock.get_item_details import get_item_details, get_conversion_factor


@frappe.whitelist()
def custom_get_item_details(args, doc=None, for_validate=False, overwrite_warehouse=True):
    item_details = get_item_details(args, doc=doc, for_validate=for_validate, overwrite_warehouse=overwrite_warehouse)
    if item_details.get("item_code"):
        custom_packing_uom = frappe.get_cached_value("Item", item_details.get("item_code"), "custom_packing_uom")
        if custom_packing_uom:
            item_details["custom_packing_uom"] = custom_packing_uom
            conversion_factor = get_conversion_factor(item_details.get("item_code"), custom_packing_uom)
            item_details["custom_packing_conversion_factor"] = conversion_factor.get("conversion_factor")
        else:
            item_details["custom_packing_uom"] = ""
            item_details["custom_packing_conversion_factor"] = 1

    return item_details


def validate_and_configure_left_right_pair_packed_item(doc):
    for item in doc.items:
        if frappe.db.exists("Product Bundle", {"name": item.item_code, "disabled": 0, "custom_is_left_right_pair_item": 1}):
            if item.qty and item.qty % 2 != 0:
                frappe.throw(_("Idx: {0}, {1} is checked with 'Is Left Right Pair Item', so qty must be even number.").format(item.idx, frappe.get_desk_link("Product Bundle", item.item_code)))

    for d in doc.packed_items:
        if frappe.get_cached_value("Product Bundle", d.parent_item, "custom_is_left_right_pair_item"):
            line_item_table = d.parenttype + " Item"
            parent_item_qty = frappe.db.get_value(line_item_table, d.parent_detail_docname, "qty")
            uom = frappe.get_cached_value("Product Bundle", d.parent_item, "custom_pair_uom")
            if not uom:
                frappe.throw(_("Pair UOM is mandatory for {0} is checked with 'Is Left Right Pair Item'").format(frappe.get_desk_link("Product Bundle", d.parent_item)))
            if parent_item_qty and uom:
                d.qty = parent_item_qty/2
                d.uom = uom
