# -*- coding: utf-8 -*-

LOT_STATUSES = ["draft", "pending", "deleted"]

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
            "deleted": ["lot_owner", "Administrator"]
        }
    },
    "deleted": {
        "editing_permissions": [],
        "next_status": {}
    },
}

DOCUMENT_TYPES = [
    'notice', 'technicalSpecifications', 'illustration', 'virtualDataRoom',
    'x_presentation', 'x_dgfAssetFamiliarization', 'procurementPlan', 'projectPlan'
]
