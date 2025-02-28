import frappe
from frappe.utils import cint
from jedermann.events.utils import is_product_bundle


def sort_items(items, sort_by):
    def sort_key(item):
        item = item.as_dict()
        if sort_by == "Sort by Item Code":
            return item['item_code']
        elif sort_by == "Sort by Sales Order":
            return (item.get('against_sales_order') is not None, item.get('against_sales_order', ''), item['item_code'])

    return sorted(items, key=sort_key)


def get_product_labels(doc):
    labels = []
    for item in doc.items:
        if is_product_bundle(item.item_code):
            for packed_item in doc.packed_items:
                packed_item = packed_item.as_dict()
                packed_item["uom"] = item.get("uom")
                packed_item["custom_packing_conversion_factor"] = item.get("custom_packing_conversion_factor")
                packed_item["custom_packing_uom"] = item.get("custom_packing_uom")
                packed_item["customer_item_code"] = packed_item.get("custom_customer_item_code")
                labels.extend(generate_labels(packed_item))          
        else:
            item = item.as_dict()
            labels.extend(generate_labels(item))

    return labels


def generate_labels(item):
    labels = []
    if item.custom_packing_conversion_factor == 1 or not (item.custom_packing_uom):
        label_item = item.copy()
        label_item["label_qty"] = (item.qty)
        labels.append(label_item)
        return labels

    full_labels = item.qty // item.custom_packing_conversion_factor
    remainder = item.qty % item.custom_packing_conversion_factor

    for _ in range(frappe.utils.cint(full_labels)):
        label_item = item.copy()
        label_item["label_qty"] = cint(item.custom_packing_conversion_factor)
        labels.append(label_item)

    if remainder > 0:
        remainder_item = item.copy()
        remainder_item["label_qty"] = cint(remainder)
        labels.append(remainder_item)

    return labels


def get_article_and_description_column_width(items, key, total_both_columns_width):
    item_col_lengths = (11, 20, 25)
    column_width = {
        "item_code": 0,
        "description": 0,
    }

    max_item_code_length = max([(item.get('item_code') or '').__len__() for item in items])
    max_customer_item_code_length = max([(item.get('customer_item_code') or '').__len__() for item in items])

    max_item_code_length = max(max_item_code_length, max_customer_item_code_length)

    if max_item_code_length <= 11:
        column_width["item_code"] = item_col_lengths[0]
        column_width["description"] =   total_both_columns_width - item_col_lengths[0]

    elif max_item_code_length <= 20:
        column_width["item_code"] = item_col_lengths[1]
        column_width["description"] = total_both_columns_width - item_col_lengths[1]
    else:
        column_width["item_code"] = item_col_lengths[2]
        column_width["description"] = total_both_columns_width - item_col_lengths[2]
    
    return column_width.get(key, 0)


def group_items_by_pallet(doc):
    grouped_items = {}
    for item in doc.items:
        if is_product_bundle(item.item_code):
            pass
            for packed_item in doc.packed_items:
                packed_item = packed_item.as_dict()
                packed_item["custom_packing_conversion_factor"] = item.get("custom_packing_conversion_factor")
                packed_item["custom_packing_uom"] = item.get("custom_packing_uom")
                packed_item["against_sales_order"] = item.get("against_sales_order")
                packed_item["customer_item_code"] = packed_item.get("custom_customer_item_code")
                group_item_by_pallet(packed_item, grouped_items)

        else:
            group_item_by_pallet(item, grouped_items)

    return grouped_items


def group_item_by_pallet(item, grouped_items):
    pallet_no = item.get('custom_pallet_number')
    if pallet_no:
        if pallet_no not in grouped_items:
            grouped_items[pallet_no] = {
                'items': [],
                'total_qty': 0
            }
        grouped_items[pallet_no]['items'].append(item)
        if item.custom_packing_conversion_factor == 1:
            grouped_items[pallet_no]['total_qty'] += item.get('custom_packing_conversion_factor')
        else:
            total_items = item.qty
            box_capacity = item.custom_packing_conversion_factor or 1
            grouped_items[pallet_no]['total_qty'] += (total_items + box_capacity - 1) // box_capacity
