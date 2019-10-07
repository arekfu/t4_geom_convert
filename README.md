t4_geom_convert
===============

[![PyPI version](https://badge.fury.io/py/t4-geom-convert.svg)](https://badge.fury.io/py/t4-geom-convert)

This repository contains the development version of `t4_geom_convert`, a Python
tool to convert [MCNP] geometries into the [TRIPOLI-4®] format.

Features
--------

Here is a list of features of the MCNP modelling engine that are
at least partially supported and converted by `t4_geom_convert`:

* All surface types (except SQ)
* Boolean cell operators
* Affine transformations on surfaces and on cells (see the [Current
  limitations](#current-limitations) section though)
* Boundary conditions (reflection, white surfaces)
* Isotopic compositions and cell densities
* Universes and fills, even nested, possibly with affine transformations
* [Lattices](#lattice-conversion) (see the [Current
  limitations](#current-limitations) section though)


Installation
------------

If you want to install the latest stable version, just type the following
command in a terminal:

```
$ pip3 install t4_geom_convert
```

You can also install the latest development version with

```
$ pip3 install git+https://github.com/arekfu/t4_geom_convert.git@next
```

You might want to pass the `--user` option to `pip3` for a local install. Even
better, you can create a virtual environment and install `t4_geom_convert`
there with

```
$ python3 -m venv /path/to/some/folder
$ source /path/to/some/folder/bin/activate
$ pip3 install -U pip setuptools
$ pip3 install t4_geom_convert
```

### Dependencies

The MCNP input file is parsed by [MIP]. We use a slightly modified version of
MIP, which is shipped along with `t4_geom_convert`. MIP depends on [TatSu]
4.3.0.

`t4_geom_convert` also depends on `numpy`.


Usage
-----

The basic usage is simply

```
$ t4_geom_convert <mcnp_input>
```

This will create a TRIPOLI-4 output file called `<mcnp_input>.t4` containing
the converted geometry.  You can also choose a different name for the output
file using the `-o` option.

Use the `-h` option for a list of all available options.

### Lattice conversion

`t4_geom_convert` is capable of handling the conversion of repeated structures
(lattices). Only hexaedral lattices (`LAT=1`) are supported for the moment.

A hexaedral cell declared as `LAT=1` represents the unit cell of the lattice,
which is assumed to repeat in all directions up to the boundaries of the
enclosing cell. Due to limitations of the TRIPOLI-4 representation of lattices,
we have chosen to represent lattices using a purely surface-based approach.
This means that `t4_geom_convert` will actually emit separate cell definitions
for each cell of the lattice that is visible through the enclosing cell. The
ranges of cell definitions to be emitted must be specified by the user via the
`--lattice` command-line option. For instance, consider the following MCNP
input:

```
A lattice example
1 0  1 -2 3 -4 IMP:N=1 U=2 LAT=1
10 1 -1. -10 IMP:N=1 FILL=2
1000 0 10 IMP:N=0

1 PX -1.5
2 PX 1.5
3 PY -0.5
4 PY 0.5
10 SO 4

m1 13027 1.
```

Here the unit cell is two-dimensional. The lattice fills a sphere of radius
4.  Assuming the unit cell is indexed as (0,0), the visible lattice cells are
* (-1, -4) to (-1, 4)
* (0, -4) to (0, 4)
* (1, -4) to (1, 4)

This can be confirmed by visual inspection of the MCNP geometry or by
geometrical considerations. Once the index bounds are determined, the
`--lattice` option must be specified as

```
$ t4_geom_convert --lattice 1,-1:1,-4:4 <mcnp_input>
                            ↑  ↑ ↑  ↑ ↑
             cell number ───┘  │ │  │ └ j-range upper bound
        i-range lower bound ───┘ │  └─── j-range lower bound
          i-range upper bound ───┘
```

This results in the following TRIPOLI-4 geometry (X-Y cut), where a few cell
indices have been annotated:
![example of converted geometry with lattices][lattice_example]

The syntax for one-dimensional lattices is

```
--lattice <cell>,<i-from>:<i-to>
```

and for three-dimensional lattices it is

```
--lattice <cell>,<i-from>:<i-to>,<j-from>:<j-to>,<k-from>:<k-to>
```

Note that the `ijk` axes are not necessarily the same as the coordinate axes.

A lattice unit cell may appear as a fill pattern in several enclosing cells. It
is currently not possible to specify different fill ranges for each of them.


Current limitations
-------------------

Here is a list of some things that `t4_geom_convert` cannot currently do, but
may be able to do in the future (in roughly decreasing order of likelihood):

- [ ] Convert SQ surfaces (tracked in issue #11)
- [ ] Import the title of the MCNP input file (tracked in issue #5)
- [ ] Handle affine transformations with `m=-1` (the last parameter of the
      affine transformation) (tracked in issue #12)
- [ ] Optimize fills with negative universes (do not intersect with the
      enclosing cell) (tracked in issue #13)
- [ ] Warn about isotopes that are missing from the TRIPOLI-4 dictionary
      (currently you need to edit the converted file by hand and remove the
      occurrences of the missing isotopes)
- [ ] Convert MCNP macrobodies
- [ ] Convert cell temperatures
- [ ] Convert hexagonal lattices
- [ ] Import comments describing the MCNP cells/surfaces (tracked in issue #9)
- [ ] Provide a way to specify lattice fill ranges per enclosing cell(s) (this
      needs to be specified in such a way that it works with nested lattices,
      too)
- [ ] Deduplicate repeated surface definitions, i.e. remove duplicate surface
      definitions in favour of one of the replicas (this is especially an issue
      for lattices, that tend to generate lots of identical surfaces)
- [ ] Deduplicate repeated cell definitions (this is a bit harder than
      deduplicating surfaces)
- [ ] Produce a TRIPOLI-4 connectivity map for as many cells as possible
      (mostly lattices)
- [ ] Recognize and automatically suppress empty cells (they may be generated
      by lattice development or fill development)
  - Use a linear programming solver for cells bounded by planes?
  - Use a SAT solver in the general case?
- [ ] Convert (some) MCNP source definitions
- [ ] Convert (some) MCNP tally definitions

A couple of limitations are due to MIP/TatSu:

- [ ] MIP does not support TatSu>4.3.0 (something breaks, but I'm not sure what
      exactly yet)
- [X] ~~Input files cannot contain unusual or non-ASCII characters such as `&`
      or `é`; you need to remove these characters from your input file before
      attempting the conversion~~

  **Fixed upstream**
- [X] ~~Spaces are not permitted in a cell definition between a complement
      operator `#` and its argument:~~
  - ~~good: `#42`~~
  - ~~good: `#(123 -124)`~~
  - ~~bad: `# 42`~~
  - ~~bad: `# (123 -124)`~~

  **Fixed in issue #10**

Your help is welcome! Feel free to open an issue if you would like to implement
a new feature or contribute to the project in any way.

The full changelog is [here](CHANGELOG.md).


Reporting bugs
--------------

Please report any bug/feature request on [the GitHub issues page][bugs].


Licence and acknowledgments
---------------------------

The development of `t4_geom_convert` was partially financed by the [EUROfusion]
consortium. `t4_geom_convert` is released under the terms of the  [GNU Public
Licence, version 3](COPYING).


[MCNP]: https://mcnp.lanl.gov/
[TRIPOLI-4®]: http://www.cea.fr/nucleaire/tripoli-4
[MIP]: https://github.com/travleev/mip
[TatSu]: https://tatsu.readthedocs.io/en/stable/
[bugs]: https://github.com/arekfu/t4_geom_convert/issues
[EUROfusion]: https://www.euro-fusion.org/
[lattice_example]: pics/lattice_example.png
