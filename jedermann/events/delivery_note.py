import frappe
from frappe import _
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
from erpnext.stock.doctype.batch.batch import get_batch_qty
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from jedermann.events.utils import configure_left_right_pair_packed_item


class CustomDeliveryNote(DeliveryNote):
    def validate(self):
        if self._action == "submit":
            if not frappe.get_cached_value("Jedermann Settings", None, "enable_stock_entry_automation_for_batch_item"):
                return

            for item in self.items:
                if item.batch_no and item.warehouse and item.item_code:
                    qty = get_batch_qty(item.batch_no, item.warehouse, item.item_code)
                    if qty < item.qty:
                        qty = item.qty - qty
                        stock_entry = make_stock_entry(
                            item_code=item.item_code,
                            qty=qty,
                            to_warehouse=item.warehouse,
                            batch_no=item.batch_no,
                            purpose="Material Receipt",
                        )
                        stock_entry.add_comment("Comment", _("Adusting stock for Delivery Note {0}").format(self.name))
            self.set_actual_qty()

        self.set_batches_in_items()
        super().validate()
        configure_left_right_pair_packed_item(self)

    def set_batches_in_items(self):
        enable_batch_automation = frappe.get_cached_value("Jedermann Settings", None, "enable_batch_automation")
        if not enable_batch_automation:
            return

        for item in self.items:
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
