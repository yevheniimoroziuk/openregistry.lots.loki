.. _tutorial:

Tutorial
========

Exploring basic rules
---------------------

Let's try exploring the `/lots` endpoint:

**************************************

Just invoking it reveals empty set.

Now let's attempt creating a lot:

*******************************************

Error states that the only accepted Content-Type is `application/json`.

Let's satisfy the Content-type requirement:

*********************************

Error states that no `data` has been found in JSON body.


.. index:: Lot

Creating lot
------------


Let's create lot with the minimal (only required) data set:

**************************************

**************************************

**************************************

Success! Now we can see that new object was created. Response code is `201`
and `Location` response header reports the location of the created object.  The
body of response reveals the information about the created lot: its internal
`id` (that matches the `Location` segment), its official `lotID` and
`dateModified` datestamp stating the moment in time when lot was last
modified. Note that lot is created with `pending` status.

Let's access the URL of the created object (the `Location` header of the response):

**************************************

.. XXX body is empty for some reason (printf fails)

We can see the same response we got after creating lot.

**************************************

Let's see what listing of lots reveals us:


We do see the internal `id` of the lot (that can be used to construct full URL by prepending `**************************************`) and its `dateModified` datestamp.

The previous lot contained only required fields. Let's try creating lot with more data:

**************************************

**************************************

.. XXX patching lot to pending.dissolution

**************************************

And again we have `201 Created` response code, `Location` header and body with extra `id`, `lotID`, and `dateModified` properties.

Let's check what lot registry contains:

**************************************

And indeed we have 2 lots now.



Modifying Lot
-------------

Time for the lot to be modified is `rectificationPeriod`

Let's update lot description:

**************************************

.. XXX body is empty for some reason (printf fails)

We see the added properies have merged with existing lot data. Additionally, the `dateModified` property was updated to reflect the last modification datestamp.

Checking the listing again reflects the new modification date:

**************************************

Deleting Lot
------------

Let's delete lot:

**************************************

Integration with assets
-----------------------


Concierge operations
--------------------

For lot to be formed, you need to specify id of the asset to be included 
in that lot. If this assets is available, it will be attached to lot 
and status of a lot itself will be changed to `pending`:

**************************************

In case of this assets is unavailable (e.g. it has already been 
attached to another lot), status of the current lot will be turned to `invalid`:

**************************************

When bot finds that status of lot is `pending.dissolution`, it
turns status of the asset being attached to that lot to `pending`. Status of the lot itself will become `dissolved`.
   
**************************************

**************************************

When bot finds that status of lot is `pending.sold`, it
turns status of the asset being attached to that lot to `complete`. Status of the lot itself
turns to `sold`.


**************************************
   
Convoy operations
-----------------

When lot is finally formed, owner switches its status to `active.salable` so that the lot can be used in the
procedure. 
For the procedure to be created, you need to specify lot id. 
By doing this, you will find the `merchandisingObject` field with the current 
lot id in the created procedure and id of the auction within which 
it is going to be sold. Status of the lot used will be automatically changed 
to `active.awaiting` in the Registry. This indicates that Organizer is creating some auction with
this lot within CDB, so it is currently unavailable for usage.

**************************************

When the procedure is successfully created, lot status will be changed to 
`active.auction`: 


**************************************


In case of that lot has not been sold, its status will be changed to `pending.dissolution`:

**************************************

When contract has been successfully created within the Module of Contracting, lot's status turns to `active.contracting`:

**************************************

When contract reaches status: terminated, lot becomes `pending.sold`:

**************************************

In case of that contracts is `unsuccessul`, status of lot turns to `pending.dissolution`:

