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

    return item_details