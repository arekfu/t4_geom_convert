/**
 * @file oracle.cc
 * This is the main file for the test Oracle of the converter.
 *
 * @brief contains the main functions of the Oracle program
 *
 * @author J. Faustin
 * @version 1.0
 */

#include "MCNPGeometry.hh"
#include "Statistics.hh"
#include "T4Geometry.hh"
#include "anyvolumes.hh"
#include "compos.hh"
#include "composfromgeom.hh"
#include "geometrytype.hh"
#include "options_compare.hh"
#include "t4convert.hh"
#include "t4coreglob.hh"
#include "volumes.hh"
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <utility>
#include <vector>

using namespace std;
int strictness_level = 3; //Global variable required by T4 libraries

Statistics compare_geoms(const OptionsCompare &options)
{
  T4Geometry t4Geom(options.filenames[0]);
  MCNPGeometry mcnpGeom(options.filenames[1]);
  MCNPPTRAC mcnpPtrac(options.filenames[2], options.ptracFormat);
  Statistics stats;

  stats.setNbT4Volumes(t4Geom.getVolumes()->get_nb_vol());

  mcnpGeom.parseINP();
  long maxSampledPts = min(options.npoints, mcnpGeom.getNPS());

  std::cout << "Starting comparison on "
            << maxSampledPts << " points..."
            << std::endl;

  if (options.verbosity > 0) {
    cout << "delta is " << options.delta << endl;
  }

  if(!options.guessMaterialAssocs) {
    auto const &compos = t4Geom.getCompos()->get_compo_map();
    for(auto const &compo: compos) {
      std::string const &compo_name = compo.second;
      if(compo_name == "No compo") {
        continue;
      }
      auto pos = compo_name.find_first_of("_");
      std::string index = compo_name.substr(1, pos-1);
      std::string density = compo_name.substr(pos+1);
      if(index == "0") {
        density = "void";
      } else {
        density = compo_name.substr(pos+1);
      }
      std::string mcnp_compo_name = index + "_" + density;
      if (options.verbosity > 0) {
        std::cout << "associating MCNP material \"" << mcnp_compo_name << "\" --> T4 composition \"" << compo_name
          << '"' << endl;
      }
      t4Geom.addEquivalence(mcnp_compo_name, compo_name);
    }
  }

  unsigned long countPoints = 0;
  auto current = std::chrono::system_clock::now();
  auto previous = current;
  while(mcnpPtrac.readNextPtracData(maxSampledPts)) {

    ++countPoints;

    current = std::chrono::system_clock::now();
    auto print_seconds = current - previous;
    if(print_seconds > 5s) {
      std::cout << "Progress: " << countPoints << " / " << maxSampledPts << std::endl;
      previous = current;
    }

    auto const &record = mcnpPtrac.getPTRACRecord();
    auto const &point = record.point;
    long rank = t4Geom.getVolumes()->which_volume(point);
    std::string compo = t4Geom.getCompos()->get_name_from_volume(rank);

    if (rank < 0) {
      stats.incrementOutside();
    } else {
      stats.recordCoveredRank(rank);

      unsigned long cID = record.cellID;
      string materialDensityKey = mcnpGeom.getCellDensity(cID);
      if (!t4Geom.materialInMap(materialDensityKey) && options.guessMaterialAssocs) {
        if (options.verbosity > 0) {
          cout << "at point: (" << point[0] << ", " << point[1] << ", " << point[2]
            << "); associating MCNP material \"" << materialDensityKey << "\" (cell ID " << cID << ") --> T4 composition \"" << compo
            << '"' << endl;
        }
        t4Geom.addEquivalence(materialDensityKey, compo);
        stats.incrementSuccess();
      } else {
        if (t4Geom.weakEquivalence(materialDensityKey, compo)) {
          stats.incrementSuccess();
        } else {
          double const dist = t4Geom.distanceFromSurface(point, rank);
          if (dist <= options.delta) {
            stats.incrementIgnore();
          } else {
            int pID = record.pointID;
            int mID = record.materialID;
            stats.incrementFailure();
            stats.recordFailure(point, rank, pID, cID, mID, dist);
            if (options.verbosity > 0) {
              cout << "Failed tests at position: " << endl
                   << "x = " << point[0] << endl
                   << "y = " << point[1] << endl
                   << "z = " << point[2] << endl;
              cout << "T4 rank: " << rank << "   T4 compo: " << compo << endl;
              cout << "MCNP cellID: " << record.cellID << "   MCNP compo: " << materialDensityKey << endl;
            }
          }
        }
      }
    }
  }
  return stats;
}

int main(int argc, char **argv)
{
  auto start = std::chrono::system_clock::now();
  std::cout << "*** MCNP / Tripoli-4 geometry comparison ***" << endl;
  t4_output_stream = &cout;
  t4_language = (T4_language)0;

  // ---- Read options ----
  OptionsCompare options;
  options.get_opts(argc, argv);
  if (options.help) {
    help();
    exit(EXIT_SUCCESS);
  }

  Statistics stats = compare_geoms(options);
  stats.report();
  stats.writeOutForVisu(options.filenames[0]);

  auto end = std::chrono::system_clock::now();
  std::chrono::duration<double> elapsed_seconds = end - start;
  std::cout << "Elapsed time: " << elapsed_seconds.count() << "s\n";
  std::cout << "Time per point: " << elapsed_seconds.count() / stats.getTotalPts() << "s\n";
  return 0;
}
