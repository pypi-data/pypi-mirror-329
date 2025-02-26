from typing import List
from datetime import datetime
from .types import MailingStatistic, MailingContact, MassMailing

def search_mailing_ids_by_subject(self, subjects: List[str]) -> List[int]:
    """Search for mass mailings by subjects."""
    return self.connection.env['mail.mass_mailing'].search([
        ('subject', 'ilike', subjects)
    ])

def search_mailing_ids_by_date_range(self, start_date: datetime, end_date: datetime) -> List[int]:
    """Search for mass mailings within a date range."""
    return self.connection.env['mail.mass_mailing'].search([
        ('sent_date', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent_date', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_mailings_by_id(self, mailing_ids: List[int]) -> List[MassMailing]:
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

def search_statistics_ids_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingStatistic]:
    """Search statistics for specific mass mailings."""
    return self.connection.env['mail.mail.statistics'].search([
        ('mass_mailing_id', 'in', mailing_ids)
    ])

def search_statistics_ids_by_recipient(self, emails: List[str]) -> List[MailingStatistic]:
    """Search statistics for specific recipients."""
    return self.connection.env['mail.mail.statistics'].search([
        ('recipient', 'in', emails)
    ])

def search_statistics_ids_by_date_range(self, start_date: datetime, end_date: datetime) -> List[MailingStatistic]:
    """Search statistics within a date range."""
    return self.connection.env['mail.mail.statistics'].search([
        ('sent', '>=', start_date.strftime('%Y-%m-%d %H:%M:%S')),
        ('sent', '<=', end_date.strftime('%Y-%m-%d %H:%M:%S'))
    ])

def fetch_statistics_by_id(self, stat_ids: List[int]) -> List[MailingStatistic]:
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

def search_contact_ids_by_email(self, emails: List[str]) -> List[int]:
    """Search for mailing list contacts by emails."""
    return self.connection.env['mail.mass_mailing.contact'].search([
        ('email', 'in', emails)
    ])

def search_contact_ids_by_mailing_id(self, mailing_ids: List[int]) -> List[int]:
    """Search for mailing list contacts for specific mass mailings."""
    return self.connection.env['mail.mass_mailing.contact'].search([
        ('mass_mailing_id', 'in', mailing_ids)
    ])

def fetch_contacts_by_id(self, contact_ids: List[int]) -> List[MailingContact]:
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


# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_mailings_by_subject(self, subjects: List[str]) -> List[MassMailing]:
    """Fetch mass mailings by subjects."""
    return self.fetch_mailings_by_id(self.search_mailing_ids_by_subject(subjects))

def fetch_mailings_by_date_range(self, start_date: datetime, end_date: datetime) -> List[MassMailing]:
    """Fetch mass mailings within a date range."""
    return self.fetch_mailings_by_id(self.search_mailing_ids_by_date_range(start_date, end_date))

def fetch_statistics_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingStatistic]:
    """Fetch mailing statistics for specific mass mailings."""
    return self.fetch_statistics_by_id(self.search_statistics_ids_by_mailing_id(mailing_ids))

def fetch_statistics_by_recipient(self, emails: List[str]) -> List[MailingStatistic]:
    """Fetch mailing statistics for specific recipients."""
    return self.fetch_statistics_by_id(self.search_statistics_ids_by_recipient(emails))

def fetch_statistics_by_date_range(self, start_date: datetime, end_date: datetime) -> List[MailingStatistic]:
    """Fetch mailing statistics within a date range."""
    return self.fetch_statistics_by_id(self.search_statistics_ids_by_date_range(start_date, end_date))

def fetch_contacts_by_email(self, emails: List[str]) -> List[MailingContact]:
    """Fetch mailing list contacts by emails."""
    return self.fetch_contacts_by_id(self.search_contact_ids_by_email(emails))

def fetch_contacts_by_mailing_id(self, mailing_ids: List[int]) -> List[MailingContact]:
    """Fetch mailing list contacts for specific mass mailings."""
    return self.fetch_contacts_by_id(self.search_contact_ids_by_mailing_id(mailing_ids))
