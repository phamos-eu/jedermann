app_name = "jedermann"
app_title = "Jedermann"
app_publisher = "Phamos GmbH"
app_description = "Customisation for Jedermann"
app_email = "support@phamos.eu"
app_license = "mit"
required_apps = ["erpenext"]

doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js"
}

doc_events = {
    "Sales Invoice": {
        "validate": "jedermann.events.sales_invoice.set_validate_dn_data"
    }
}

fixtures = [
    {
        "dt": "Print Format", "filters": [
        [
            "name", "in", [
                'Sales Invoice 1.1'
            ]
        ]
    ]},
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
    }
]