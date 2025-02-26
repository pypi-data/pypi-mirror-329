from typing import List, Optional
from datetime import datetime
from .types import MailingStatistic, MailingContact, MassMailing

def search_mailing_ids_by_subject(self, subject: str) -> List[int]:
    """Search for mass mailings by subject."""
    return self.connection.env['mail.mass_mailing'].search([
        ('subject', 'ilike', subject)
    ])

def search_mailing_ids_by_date_range(self, start_date: datetime, end_date: datetime) -> List[int]:
    """Search for mass mailings within a date range."""
    return self.connection.env['mail.mass_mailing'].search([
        ('sent_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent_date', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_mailings_by_ids(self, mailing_ids: List[int]) -> List[MassMailing]:
    """Fetch mass mailing details by IDs."""
    return [{
        'id': mailing['id'],
        'name': mailing['name'],
        'subject': mailing['subject'],
        'sent_date': mailing['sent_date'],
        'state': mailing['state'],
        'mailing_model': mailing['mailing_model'],
        'statistics_ids': mailing['statistics_ids'],
        'contact_list_ids': mailing['contact_list_ids']
    } for mailing in self.connection.env['mail.mass_mailing'].read(
        mailing_ids,
        ['name', 'subject', 'sent_date', 'state', 'mailing_model', 'statistics_ids', 'contact_list_ids']
    )]

def search_statistics_ids_by_mailing_id(self, mailing_id: int) -> List[MailingStatistic]:
    """Search statistics for a specific mass mailing."""
    return self.connection.env['mail.mail.statistics'].search([
        ('mass_mailing_id', '=', mailing_id)
    ])

def search_statistics_ids_by_recipient(self, email: str) -> List[MailingStatistic]:
    """Search statistics for a specific recipient."""
    return self.connection.env['mail.mail.statistics'].search([
        ('recipient', '=', email)
    ])

def search_statistics_ids_by_date_range(self, start_date: datetime, end_date: datetime) -> List[MailingStatistic]:
    """Search statistics within a date range."""
    return self.connection.env['mail.mail.statistics'].search([
        ('sent', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_statistics_by_ids(self, stat_ids: List[int]) -> List[MailingStatistic]:
    """Fetch mailing statistics by IDs."""
    return [{
        'id': stat['id'],
        'mass_mailing_id': stat['mass_mailing_id'][0] if isinstance(stat['mass_mailing_id'], (list, tuple)) else stat['mass_mailing_id'],
        'model': stat['model'],
        'res_id': stat['res_id'],
        'recipient': stat['recipient'],
        'sent': stat['sent'],
        'opened': stat['opened'],
        'clicked': stat['clicked'],
        'bounced': stat['bounced'],
        'exception': stat['exception']
    } for stat in self.connection.env['mail.mail.statistics'].read(
        stat_ids,
        ['mass_mailing_id', 'model', 'res_id', 'recipient', 'sent', 'opened', 'clicked', 'bounced', 'exception']
    )]

def search_contact_ids_by_email(self, email: str) -> List[int]:
    """Search for mailing list contacts by email."""
    return self.connection.env['mail.mass_mailing.contact'].search([
        ('email', '=', email)
    ])

def fetch_contacts_by_ids(self, contact_ids: List[int]) -> List[MailingContact]:
    """Fetch mailing list contact details."""
    return [{
        'id': contact['id'],
        'name': contact['name'],
        'email': contact['email'],
        'list_ids': contact['list_ids'],
        'unsubscribed': contact['unsubscribed'],
        'opt_out': contact['opt_out']
    } for contact in self.connection.env['mail.mass_mailing.contact'].read(
        contact_ids,
        ['name', 'email', 'list_ids', 'unsubscribed', 'opt_out']
    )]


def get_mailing_open_rates(self, mailing_id: int) -> dict:
    """Get open rate statistics for a specific mailing."""
    stats = fetch_statistics_by_mailing_id(self, mailing_id)
    total = len(stats)
    opened = len([s for s in stats if s['opened']])
    bounced = len([s for s in stats if s['bounced']])
    clicked = len([s for s in stats if s['clicked']])

    return {
        'total_sent': total,
        'total_opened': opened,
        'total_bounced': bounced,
        'total_clicked': clicked,
        'open_rate': (opened / total * 100) if total > 0 else 0,
        'bounce_rate': (bounced / total * 100) if total > 0 else 0,
        'click_rate': (clicked / total * 100) if total > 0 else 0
    }
