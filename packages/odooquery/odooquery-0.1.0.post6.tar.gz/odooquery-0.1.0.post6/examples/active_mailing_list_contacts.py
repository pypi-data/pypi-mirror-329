#!/usr/bin/env python

"""
This script demonstrates how to list contats from a mailing list that
have opened any email from the list within a set amount of time.
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta
from typing import List
import os

from odooquery import OdooQuery

def main():
    odoo = None

    try:
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Get the Odoo server URL, database name, and user credentials from
        # environment variables, or prompt the user to enter them manually.
        odoo_url = os.environ.get("ODOO_URL")
        odoo_db = os.environ.get("ODOO_DB")
        odoo_user = os.environ.get("ODOO_USER")
        odoo_password = os.environ.get("ODOO_PASSWORD")

        if not all([odoo_url, odoo_db, odoo_user, odoo_password]):
            raise EnvironmentError("Please set the ODOO_URL, ODOO_DB, ODOO_USER, and ODOO_PASSWORD environment variables.")

        # Create an OdooQuery instance
        odoo = OdooQuery(odoo_url, odoo_db, odoo_user, odoo_password)

        # Connect to the Odoo server
        odoo.connect()

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        if odoo:
            # Close the Odoo connection
            odoo.disconnect()
