app_name = "jedermann"
app_title = "Jedermann"
app_publisher = "Phamos GmbH"
app_description = "Customisation for Jedermann"
app_email = "support@phamos.eu"
app_license = "mit"
required_apps = ["erpnext"]

doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js"
}

doc_events = {
    "Sales Invoice": {
        "validate": "jedermann.events.sales_invoice.set_validate_dn_data"
    }
}

override_doctype_class = {
	"Sales Order": "jedermann.events.sales_order.CustomSalesOrder"
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
    {
        "dt": "Translation", "filters": [
        [
            "language", "=", "de"
        ],
        [
            "source_text", "in", [
                "Sort by Sales Order",
                "Sort by Item Code",
                "Sorting Option"
            ]
        ]
    ]}
]

jinja = {
    "methods": [
        "jedermann.events.jinja_functions.sort_items",
        "jedermann.events.jinja_functions.get_article_and_description_column_width",
    ]
}
