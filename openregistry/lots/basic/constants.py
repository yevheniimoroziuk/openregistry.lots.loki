# -*- coding: utf-8 -*-

STATUS_CHANGES = {
    "draft": {
        "deleted": ["lot_owner", "Administrator"],
        "waiting": ["lot_owner", "Administrator"],
    },
    "deleted": {

    },
    "waiting": {
        "invalid": ["bot1", "Administrator"],
        "active.pending": ["bot1", "Administrator"],
    },
    "invalid": {

    },
    "active.pending": {
        "dissolved": ["lot_owner", "Administrator"],
        "active.inauction": ["bot2", "Administrator"],
    },
    "dissolved": {

    },
    "active.inauction": {
        "active.pending": ["bot2", "Administrator"],
        "sold": ["bot2", "Administrator"],
    },
    "sold": {

    },
}

TERMINATED_STATUSES = ["deleted", "sold", "dissolved"]
