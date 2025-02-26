from typing import List
from .types import Message
from .utils.text_processing import strip_html as _strip_html

def fetch_messages_by_id(self, message_ids: List[int]) -> List[Message]:
    messages = self.connection.env['mail.message'].read(message_ids, ['id', 'attachment_ids','author_id','body','date','subtype_id','is_internal','description','message_type','needaction'])

    return [{
        'id': message['id'],
        'date': message['date'],
        'body': message['body'],  # Strip HTML from body
        'author_id': message['author_id'][0] if isinstance(message['author_id'], (list, tuple)) else message['author_id'],
        'author_name': message['author_id'][1] if isinstance(message['author_id'], (list, tuple)) else '',
        'subtype_id': message['subtype_id'][0] if isinstance(message['subtype_id'], (list, tuple)) else message['subtype_id'],
        'subtype_name': message['subtype_id'][1] if isinstance(message['subtype_id'], (list, tuple)) else '',
        'attachment_ids': message['attachment_ids'],
        'is_internal': message['is_internal'],
        'description': _strip_html(message['description']),  # Strip HTML from description
        'message_type': message['message_type'],
        'needaction': message['needaction']
    } for message in messages]