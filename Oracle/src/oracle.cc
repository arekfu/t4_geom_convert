/**
 * @file oracle.cc
 * This is the main file for the test Oracle of the converter.
 *
 * @brief contains the main functions of the Oracle program
 *
 * @author J. Faustin
 * @version 1.0
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <cstdlib>
#include <vector>
#include <utility>
#include "options_compare.hh"
#include "geometrytype.hh"
#include "volumes.hh"
#include "anyvolumes.hh"
#include "compos.hh"
#include "composfromgeom.hh"
#include "t4coreglob.hh"
#include "t4convert.hh"
#include "t4sobol.hh"
#include "t4random.hh"
#include "MCNPGeometry.hh"
#include "T4Geometry.hh"
#include "Statistics.hh"
#include <chrono>

using namespace std;
int strictness_level = 3;

Statistics compare_geoms(const OptionsCompare &options){
  T4Geometry t4Geom(options.filenames[0], options.delta);
  cout << "delta is " << t4Geom.getDelta() << endl;
  MCNPGeometry mcnpGeom(options.filenames[2], options.filenames[1]);
  Statistics stats;
  vector<double> point;

  stats.setNbT4Volumes(t4Geom.getVolumes()->get_nb_vol());

  mcnpGeom.parseINP();
  long nbSampledPts = min(options.npoints, mcnpGeom.getNPS());

  std::cout << "Starting comparison on "
            <<  nbSampledPts << " points..."
            << std::endl;
  mcnpGeom.goThroughHeaderPTRAC(8);

  while (mcnpGeom.readNextPtracData(nbSampledPts)) {
    long rank;
    std::string compo;

    point = mcnpGeom.getPointXyz();
    rank = t4Geom.getVolumes()->which_volume(point);
    compo = t4Geom.getCompos()->get_name_from_volume(rank);


    if (rank<0){
      stats.incrementOutside();
    }else{
      stats.recordCoveredRank(rank);

      string materialDensityKey = mcnpGeom.getMaterialDensity();
      if (!t4Geom.materialInMap(materialDensityKey)){
          t4Geom.addEquivalence(materialDensityKey, compo);
          stats.incrementSuccess();
      }
      else{
        if (t4Geom.weakEquivalence(materialDensityKey, compo)){
          stats.incrementSuccess();
        }
        else {
          if(t4Geom.isPointNearSurface(point, rank)){
              stats.incrementIgnore();
          }
          else{
            stats.incrementFailure();
            stats.recordFailure(point, rank);
          }
        }
      }


    }
  }
  return stats;
}

int main(int argc, char ** argv){
  // tracability
  auto start = std::chrono::system_clock::now();
  std::cout << "*** MCNP / Tripoli-4 geometry comparison ***" << endl;
  // std::cout << "Tripoli-4 Version is $Name:  $\n" << endl;
  // std::cout << "File Version is $Id: visutripoli4.cc,v 1.20 2016/07/26 09:09:13 dm232107 Exp $\n" << endl;
  t4_output_stream = &cout;
  t4_language = (T4_language) 0;

  // ---- Read options ----
  OptionsCompare options;
  options.get_opts(argc, argv);
  if (options.help){
    help();
    exit(EXIT_SUCCESS);
  }

  Statistics stats = compare_geoms(options);
  stats.report();
  stats.writeOutForVisu("data_set.points");

  auto end = std::chrono::system_clock::now();
  std::chrono::duration<double> elapsed_seconds = end-start;
  std::cout << "Elapsed time: " << elapsed_seconds.count() << "s\n";
  std::cout << "Time per point: "<< elapsed_seconds.count()/stats.getTotalPts() << "s\n";
  return 0;
}
