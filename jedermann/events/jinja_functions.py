def sort_items(items, sort_by):
    def sort_key(item):
        item = item.as_dict()
        if sort_by == "Sort by Item Code":
            return item['item_code']
        elif sort_by == "Sort by Sales Order":
            return (item.get('against_sales_order') is not None, item.get('against_sales_order', ''), item['item_code'])

    return sorted(items, key=sort_key)


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
