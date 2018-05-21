.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Documents, Attachment, File, Notice, Bidding Documents, Technical Specifications, Evaluation Criteria, Clarifications

.. _Documents:

Documents
=========

Schema
------

:id:
    string, auto-generated

:documentType:
    string, required

    Type of the document.

    Possible values are:

    * `notice` - Lot Notice
    
    The formal notice that gives details. This may be a link to a downloadable document, to a web page, or to an official gazette in which the notice is contained.

    * `technicalSpecifications` - Technical Specifications
    
    Detailed technical information about goods or services to be provided.

    * `illustration` - Illustrations

    * `x_presentation` - Presentation

    Presentation about the lot to be sold.

    * `informationDetails` - Information Details

    Auto-generated type of document that will be attached to each of the lot automatically.

    * `cancellationDetails` - Cancellation Details

    Reasons why the lot has to be deleted.
    
:title:
    string, multilingual, required
    
    |ocdsDescription|
    The document title. 
    
:description:
    string, multilingual
    
    |ocdsDescription|
    A short description of the document. In the event the document is not accessible online, the description field can be used to describe arrangements for obtaining a copy of the document.
    
:format:
    string, optional
    
    |ocdsDescription|
    The format of the document taken from the `IANA Media Types code list <http://www.iana.org/assignments/media-types/>`_, with the addition of one extra value for 'offline/print', used when this document entry is being used to describe the offline publication of a document. 
    
:url:
    string, auto-generated
    
    |ocdsDescription|
    Direct link to the document or attachment. 
    
:datePublished:
    string, :ref:`date`, auto-generated
    
    |ocdsDescription|
    The date on which the document was first published. 
    
:dateModified:
    string, :ref:`date`, auto-generated
    
    |ocdsDescription|
    Date that the document was last modified
    
:language:
    string, optional
    
    |ocdsDescription|
    Specifies the language of the linked document using either two-digit `ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_, or extended `BCP47 language tags <http://www.w3.org/International/articles/language-tags/>`_. 

:documentOf:
    string, required

    Possible values are:

    * `lot`
    * `item`

:relatedItem:
    string, optional

    Id of related :ref:`Lot` or :ref:`item`.

:index:
    integer, optional

    |ocdsDescription|
    Sorting (display order) parameter used for illustrations. The smaller number is, the higher illustration is in the sorting. If index is not specified, illustration will be displayed the last. If two illustrations have the same index, they will be sorted depending on their publishing date.

:accessDetails:
    string, optional