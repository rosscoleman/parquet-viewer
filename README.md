Cross-platform viewer for Apache Parquet files using Qt for Python.

This is currently just a proof of concept.

This is useful for Parquet files that are small enough to fit on local storage for a workstation or laptop.

TODO:
* Package as stand-alone Windows and Mac executables.
* Handle Windows and Mac file associations. (Double click file to open.)
  * KDE plasma?
  * GNOME3?

Possible enhancements:
* Read Parquet files in chunks as you scoll, for files that fit on disk but not in RAM.
  * On the other hand, are these so big that a metadata viewer and summary statistics are all that make sense?
* Sort by clicking on a column header
  * Harder if we only load chunks into RAM at a time.
* Support Apache Feather files