.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Lot, Period, Date 

.. _lot:

Lot
===============

Schema
------

:id:
    string, auto-generated, read-only
    
:lotID:
   string, auto-generated, read-only

   The lot identifier to refer that lot to in the `paper` documentation. 

   |ocdsDescription|
   LotID is included to make the flattened data structure more convenient.
   
:date:
    string, auto-generated, read-only
    
    The date of lot creation/undoing.
    
:dateModified:    
    string, auto-generated, read-only
    
    |ocdsDescription|
    Date when the lot was last modified.
    
:rectificationPeriod:
    :ref:`Period`, auto-generated, read-only

    Period during which the lot's owner can edit it.

:status:
    string, required
    
    The lot status within the Registry.

:assets:
    string, optional
    
    id of the related asset.

:title:
    string, multilingual, auto-generated
    
    Originates from `asset.title`.

:description:
    string, multilingual, auto-generated
    
    |ocdsDescription|
    A description of the goods, services to be provided.
    
    Originates from `asset.description`.
    
:decisions:
    Array of :ref:`Decisions`, auto-generated, required

    Also include the decision from `asset.decisions <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/standard/asset.html#decisions>`_.
    
:lotCustodian:
   :ref:`Organization`, auto-generated

   An entity managing the lot. Originates from `asset.assetCustodian <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/standard/organization.html#organization>`_.

:items:
    :ref:`Item`, auto-generated

    Originates from `asset.items <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/standard/item.html>`_.

:lotHolder:
   :ref:`lotHolder`, auto-generated

   Originates from `asset.assetHolder <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/standard/assetHolder.html>`_.

:auctions:
    :ref:`Auctions`, required

    Auction conditions due to which the lot is to be sold.

:mode:
    optional

    The additional parameter with a value `test`.

:lotType:
    string, auto-generated, read-only

    Type of the given lot.

.. _period:    

Period
=======    

Schema
------

:startDate:
    string, :ref:`Date`

    |ocdsDescription|
    The start date for the period.
    `startDate` should always precede `endDate`.

:endDate:
    string, :ref:`Date`

    |ocdsDescription|
    The end date for the period.

.. _date:

Date
====

Date/time in `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601#Dates>`_.


.. _value:

Value
===============

Schema
------

:amount:    
    float, required

    Should be positive.
    
:currency:
    string, required
    
    |ocdsDescription|
    The currency in 3-letter ISO 4217 format.
    
:valueAddedTaxIncluded:
    bool, required

