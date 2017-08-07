# -*- coding: utf-8 -*-

STATUS_CHANGES = {
    "draft": {
        "deleted": "lot_owner",
        "waiting": "lot_owner",
    },
    "deleted": {

    },
    "waiting": {
        "invalid": "bot1",
        "active.pending": "bot1",
    },
    "invalid": {

    },
    "active.pending": {
        "dissolved": "lot_owner",
        "active.inauction": "bot2",
    },
    "dissolved": {

    },
    "active.inauction": {
        "active.pending": "bot2",
        "sold": "bot2",
    },
    "sold": {

    },
}
