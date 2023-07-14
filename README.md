Cross-platform viewer for Apache Parquet files using Qt for Python.

This is currently just a proof of concept. It would also be useful to have a cross-platform GUI to view metatadata for a Parquet file. Would the same application do both?

This is useful for Parquet files that are small enough to fit on local storage for a workstation or laptop. For remote storage, network latency and throughput would matter a lot.

TODO:
* Package as stand-alone Windows and Mac executables.
* Handle Windows and Mac file associations. (Double click file to open.)
  * KDE plasma?
  * GNOME3?

Possible enhancements:
* Read Parquet files in chunks as you scoll, for files that fit on disk but not in RAM.
  * On the other hand, are these so big that a metadata viewer and summary statistics are all that make sense?
* Column sorting and filtering
* Support Apache Feather files
* Metadata viewer:
  * https://parquet.apache.org/docs/file-format/metadata/
  * Compression algorithm
  * Total number of rows
  * Column chunk size or number of chunks
  * Column names
  * Column types
  * Number of NULLs in a Column
  * Summary Statistics by Column