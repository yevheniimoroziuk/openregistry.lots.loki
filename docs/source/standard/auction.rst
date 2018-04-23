.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Duration, Value, Guarantee, auctionParameters

.. _auction:

Auction
=======

Schema
------

:id:
  string, auto-generated, read-only

:auctionID:
  string, auto-generated, read-only

  The auction identifier to refer auction to in "paper" documentation. 

  |ocdsDescription|
  AuctionID should always be the same as the OCID. It is included to make the flattened data structure more convenient.
   
:procurementMethodType:
  string, auto-generated, read-only

:auctionPeriod:
  :ref:`period`, required

  Period when the first auction is conducted. Here startDate` should be provided.

:tenderingDuration:
  :ref:`Duration`, required

  Duration of tenderPeriod for 2nd and 3rd procedures within the privatization cycle. 

:documents:
  List of :ref:`document` objects
 
  |ocdsDescription|
  All documents and attachments related to the auction.

:value:
  ref:`value`, required

  Total available budget of the 1st auction. Bids lower than ``value`` will be rejected.

  `Auction.value` for 2nd and 3rd auctions within the privatization cycle will be calculated as half of the `auction.value` provided.

  |ocdsDescription|
  The total estimated value of the procurement.

:guarantee:
  :ref:`Guarantee`, required

  Bid guarantee.

:registrationFee:
  :ref:`Guarantee`, required

  Bid registration fee.

:minimalStep:
  :ref:`value`, required

  The minimal step of the 1st auction. `Auction.minimalStep` for 2nd and 3rd auctions within the privatization cycle will be calculated as half of the `auction.minimalStep` provided.

  Validation rules:

  * `amount` should be greater than `Auction.value.amount`
  * `currency` should either be absent or match `Auction.value.currency`
  * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:auctionParameters:
  :ref: `auctionParameters`, optional

  Parameters for the auction to be held.

:accountDetails:
  :ref:`accountDetails`, optional

  Details which uniquely identify a bank account, and are used when making or receiving a payment.

.. _auctionParameters:

auctionParameters
=================

Schema
------

:type:
  string, auto-generated, read-only

  Type of the auction.

:dutchSteps:
  integer, optional

  Number of steps within the dutch part of the insider auction. 

  Possible values are [1; 100]. Defaul value is 99.

:procurementMethodDetails:

  Parameter that accelerates auction periods. For instance you can set `quick, accelerator=1440`
  as text value for `procurementMethodDetails`. The number 1440 shows that restrictions and time frames 
  will be reduced in 1440 times.

.. _duration:

Duration
========

Duration in `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601#Durations>`_.

.. _value:

Value
=====

Schema
------

:amount:    
  float, required

  Should be positive.

  |ocdsDescription|
  Amount as a number.
    
:currency:
  string, required
    
  |ocdsDescription|
  The currency in 3-letter ISO 4217 format.
    
:valueAddedTaxIncluded:
  bool, required

  Possible values are `true` or `false`.

.. _guarantee:

Guarantee
=========

Schema
------

:amount:    
  float, required

  Should be positive.

  |ocdsDescription|
  Amount as a number.
    
:currency:
  string, required
    
  |ocdsDescription|
  The currency in 3-letter ISO 4217 format.