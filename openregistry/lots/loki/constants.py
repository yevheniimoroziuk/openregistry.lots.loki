# -*- coding: utf-8 -*-
from datetime import timedelta

LOT_STATUSES = [
    "draft", "composing", "pending", "deleted", "active.salable", "active.awaiting", "active.auction",
    "active.contracting", "pending.sold", "pending.dissolution", "sold", "dissolved", "invalid"]

STATUS_CHANGES = {
    "draft": {
        "editing_permissions": ["lot_owner", "Administrator"],
        "next_status": {
            "composing": ["lot_owner", "Administrator"],
        }
    },
    "composing": {
        "editing_permissions": ["Administrator", "concierge"],
        "next_status": {
            "pending": ["concierge", "Administrator"],
            "invalid": ["concierge", "Administrator"],
        }
    },
    "pending": {
        "editing_permissions": ["lot_owner", "Administrator"],
        "next_status": {
            "deleted": ["lot_owner", "Administrator"],
            "active.salable": ["lot_owner", "Administrator"],
        }
    },
    "deleted": {
        "editing_permissions": [],
        "next_status": {}
    },
    "active.salable": {
        "editing_permissions": ["Administrator", "convoy"],
        "next_status": {
            "active.awaiting": ["Administrator", "convoy"]
        }
    },
    "active.awaiting": {
        "editing_permissions": ["Administrator", "convoy"],
        "next_status": {
            "active.salable": ["Administrator", "convoy"],
            "active.auction": ["Administrator", "convoy"]
        }
    },
    "active.auction": {
        "editing_permissions": ["Administrator", "convoy"],
        "next_status": {
            "active.contracting": ["Administrator", "convoy"],
            "pending.dissolution": ["Administrator", "convoy"]
        }
    },
    "active.contracting": {
        "editing_permissions": ["Administrator", "convoy"],
        "next_status": {
            "pending.sold": ["Administrator", "convoy"],
            "pending.dissolution": ["Administrator", "convoy"]
        }
    },
    "pending.sold": {
        "editing_permissions": ["Administrator", "concierge"],
        "next_status": {
            "sold": ["Administrator", "concierge"]
        }
    },
    "pending.dissolution": {
        "editing_permissions": ["Administrator", "concierge"],
        "next_status": {
            "dissolved": ["Administrator", "concierge"]
        }
    },
    "sold": {
        "editing_permissions": [],
        "next_status": {}
    },
    "dissolved": {
        "editing_permissions": [],
        "next_status": {}
    },
    "invalid": {
        "editing_permissions": [],
        "next_status": {}
    },
}

RECTIFICATION_PERIOD_DURATION = timedelta(days=1)
DEFAULT_DUTCH_STEPS = 99