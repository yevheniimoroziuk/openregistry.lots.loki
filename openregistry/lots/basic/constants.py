# -*- coding: utf-8 -*-

STATUS_CHANGES = {
    "draft": {
        "deleted": "lot_owner",
        "waiting": "lot_owner",
    },
    "deleted": {

    },
    "waiting": {
        "invalid": "bot",
        "active.pending": "bot",
    },
    "invalid": {

    },
    "active.pending": {
        "dissolved": "lot_owner",
        "active.inauction": "bot",
    },
    "dissolved": {

    },
    "active.inauction": {
        "active.pending": "bot",
        "sold": "bot",
    },
    "sold": {

    },
}
