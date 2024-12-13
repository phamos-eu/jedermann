def sort_items(items, sort_by):
    def sort_key(item):
        item = item.as_dict()
        if sort_by == "Sorting by Item Code":
            return item['item_code']
        elif sort_by == "Sorting by Sales Order":
            return (item.get('against_sales_order') is not None, item.get('against_sales_order', ''), item['item_code'])

    return sorted(items, key=sort_key)
