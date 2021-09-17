# Copyright 2019 ForgeFlow S.L.
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import odoo.tests.common as common
from odoo import fields


class TestPurchaseLastPriceInfo(common.TransactionCase):

    def setUp(self):
==== BASE ====
        super(TestPurchaseLastPriceInfo, self).setUp()
        self.purchase_model = self.env["purchase.order"]
        self.purchase_line_model = self.env["purchase.order.line"]
        self.product = self.env.ref("product.consu_delivery_01")
        self.partner = self.env.ref("base.res_partner_1")
==== BASE ====

    def test_purchase_last_price_info_demo(self):
==== BASE ====
        purchase_order = self.env.ref("purchase.purchase_order_6")
        purchase_order.button_confirm()
==== BASE ====
        purchase_lines = self.purchase_line_model.search(
==== BASE ====
            [
                ("product_id", "=", self.product.id),
                ("state", "in", ["purchase", "done"]),
            ]
        ).sorted(key=lambda l: l.order_id.date_order, reverse=True)
==== BASE ====
        self.assertEqual(
==== BASE ====
            fields.Datetime.from_string(purchase_lines[:1].order_id.date_order).date(),
            fields.Datetime.from_string(self.product.last_purchase_date).date(),
        )
==== BASE ====
        self.assertEqual(
==== BASE ====
            purchase_lines[:1].price_unit, self.product.last_purchase_price
        )
==== BASE ====
        self.assertEqual(
==== BASE ====
            purchase_lines[:1].order_id.partner_id, self.product.last_supplier_id
        )
==== BASE ====

    def test_purchase_last_price_info_new_order(self):
==== BASE ====
        purchase_order = self.purchase_model.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom": self.product.uom_id.id,
                            "price_unit": self.product.standard_price,
                            "name": self.product.name,
                            "date_planned": fields.Datetime.now(),
                            "product_qty": 1,
                        },
                    )
                ],
            }
        )
        purchase_order.button_confirm()
==== BASE ====
        self.assertEqual(
==== BASE ====
            fields.Datetime.from_string(purchase_order.date_order).date(),
            fields.Datetime.from_string(self.product.last_purchase_date).date(),
        )
        self.assertEqual(
            purchase_order.order_line[:1].price_unit, self.product.last_purchase_price
        )
        self.assertEqual(self.partner, self.product.last_supplier_id)
        purchase_order.button_cancel()
        self.assertEqual(purchase_order.state, "cancel")
==== BASE ====
