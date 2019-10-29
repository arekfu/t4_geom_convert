v0.2.0
======

* Support conversion of planes defined by three points (fixes issue #1).
* Add support for 0 as a cone sheet specifier (fixes issue #2).
* Add support for elliptic tori in MIP (fixes issue #3).
* Handle the specification of `FILL` transformations by ID (fixes issue #4).
* Partially handle conversion of lattices in fully-specified form (fixes issue
  #16).
* Fix parsing of cell card options starting with `*FILL` in MIP.
* Fix detection of line continuation.
* Preserve the precision of isotope concentrations in the MCNP file.
* Make pytest runnable from the package root directory.
* Fix conversion of materials specified by density and atomic fractions (fixes
  issue #8).
* Fix conversion of materials specified by total atomic concentration and
  atomic fractions (fixes issue #14).
* Support spaces between the # operator and its arguments (fixes issue #10).
* Handle the conversion of cards with a TRCL keyword (fixes issue #21).
* Remove duplicated surfaces (fixes issue #19).
* Do not use fixed IDs for the helper surface used in UNION cells (fixes issue
  #15).
* Do not emit TRIPOLI-4 cells where the same surface appears twice.
* Some linting and refactoring.


v0.1.4
======

* First public release
