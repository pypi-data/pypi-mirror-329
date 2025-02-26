.. image:: https://img.shields.io/pypi/v/collective.formsupport.counter.svg
    :target: https://pypi.python.org/pypi/collective.formsupport.counter/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.formsupport.counter.svg
    :target: https://pypi.python.org/pypi/collective.formsupport.counter
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.formsupport.counter.svg?style=plastic
    :target: https://pypi.python.org/pypi/collective.formsupport.counter/
    :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.formsupport.counter.svg
    :target: https://pypi.python.org/pypi/collective.formsupport.counter/
    :alt: License

.. image:: https://coveralls.io/repos/github/collective/collective.formsupport.counter/badge.svg
    :target: https://coveralls.io/github/collective/collective.formsupport.counter
    :alt: Coverage


==============================
collective.formsupport.counter
==============================

Counter integration for `collective.volto.formsupport <https://github.com/collective/collective.volto.formsupport>`_

Features
--------

- Form counter for `collective.volto.formsupport <https://github.com/collective/collective.volto.formsupport>`_ >= 3.2


Installation
------------

Install collective.formsupport.counter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.formsupport.counter


and then running ``bin/buildout``

REST API
========
-------------------------------------------
🔄 Reset Form Counter
-------------------------------------------

Reset the counter for a specific form block.

**Endpoint:**

.. code-block:: text

    /<document>/@counter

**Method:**

``PATCH``

**Parameters:**

- ``block_id`` *(optional)* — The identifier of the form block, if not passed, the first available formblock selected.
- ``counter_value`` *(optional)* — The value to set the counter to (default: 0).

**Description:**

This endpoint resets the form counter to a specified value.

**Request Example:**

.. code-block:: http

    PATCH /my-document/@counter
    Content-Type: application/json

    {
        "block_id": "form_block_123",
        "counter_value": 5
    }

**Response:**

- **Status Code:** ``204 No Content``

  The response indicates that the counter has been successfully reset. No response body is returned.

-------------------------------------------
📊 Get Counter Value
-------------------------------------------

Retrieve the current counter value for a specific form block.

**Endpoint:**

.. code-block:: text

    /<document>/@counter

**Method:**

``GET``

**Parameters:**

- ``block_id`` *(optional)* — The identifier of the form block. The first available is being selected if not passed.

**Description:**

This endpoint retrieves the current value of the form counter.

**Request Example:**

.. code-block:: http

    GET /my-document/@counter?block_id=form_block_123
    Accept: application/json

**Response:**

- **Status Code:** ``200 OK``

- **Response Body:**

.. code-block:: json

    {
        "counter_value": 5
    }


Authors
-------

RedTurtle


Contributors
------------

- folix-01

Contribute
----------

- Issue Tracker: https://github.com/collective/collective.formsupport.counter/issues
- Source Code: https://github.com/collective/collective.formsupport.counter
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: info@redturtle.it


License
-------

The project is licensed under the GPLv2.
