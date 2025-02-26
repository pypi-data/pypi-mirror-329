from typing import List
from .types import Partner

def search_partner_ids_by_email(self, emails: List[str]) -> List[int]:
    """Search for partners by email addresses."""
    return self.connection.env['res.partner'].search([('email', 'in', emails)])

def search_partner_ids_by_name(self, names: List[str]) -> List[int]:
    """Search for partners by names."""
    return self.connection.env['res.partner'].search([('name', 'ilike', names)])

def fetch_partners_by_id(self, partner_ids: List[int]) -> List[Partner]:
    """Fetch partner details."""
    partners = self.connection.env['res.partner'].read(partner_ids, ['id', 'name', 'email', 'phone', 'company_name', 'street', 'city', 'state_id', 'country_id', 'zip'])

    return [{
        'id': partner['id'],
        'name': partner['name'],
        'email': partner['email'],
        'phone': partner['phone'],
        'company_name': partner['company_name'],
        'street': partner['street'],
        'city': partner['city'],
        'state_id': partner['state_id'][0] if isinstance(partner['state_id'], (list, tuple)) else partner['state_id'],
        'state_name': partner['state_id'][1] if isinstance(partner['state_id'], (list, tuple)) else '',
        'country_id': partner['country_id'][0] if isinstance(partner['country_id'], (list, tuple)) else partner['country_id'],
        'country_name': partner['country_id'][1] if isinstance(partner['country_id'], (list, tuple)) else '',
        'zip': partner['zip']
    } for partner in partners]

# Aggregate functions provide higher level functionality by combining multiple lower level functions
def fetch_partners_by_email(self, emails: List[str]) -> List[Partner]:
    """Fetch partner details by email addresses."""
    return self.fetch_partners_by_id(self.search_partner_ids_by_email(emails))

def fetch_partners_by_name(self, names: List[str]) -> List[Partner]:
    """Fetch partner details by names."""
    return self.fetch_partners_by_id(self.search_partner_ids_by_name(names))
