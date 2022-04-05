# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Qu Pack Modules - Data Migration",
    "summary": "All modules needed to migration Using XML-RPC",
    "version": "15.0.1.0.0",
    "category": "Pro",
    "website": "https://www.qubiq.es",
    "author": "QubiQ, Odoo",
    "license": "AGPL-3",
    "application": False,
    "installable": True,

    "depends": [
        "sale",
        "purchase",
        "stock",
        "account",
        "contacts",
        "qu_allow_duplicated_barcode",
	    "qu_allow_unbalanced_move",
        "disable_vat_check",
    ],

    "data": [
        "data/data.xml",
    ],
}
