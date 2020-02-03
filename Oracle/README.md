MCNP/TRIPOLI-4 comparison oracle
================================

This folder contains a few tools to test the equivalence of an MCNP geometry
and a TRIPOLI-4 geometry.

The main tool is called `oracle` and performs the equivalence tests. It writes
a test report to standard output and a list of points that failed the test to
an output file. The output file can subsequently be loaded in TRIPOLI-4's
visualization tool T4G to get a graphical view of the problematic regions.
`oracle` is mainly used as a verification tool for `t4_geom_convert`, but it
can be used in other contexts, too.

When two geometries are found not to be equivalent, sometimes it is difficult
to understand why. A helper tool called `explainT4` can be used to automate
part of the task of figuring out what went wrong.


Principle
---------

Two geometries are considered to be *equivalent* if points with the same
coordinates are associated to the same material in both geometries, with the
possible exception of points within some user-defined tolerance from a
geometrical boundary (surface). Note that this definition does not involve
cells (volumes), but only materials.

The main idea of the `oracle` tool is to use a PTRAC file produced by MCNP as
a collection of results of queries to the MCNP geometry; the PTRAC file
contains information about which material was seen at different locations.  The
advantage of using a PTRAC file is that you do not need to have access to the
MCNP source files in order to query the MCNP geometry.

While a similar strategy could in principle be used to query the TRIPOLI-4
geometry, too, for the moment we have decided to use the TRIPOLI-4 geometry API
directly. It is possible however to envisage that the `oracle` tool may be
decoupled from TRIPOLI-4 and generalized to other geometry engines and
transport codes in the future.

How do we know if the material that we find in the MCNP geometry is the same as
the one that we find in TRIPOLI-4? By default, the `oracle` only checks the
material names. The TRIPOLI-4 materials are expected to follow the same naming
convention as those produced by `t4_geom_convert`. Specifically, if the MCNP
material `m5` appears in a cell with a density of `-2.32`, the corresponding
TRIPOLI-4 material should be called `m5_-2.32`. [There is a
flag](#useful-command-line-options) (`-g`) that changes this behavior.


Requirements
------------

You will need the following software to compile the comparison:

* CMake >=3.2
* a recent version of TRIPOLI-4 (sources included) and its prerequisites

You will also need an MCNP executable to run meaningful tests.


Compilation
-----------

All the tools are written in C++.

First, you need to compile TRIPOLI-4 using the CMake build:

```bash
$ mkdir /path/to/build-t4 /path/to/install-t4
$ cd /path/to/build-t4
$ cmake -DCMAKE_INSTALL_PREFIX=/path/to/install-t4 /path/to/tripoli4-sources
$ make && make install
```

Once TRIPOLI-4 has been installed, you can compile this package:

```bash
$ mkdir /path/to/build-oracle
$ cd /path/to/build-oracle
$ cmake -DT4_DIR=/path/to/install-t4/share/cmake /path/to/t4_geom_convert/Oracle
$ make
```

If all went well, you should find an `oracle` and an `explainT4` executable in
your build directory.


Usage
-----

In order to compare a TRIPOLI-4 and an MCNP geometry, you will need:

* the TRIPOLI-4 input file containing the description of the geometry (say
  `geometry.t4`);
* the MCNP input file (say `geometry.mcnp`)

### Preparing the PTRAC file

The first thing to do is to modify the MCNP input file to generate a suitable
PTRAC file.

1. Comment out the source cards (`SDEF` and friends). Add a new source that
   covers the portion of the geometry that you would like to test (possibly all
   of it). The type and energy of the source particles do not matter: the
   following cards, for instance, produce 14-MeV neutrons in the box `-10 < x <
   1700`, `-575 < y < 575`, `-1460 < z < 1810`:

   ```
   sdef  pos=0 0 0  x=d1  y=d2  z=d3  erg=14
   si1   -10   1700
   sp1   0     1
   si2   -575  575
   sp2   0     1
   si3   -1460 1810
   sp3   0     1
   ```
  
   To speed things up, you may want to kill particles right below the source
   energy:
  
   ```
   cut:n  j  13.9999
   ```
  
   The PTRAC card should look something like this:
  
   ```
   ptrac  file=bin event=src max=-1000000
   ```
  
   Both binary (`file=bin`) and ASCII (`file=asc`) PTRAC file formats are
   supported by the `oracle`, but binary files are recommended (they do not
   drop any precision on the point coordinates, reducing the number of false
   positives). The number of events to be written (`max`) can be adjusted; just
   make sure that you adjust the number of source particles accordingly (`nps`
   card).

2. Run MCNP on the modified input file.


### Running the `oracle`

Let us assume the name of the PTRAC file is `geometry.ptrac`.  Run the `oracle`
as follows:

```bash
$ /path/to/oracle geometry.t4 geometry.mcnp geometry.ptrac
```

This will run the equivalence tests on the points in the PTRAC file. For each
point:

* If the same material was found in the TRIPOLI-4 and MCNP geometry, the point
  is counted as `SUCCESSFUL`.

* If materials are different but the point was within some tolerance distance
  from one of the volume boundaries, the point is counted as `IGNORED`.

* If the materials are different but the point was **not** within the specified
  tolerance, the point is counted as `FAILED`.

* If the point did not fall inside the TRIPOLI-4 geometry, it is counted as
  `OUTSIDE`.

At the end of the run, you will get a report that looks like this:

```
---------------------------
Reporting on MCNP/T4 geometry comparison
-----------------------------
Number of SAMPLED points : 10000
Number of SUCCESSFUL     : 9978 -> 99.78%
Number of FAILED         : 12 -> 0.12%
Number of IGNORED        : 4 -> 0.04%
Number of OUTSIDE        : 6 -> 0.06%
Number of COVERED volumes: 270
Number of INPUT   volumes: 84699
Average distance to surface for FAILED points: 6.41229e-6
Maximum distance to surface for FAILED points: 1.44246e-5
Elapsed time: 1.30655s
Time per point: 0.000130642s
```

Additional statistics are produced for the number of distinct TRIPOLI-4 volumes
that were actually seen by the test, the number of *total* TRIPOLI-4 volumes in
the input file (including `FICTIVE` volumes, though), the average and maximum
distance from a volume boundary for failed points and the elapsed time.

The `oracle` will also produce three output files, called
`geometry.failedpoints.dat`, `geometry.failedpoints.general` and
`geometry.points`, which can be used to view the location of the points that
failed the equivalence test in T4G.


Useful command-line options
---------------------------

Both the `oracle` and `explainT4` executables support the `-h` option for help:

```bash
$ /path/to/oracle -h
 *** MCNP / Tripoli-4 geometry comparison ***

oracle

  Compare MCNP and T4 geometries check that they are weakly equivalent.
  A point is assumed to match by checking the name of the composition at
  that point in each geometry.

USAGE
        oracle [options] jdd.t4 jdd.inp ptrac

INPUT FILES
        jdd.t4 .........................A TRIPOLI-4 input file converted from MCNP INP file.
        jdd.inp ........................The MCNP INP file that was used for the conversion.
        ptrac ..........................The MCNP PTRAC file corresponding to the INP file.

OPTIONS
        -V, --verbose ..................Increase output verbosity.
        -h, --help .....................Displays this help message.
        -n, --npts .....................Maximum number of tested points.
        -d, --delta ....................Distance to the nearest surface below which a failed test is ignored.
        -g, --guess-material-assocs ....guess the materials correspondence based on the first few points
        --binary,---ascii ..............Specify the format of the MCNP PTRAC file
```

Useful options for the `oracle` executable include:

* `-V`: increase the verbosity.

* `-n NPOINTS`: limits the test run to `NPOINTS` points. There is no limit by
  default.

* `-d DELTA`: specifies the geometrical tolerance for ignoring mismatched
  materials near surfaces. Points that are within a distance `DELTA` from a
  volume boundary will be ignored for the purpose of counting the number of
  failed points. Default: `DELTA=1e-7`.

* `--binary` (default), `--ascii`: these options specify the format of the
  PTRAC file.

* `-g`: lets `oracle` guess the mapping between MCNP and TRIPOLI-4 materials,
  instead of assuming `t4_geom_convert`'s naming convention. The correspondence
  will be deduced on the fly: every time a new material is seen on the MCNP
  side, it is assumed that the material seen on the TRIPOLI-4 side is the
  corresponding one. Subsequent occurrences of the same MCNP materials will be
  checked against the TRIPOLI-4 material seen on the first point.


Known bugs and limitations
--------------------------

The oracle needs to do some rudimentary parsing of the MCNP input file. The
parser is not very robust and may choke on unusual spacing, line continuations,
etc.
