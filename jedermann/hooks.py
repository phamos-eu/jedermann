app_name = "jedermann"
app_title = "Jedermann"
app_publisher = "Phamos GmbH"
app_description = "Customisation for Jedermann"
app_email = "support@phamos.eu"
app_license = "mit"
required_apps = ["erpnext"]
app_logo_url = "/assets/jedermann/img/Jedermann-AG-Favicon.png"

website_context = {
	"favicon": "/assets/jedermann/img/Jedermann-AG-Favicon.png",
	"splash_image": "/assets/jedermann/img/Jedermann-AG-Favicon.png",
}

doctype_js = {
    "Sales Order": "public/js/sales_order.js",
    "Sales Invoice": "public/js/sales_invoice.js",
    "Delivery Note": "public/js/delivery_note.js",
}

override_whitelisted_methods = {
	"erpnext.stock.get_item_details.get_item_details": "jedermann.events.utils.custom_get_item_details"
}

doc_events = {
    "Sales Invoice": {
        "validate": "jedermann.events.sales_invoice.set_validate_dn_data"
    },
    "Product Bundle": {
        "validate": "jedermann.events.product_bundle.validate_left_right_pair_item"
    }
}

override_doctype_class = {
	"Sales Order": "jedermann.events.sales_order.CustomSalesOrder",
	"Sales Invoice": "jedermann.events.sales_invoice.CustomSalesInvoice",
    "Delivery Note": "jedermann.events.delivery_note.CustomDeliveryNote"
}

fixtures = [
    {
        "dt": "Letter Head", "filters": [
        [
            "name", "in", [
                "Standard 1.1"
            ]
        ]
    ]},
    {
        "dt": "Role", "filters": [
        [
            "name", "in", [
                "0 Geschäftsleitung"
            ]
        ]
    ]},
    {
        "dt": "Custom DocPerm", "filters": [
        [
            "role", "=", "0 Geschäftsleitung"
        ]
    ]},
    {
        "dt": "Print Settings"
    },
    {"dt": "Property Setter", "filters": [
        [
            "module", "=", "Jedermann"
        ]
    ]},
    {
        "dt": "Translation", "filters": [
        [
            "source_text", "in", [
                "Sort by Sales Order",
                "Sort by Item Code",
                "Sorting Option",
                "Batch Number",
                "Pallet Number",
                "Intern",
                "Supplier Quote Reference"
            ]
        ]
    ]}
]

jinja = {
    "methods": [
        "jedermann.events.jinja_functions.sort_items",
        "jedermann.events.jinja_functions.get_article_and_description_column_width",
        "jedermann.events.jinja_functions.get_product_labels",
        "jedermann.events.jinja_functions.group_items_by_pallet",
    ]
}
