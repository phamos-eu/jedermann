import frappe
from frappe import _
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from erpnext.stock.doctype.batch.batch import get_batch_qty
from jedermann.events.utils import validate_and_configure_left_right_pair_packed_item, is_product_bundle


class CustomDeliveryNote(DeliveryNote):
    def validate(self):
        if self._action == "submit": # making sure that it run on validate event just before submit
            if not frappe.get_cached_value("Jedermann Settings", None, "enable_stock_entry_automation_for_batch_item"):
                return

            for item in self.items:
                if item.batch_no and item.warehouse and item.item_code and not is_product_bundle(item.item_code):
                    qty = get_batch_qty(item.batch_no, item.warehouse, item.item_code)
                    if qty < item.qty:
                        qty = item.qty - qty
                        stock_entry = make_stock_entry(
                            item_code=item.item_code,
                            qty=qty,
                            warehouse=item.warehouse,
                            batch_no=item.batch_no,
                            dn=self.name
                        )
                    item.actual_batch_qty = qty
            self.set_actual_qty()

            for item in self.packed_items:
                if item.batch_no and item.warehouse and item.item_code:
                    qty = get_batch_qty(item.batch_no, item.warehouse, item.item_code)
                    if qty < item.qty:
                        qty = item.qty - qty
                        stock_entry = make_stock_entry(
                            item_code=item.item_code,
                            qty=qty,
                            warehouse=item.warehouse,
                            batch_no=item.batch_no,
                            dn=self.name
                        )
                    item.actual_batch_qty = qty

        self.set_batches_in_items()
        super().validate()
        validate_and_configure_left_right_pair_packed_item(self)

    def set_batches_in_items(self):
        enable_batch_automation = frappe.get_cached_value("Jedermann Settings", None, "enable_batch_automation")
        if not enable_batch_automation:
            return

        for item in self.items:
            if item.custom_batch_number and item.custom_batch_number != item.batch_no and not is_product_bundle(item.item_code):
                item.batch_no = get_batch_no_from_custom_batches(item)

        for item in self.packed_items:
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

    return batch_name


def make_stock_entry(item_code, qty, warehouse, batch_no, dn):
    se = frappe.new_doc("Stock Entry")

    se.stock_entry_type = "Material Receipt"
    se.append("items", {
        "item_code": item_code,
        "qty": qty,
        "t_warehouse": warehouse,
        "use_serial_batch_fields": 1,
        "batch_no": batch_no,
    })
    se.submit()
    se.add_comment("Comment", _("Adjusting stock for Delivery Note {0}").format(dn))

    return se
