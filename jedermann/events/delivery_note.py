import frappe


def set_batches_in_items(doc, method):
    enable_batch_automation = frappe.get_cached_value("Jedermann Settings", None, "enable_batch_automation")
    if not enable_batch_automation:
        return

    for item in doc.items:
        if item.custom_batch_number and item.custom_batch_number != item.batch_no:
            item.batch_no = get_batch_no_from_custom_batches(item)



def get_batch_no_from_custom_batches(item):
    batch_name = frappe.db.exists("Batch", {"batch_id": item.custom_batch_number, "item": item.item_code})
    if not batch_name:
        batch = frappe.new_doc("Batch")
        batch.item =  item.item_code
        batch.batch_id = item.custom_batch_number
        batch.save()
        batch_name = batch.name

    # frappe.msgprint("Batch Automation is WIP for {} ".format(item.custom_batch_number))

    return batch_name
