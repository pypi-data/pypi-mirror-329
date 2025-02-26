from . import partner, messages
from typing import List, Literal
from .types import Order, Transfer, TransferLine

# Define valid order states
OrderState = Literal['draft', 'sent', 'sale', 'done', 'cancel']

def search_order_ids_by_email(self, emails: List[str]) -> List[int]:
    """Search for orders by email addresses, using the partner id search by email function."""
    partner_ids = partner.search_partner_ids_by_email(self, emails)

    if not partner_ids:
        return []

    return self.connection.env['sale.order'].search([('partner_id', 'in', partner_ids)])

def search_order_ids_by_email_and_state(self, email: str, state: OrderState) -> List[int]:
    """Search for orders by email address and state."""
    partner_ids = partner.search_partner_ids_by_email(self, email)

    if not partner_ids:
        return []

    return self.connection.env['sale.order'].search([
        ('partner_id', 'in', partner_ids),
        ('state', '=', state)
    ])

def search_order_ids_by_partner_id_and_state(self, partner_id: int, state: OrderState) -> List[int]:
    """Search for orders by partner ID and state."""
    return self.connection.env['sale.order'].search([
        ('partner_id', '=', partner_id),
        ('state', '=', state)
    ])

def search_order_ids_by_partner_id(self, partner_ids: List[int]) -> List[int]:
    """Search for orders by partner IDs."""
    return self.connection.env['sale.order'].search([('partner_id', 'in', partner_ids)])

def search_order_line_ids_by_order_id(self, order_ids: List[int]) -> List[int]:
    """Fetch order lines for given order IDs."""
    return self.connection.env['sale.order.line'].search([('order_id', 'in', order_ids)])

def fetch_order_lines_by_id(self, order_line_ids: List[int]) -> List[int]:
    """Fetch order line details."""
    return self.connection.env['sale.order.line'].read(order_line_ids, ['product_id', 'product_uom_qty', 'price_unit', 'product_uom'])

def fetch_orders_by_id(self, order_ids: List[int]) -> List[Order]:
    return [{
        "name": order['name'],
        "order_lines": fetch_order_lines_by_id(self, search_order_line_ids_by_order_id(self, [order['id']])),
        "state": order['state'],
        "date_order": order['date_order'],
        "partner_id": order['partner_id'][0] if isinstance(order['partner_id'], (list, tuple)) else order['partner_id'],
        "partner_name": order['partner_id'][1] if isinstance(order['partner_id'], (list, tuple)) else '',
        "invoice_status": order['invoice_status'],
        "amount_total": order['amount_total'],
        "transfers": fetch_transfers_by_id(self, order['picking_ids']),
        "messages": messages.fetch_messages_by_id(self, order['message_ids'])
    } for order in self.connection.env['sale.order'].read(order_ids, ['name', 'order_line', 'state', 'date_order', 'partner_id', 'invoice_status', 'amount_total', 'message_ids', 'picking_ids'])]


def search_transfer_ids_by_order_ids(self, order_ids: List[int]) -> List[int]:
    """Search for stock transfers by order IDs."""
    return self.connection.env['stock.picking'].search([('sale_id', 'in', order_ids)])

def fetch_transfers_by_id(self, transfer_ids: List[int]) -> List[Transfer]:
    """Fetch transfer details."""
    return [{
        "name": transfer["name"],
        "state": transfer["state"],
        "date_done": transfer["date_done"],
        "location_id": transfer["location_id"][0] if isinstance(transfer["location_id"], (list, tuple)) else transfer["location_id"],
        "location_name": transfer["location_id"][1] if isinstance(transfer["location_id"], (list, tuple)) else '',
        "location_dest_id": transfer["location_dest_id"][0] if isinstance(transfer["location_dest_id"], (list, tuple)) else transfer["location_dest_id"],
        "location_dest_name": transfer["location_dest_id"][1] if isinstance(transfer["location_dest_id"], (list, tuple)) else '',
        "items": fetch_transfer_lines_by_id(self, transfer["move_line_ids_without_package"]),
        "messages": messages.fetch_messages_by_id(self, transfer['message_ids'])
    } for transfer in self.connection.env['stock.picking'].read(transfer_ids, ['name', 'state', 'date_done', 'location_id', 'location_dest_id', 'move_line_ids_without_package', 'message_ids'])]

def fetch_transfer_lines_by_id(self, transfer_line_ids: List[int]) -> List[TransferLine]:
    """Fetch transfer line details."""
    transfer_lines = self.connection.env['stock.move.line'].read(transfer_line_ids, ['product_id', 'product_reference_code', 'qty_done', 'quantity_product_uom'])

    return [{
        "product": transfer_line['product_id'][0] if isinstance(transfer_line['product_id'], (list, tuple)) else transfer_line['product_id'],
        "product_name": transfer_line['product_id'][1] if isinstance(transfer_line['product_id'], (list, tuple)) else '',
        "reference_code": transfer_line['product_reference_code'],
        "quantity": transfer_line['quantity_product_uom'],
        "quantity_done": transfer_line['qty_done']
    } for transfer_line in transfer_lines]


# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_orders_by_email(self, emails: List[str]) -> List[Order]:
    """Fetch orders by email addresses."""
    return self.fetch_orders_by_id(self.search_order_ids_by_email(emails))

def fetch_orders_by_email_and_state(self, email: str, state: OrderState) -> List[Order]:
    """Fetch orders by email address and state."""
    return self.fetch_orders_by_id(self.search_order_ids_by_email_and_state(email, state))

def fetch_orders_by_partner_id_and_state(self, partner_id: int, state: OrderState) -> List[Order]:
    """Fetch orders by partner ID and state."""
    return self.fetch_orders_by_id(self.search_order_ids_by_partner_id_and_state(partner_id, state))

def fetch_orders_by_partner_id(self, partner_ids: List[int]) -> List[Order]:
    """Fetch orders by partner IDs."""
    return self.fetch_orders_by_id(self.search_order_ids_by_partner_id(partner_ids))

def fetch_transfers_by_order_id(self, order_ids: List[int]) -> List[Transfer]:
    """Fetch stock transfers for given order IDs."""
    return self.fetch_transfers_by_id(self.search_transfer_ids_by_order_ids(order_ids))

def fetch_transfer_lines_by_order_id(self, order_ids: List[int]) -> List[TransferLine]:
    """Fetch stock transfer lines for given order IDs."""
    return self.fetch_transfer_lines_by_id(self.search_transfer_ids_by_order_ids(order_ids))
