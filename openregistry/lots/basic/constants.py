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
        "editing_permissions": ["bot1", "Administrator"],
        "next_status": {
            "pending": ["bot1", "Administrator"],
            "active.salable": ["bot1", "Administrator"]
        }
    },
    "active.salable": {
        "editing_permissions": ["bot2", "Administrator", "lot_owner"],
        "next_status": {
            "dissolved": ["lot_owner", "Administrator"],
            "active.awaiting": ["bot2", "Administrator"],
            "verification": ["Administrator"]
        }
    },
    "dissolved": {
        "editing_permissions": [],
        "next_status": {}
    },
    "active.awaiting": {
        "editing_permissions": ["bot2", "Administrator"],
        "next_status": {
            "active.auction": ["bot2", "Administrator"],
            "active.salable": ["bot2", "Administrator"]
        }
    },
    "active.auction": {
        "editing_permissions": ["bot2", "Administrator"],
        "next_status": {
            "active.salable":  ["Administrator"],
            "sold": ["bot2", "Administrator"]
        }
    }
}
