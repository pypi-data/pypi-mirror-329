from . import messages
from typing import List, Dict, Any
from .types import Ticket
from .utils.text_processing import strip_html as _strip_html
from datetime import datetime

def search_ticket_ids_by_author_email(self, emails: List[str]) -> List[int]:
    """Search for helpdesk tickets by author emails."""
    return self.connection.env['helpdesk.ticket'].search([('partner_email', 'in', emails)])

def search_ticket_ids_by_partner_id(self, partner_ids: List[int]) -> List[int]:
    """Search for helpdesk tickets by partner IDs."""
    return self.connection.env['helpdesk.ticket'].search([('partner_id', 'in', partner_ids)])

def search_ticket_ids_updated_since(self, timestamp: int, limit: int) -> List[int]:
    """Search for ticket IDs that have been updated since the given timestamp."""

    if limit == 0:
        limit = 50

    return self.connection.env['helpdesk.ticket'].search([
        ('write_date', '>=', datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'))
    ], limit=limit, order='write_date DESC')

def fetch_tickets_by_id(self, ticket_ids: List[int]) -> List[Ticket]:
    """Fetch helpdesk ticket details including messages and user info."""
    return [{
        "id": ticket['id'],
        "subject": ticket['name'],
        "author_id": ticket['partner_id'][0],
        "author_name": ticket['partner_name'],
        "author_email": ticket['partner_email'],
        "description": ticket['description'],
        "messages": sorted(
            [m for m in messages.fetch_messages_by_id(self, ticket['message_ids'])
             if m['body'] and m['body'].strip()],  # Filter out empty messages
            key=lambda x: x['date'],
            reverse=True  # Newest first
        ),
        "stage_id": ticket['stage_id'][0] if isinstance(ticket['stage_id'], (list, tuple)) else ticket['stage_id'],
        "stage_name": ticket['stage_id'][1] if isinstance(ticket['stage_id'], (list, tuple)) else '',
        "create_date": ticket['create_date']
    } for ticket in self.connection.env['helpdesk.ticket'].read(ticket_ids, ['name', 'partner_id', 'partner_name', 'partner_email', 'description', 'message_ids', 'stage_id', 'create_date'])]


def fetch_ticket_summaries_by_id(self, ticket_ids: List[int]) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for display in listings. Does not include messages or most user info."""
    return [{
        "id": ticket['id'],
        "subject": ticket['name'],
        "author_name": ticket['partner_name'],
        "description": _strip_html(ticket['description']),  # Strip HTML for summaries
        "write_date": ticket['write_date'],
        "stage": ticket['stage_id'][1] if isinstance(ticket['stage_id'], (list, tuple)) else ''
    } for ticket in self.connection.env['helpdesk.ticket'].read(
        ticket_ids,
        ['name', 'partner_name', 'description', 'write_date', 'stage_id']
    )]

# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_tickets_by_author_email(self, emails: List[str]) -> List[Ticket]:
    """Fetch helpdesk tickets by author emails."""
    return self.fetch_tickets_by_id(self.search_ticket_ids_by_author_email(emails))

def fetch_tickets_by_partner_id(self, partner_ids: List[int]) -> List[Ticket]:
    """Fetch helpdesk tickets by partner IDs."""
    return self.fetch_tickets_by_id(self.search_ticket_ids_by_partner_id(partner_ids))

def fetch_tickets_updated_since(self, timestamp: int, limit: int) -> List[Ticket]:
    """Fetch helpdesk tickets updated since the given timestamp."""
    return self.fetch_tickets_by_id(self.search_ticket_ids_updated_since(timestamp, limit))

def fetch_ticket_summaries_by_author_email(self, emails: List[str]) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for display in listings by author emails. Does not include messages or most user info."""
    return self.fetch_ticket_summaries_by_id(self.search_ticket_ids_by_author_email(emails))

def fetch_ticket_summaries_by_partner_id(self, partner_ids: List[int]) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for display in listings by partner IDs. Does not include messages or most user info."""
    return self.fetch_ticket_summaries_by_id(self.search_ticket_ids_by_partner_id(partner_ids))

def fetch_ticket_summaries_updated_since(self, timestamp: int, limit: int) -> List[Dict[str, Any]]:
    """Fetch basic ticket information for display in listings updated since the given timestamp. Does not include messages or most user info."""
    return self.fetch_ticket_summaries_by_id(self.search_ticket_ids_updated_since(timestamp, limit))