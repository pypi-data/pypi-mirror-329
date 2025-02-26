
.. _api:

API Reference
/////////////////


Fields
-------

- :py:class:`~data.core.fieldlist.Field`
- :py:class:`~data.core.fieldlist.FieldList`


Metadata
----------

- :py:class:`~data.core.metadata.Metadata`
- :py:class:`~data.core.metadata.RawMetadata`
- :py:class:`~data.readers.grib.metadata.GribMetadata`
- :py:class:`~data.readers.grib.metadata.GribFieldMetadata`
- :py:class:`~data.readers.grib.metadata.StandAloneGribMetadata`

Numpy fields
---------------
- :py:class:`~data.sources.numpy_list.NumpyField`
- :py:class:`~data.sources.numpy_list.NumpyFieldList`

GRIB
-------

- :py:class:`~data.readers.grib.index.GribFieldList`
- :py:class:`~data.readers.grib.codes.GribField`

BUFR
-----

- :py:class:`~data.readers.bufr.bufr.BUFRList`
- :py:class:`~data.readers.bufr.bufr.BUFRMessage`

CSV
----

- :py:class:`~data.readers.csv.CSVReader`

Xarray engine
--------------
- :py:class:`~data.utils.xarray.engine.EarthkitBackendEntrypoint`

Other
--------

- :py:class:`~data.utils.bbox.BoundingBox`
