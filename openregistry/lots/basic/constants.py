# -*- coding: utf-8 -*-

STATUS_CHANGES = {
    "draft": {
        "editing_permissions": ["lot_owner", "Administrator"],
        "next_status": {
            "pending": ["lot_owner", "Administrator"],
        }
    },
    "pending": {
        "editing_permissions": ["lot_owner", "Administrator"],
        "next_status": {
            "draft": ["Administrator"],
            "deleted": ["lot_owner", "Administrator"],
            "verification": ["lot_owner", "Administrator"]
        }
    },
    "deleted": {
        "editing_permissions": [],
        "next_status": {}
    },
    "verification": {
        "editing_permissions": ["concierge", "Administrator"],
        "next_status": {
            "pending": ["concierge", "Administrator"],
            "active.salable": ["concierge", "Administrator"]
        }
    },
    "active.salable": {
        "editing_permissions": ["convoy", "Administrator", "lot_owner"],
        "next_status": {
            "dissolved": ["lot_owner", "Administrator"],
            "active.awaiting": ["convoy", "Administrator"],
            "verification": ["Administrator"]
        }
    },
    "dissolved": {
        "editing_permissions": [],
        "next_status": {}
    },
    "active.awaiting": {
        "editing_permissions": ["convoy", "Administrator"],
        "next_status": {
            "active.auction": ["convoy", "Administrator"],
            "active.salable": ["convoy", "Administrator"]
        }
    },
    "active.auction": {
        "editing_permissions": ["convoy", "Administrator"],
        "next_status": {
            "active.salable":  ["Administrator"],
            "sold": ["convoy", "Administrator"]
        }
    }
}
