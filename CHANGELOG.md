v0.3.1
======

* Implement conversion of the `LIKE n BUT` syntax (fixes [issue
  #26](https://github.com/arekfu/t4_geom_convert/issues/26))
* Implement conversion of hexagonal lattices (`LAT=2`, fixes [issue
  #22](https://github.com/arekfu/t4_geom_convert/issues/22))
* Implement conversion of macrobodies (fixes [issue
  #25](https://github.com/arekfu/t4_geom_convert/issues/25))
* Add a command-line option (-e) to specify the encoding of the input file
  (fixes [issue #27](https://github.com/arekfu/t4_geom_convert/issues/27))
* Handle the MCNP data card shortcuts (`14R`, `J`, `I`, etc., fixes [issue
  #24](https://github.com/arekfu/t4_geom_convert/issues/24))
* Support importance keywords for multiple particles
* Support "message:" MCNP cards
* Support affine transformations with 13 parameters
* Improve error message on TatSu parse errors (partially fixes [issue
  #23](https://github.com/arekfu/t4_geom_convert/issues/23))
* Add integration tests with MCNP and Oracle (fixes [issue
  #6](https://github.com/arekfu/t4_geom_convert/issues/6))
* Add documentation for the Oracle tooling
* Add a message with the list of the cells that were skipped during the
  conversion
* Bug fixes:
  - Fix parsing of consecutive complement operators (`#1#2`, fixes [issue
    #33](https://github.com/arekfu/t4_geom_convert/issues/33))
  - Fix handling of TRCL keyword on cells defined using the complement operator
    (fixes [issue #32](https://github.com/arekfu/t4_geom_convert/issues/32))
  - Fix several issues with line continuations (fixes [issue
    #29](https://github.com/arekfu/t4_geom_convert/issues/29))
  - Fix parsing of input files without a newline at the end (fixes [issue
    #28](https://github.com/arekfu/t4_geom_convert/issues/28))
  - Fix conversion of material cards containing keywords (ntab, ptab, etc.)
* Lots of refactoring and cleaning

v0.2.0
======

* Support conversion of planes defined by three points (fixes [issue
  #1](https://github.com/arekfu/t4_geom_convert/issues/1)).
* Add support for 0 as a cone sheet specifier (fixes [issue
  #2](https://github.com/arekfu/t4_geom_convert/issues/2)).
* Add support for elliptic tori in MIP (fixes [issue
  #3](https://github.com/arekfu/t4_geom_convert/issues/3)).
* Handle the specification of `FILL` transformations by ID (fixes [issue
  #4](https://github.com/arekfu/t4_geom_convert/issues/4)).
* Partially handle conversion of lattices in fully-specified form (fixes [issue
  #16](https://github.com/arekfu/t4_geom_convert/issues/16)).
* Fix parsing of cell card options starting with `*FILL` in MIP.
* Fix detection of line continuation.
* Preserve the precision of isotope concentrations in the MCNP file.
* Make pytest runnable from the package root directory.
* Fix conversion of materials specified by density and atomic fractions (fixes
  [issue #8](https://github.com/arekfu/t4_geom_convert/issues/8)).
* Fix conversion of materials specified by total atomic concentration and
  atomic fractions (fixes [issue
  #14](https://github.com/arekfu/t4_geom_convert/issues/14)).
* Support spaces between the # operator and its arguments (fixes [issue
  #10](https://github.com/arekfu/t4_geom_convert/issues/10)).
* Handle the conversion of cards with a TRCL keyword (fixes [issue
  #21](https://github.com/arekfu/t4_geom_convert/issues/21)).
* Remove duplicated surfaces (fixes [issue
  #19](https://github.com/arekfu/t4_geom_convert/issues/19)).
* Do not use fixed IDs for the helper surface used in UNION cells (fixes [issue
  #15](https://github.com/arekfu/t4_geom_convert/issues/15)).
* Do not emit TRIPOLI-4 cells where the same surface appears twice.
* Some linting and refactoring.


v0.1.4
======

* First public release
