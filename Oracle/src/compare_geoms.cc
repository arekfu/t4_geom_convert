#include <iomanip>
#include <cstdlib>
#include <iostream>
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

T4_sobol_generator *gen_sobol = NULL;
T4_random *gen_random = NULL;
int strictness_level = 3;

void
init_sampling(const SamplingMethod &sampling_method, const int n_points)
{
  switch(sampling_method) {
    case SobolSampling:
      gen_sobol = new T4_sobol_generator(3, n_points);
      std::cout << "Using a " << n_points << "-point Sobol' sequence..." << std::endl;
      break;
    case RandomSampling:
      gen_random = new T4_random;
      gen_random->init(NULL, 0);
      std::cout << "Using a pseudo-random sequence..." << std::endl;
      break;
    default:
      std::cerr << "Error: unrecognized sampling method: " << sampling_method << std::endl;
      exit(EXIT_FAILURE);
      break;
  }
}

void
sample_point(const SamplingMethod &sampling_method, const double *bbox, std::vector<double> &point)
{
  switch(sampling_method) {
    case SobolSampling:
      gen_sobol->sample_vector();
      for(int i=0; i<3; ++i) {
        point[i] = gen_sobol->get_coordinate(i);
      }
      break;
    case RandomSampling:
      for(int i=0; i<3; ++i) {
        point[i] = gen_random->uni_random();
      }
      break;
    default:
      break;
  }

  point[0] = bbox[0] + (bbox[3]-bbox[0]) * point[0];
  point[1] = bbox[1] + (bbox[4]-bbox[1]) * point[1];
  point[2] = bbox[2] + (bbox[5]-bbox[2]) * point[2];
}

pair<std::vector<Volumes*>, std::vector<Compos*> >
read_geoms(std::vector<std::string> const &filenames) {
  std::vector<Volumes *> volumes;
  std::vector<Compos *> compos;

  bool has_t4_geom = false;

  for(std::vector<std::string>::const_iterator fname=filenames.begin(), efname=filenames.end();
      fname!=efname; ++fname) {
    std::cout << "\n--- Reading filename: " << *fname << std::endl;

    std::string c_tmpfilename;

    const GeometryType geom_type = detect_geometry(*fname);

    switch(geom_type) {
      case T4_GEOMETRY_TYPE:
        // first check that we have at most one T4 geometry
        if(has_t4_geom) {
          std::cerr << "\n---------------------------" << endl ;
          std::cerr << "More than one T4 geometry" << endl ;
          std::cerr << "detected; this is not allowed" << endl;
          std::cerr << "-----------------------------" << endl ;
          exit(EXIT_FAILURE);
        }

        // Compositions
        c_tmpfilename = preprocess(*fname, "GEOMCOMP");
        if (c_tmpfilename.size() > 0) {
          std::cout << "# Compositions - preprocessing file: " << c_tmpfilename << endl ;
        } else {
          std::cerr << "\n---------------------------" << endl ;
          std::cerr << "T4 geometry detected, but" << endl ;
          std::cerr << "GEOMCOMP is missing from the" << endl;
          std::cerr << "input file." << endl ;
          std::cerr << "-----------------------------" << endl ;
          exit(EXIT_FAILURE);
        }
        has_t4_geom = true;
        break;
      case ROOT_GEOMETRY_TYPE:
#ifndef HAS_ROOT
        std::cerr << "\n---------------------------" << endl ;
        std::cerr << "ROOT geometry detected, but" << endl ;
        std::cerr << "T4G was compiled without" << endl;
        std::cerr << "ROOT support. Use HAS_ROOT." << endl ;
        std::cerr << "-----------------------------" << endl ;
        exit(EXIT_FAILURE);
#endif // HAS_ROOT
        break;
      case ROOT_GEOMETRY_STACK_TYPE:
#ifndef HAS_ROOT
        std::cerr << "\n---------------------------" << endl ;
        std::cerr << "ROOTStack geometry detected," << endl ;
        std::cerr << "but T4G was compiled without" << endl;
        std::cerr << "ROOT support. Use HAS_ROOT." << endl ;
        std::cerr << "-----------------------------" << endl ;
        exit(EXIT_FAILURE);
#endif // HAS_ROOT
        break;
      case G4_GEOMETRY_TYPE:
#ifndef HAS_G4
        std::cerr << "\n---------------------------" << endl ;
        std::cerr << "Geant4 geometry detected, but" << endl ;
        std::cerr << "T4G was compiled without" << endl;
        std::cerr << "Geant4 support. Use HAS_G4." << endl ;
        std::cerr << "-----------------------------" << endl ;
        exit(EXIT_FAILURE);
#endif // HAS_G4
        break;
      default:
        std::cerr << "\n---------------------------" << endl ;
        std::cerr << "Unrecognized geometry: " << geom_type << endl ;
        std::cerr << "-----------------------------" << endl ;
        exit(EXIT_FAILURE);
    }
    Volumes *vols = new AnyVolumes(geom_type, c_tmpfilename);
    Compos *compo = new ComposFromGeom();
    std::cout << "# Reading Volumes data" << endl;
    vols->read(*fname);
    // Compos
    std::cout << "# Reading Compos data" << endl;
    compo->set_volumes(vols);
    compo->read(c_tmpfilename);

    // push the object in the return vectors
    volumes.push_back(vols);
    compos.push_back(compo);
  }
  return make_pair(volumes, compos);
}

void
compare_geoms(const OptionsCompare &options)
{
  t4_language = (T4_language) options.lang;
  pair<vector<Volumes*>, vector<Compos*> > geoms = read_geoms(options.filenames);
  vector<Volumes*> const &volumes = geoms.first;
  vector<Compos*> const &compos = geoms.second;

  if(volumes.size()!=compos.size()) {
    std::cerr << "Error: volumes and compos vectors have different sizes! ("
      << volumes.size() << "!=" << compos.size() << ")" << std::endl;
    exit(EXIT_FAILURE);
  }
  const size_t n_geoms = volumes.size();

  std::vector<double> point(3);
  int n_inside = 0;

  std::cout << "Bounding box: ("
    << options.bbox[0] << ", "
    << options.bbox[1] << ", "
    << options.bbox[2] << ") to ("
    << options.bbox[3] << ", "
    << options.bbox[4] << ", "
    << options.bbox[5] << ")" << std::endl;

  std::cout << "Starting comparison..." << std::endl;
  init_sampling(options.sampling_method, options.n_points);
  for(int i=0; i<options.n_points; ++i) {
    long rank, prev_rank;
    std::string compo, prev_compo;
    sample_point(options.sampling_method, options.bbox, point);

    // flag to check if the point is inside all geometries
    bool inside_all = true;

    for(size_t igeom=0; igeom<n_geoms; ++igeom) {
      rank = volumes[igeom]->which_volume(point);
      if(rank>=0) {
        compo = compos[igeom]->get_name_from_volume(rank);
      } else {
        inside_all = false;
        compo.clear();
      }

      if(igeom>0) {
        // do checks

        // check that both points are inside or outside the geometry
        if((rank>=0 && prev_rank<0) || (rank<0 && prev_rank>=0)) {
          std::cout << "Test #" << i << ": IN/OUT MISMATCH:"
            << "\n    point = "
            << point[0] << ", " << point[1] << ", " << point[2]
            << "\n    rank = " << rank << "; prev_rank = " << prev_rank
            << "\n    igeom = " << igeom
            << "\n    name = \"" << volumes[igeom]->get_name_from_volume(rank)
            << "\"; prev_name = \"" << volumes[igeom-1]->get_name_from_volume(prev_rank) << '"'
            << std::endl;
        } else if(options.verbosity>0) {
          std::cout << "Test #" << i << ": IN/OUT OK: point = "
            << point[0] << ", " << point[1] << ", " << point[2]
            << "; rank = " << rank << "; prev_rank = " << prev_rank
            << ", igeom = " << igeom
            << "\n    name = \"" << volumes[igeom]->get_name_from_volume(rank)
            << "\"; prev_name = \"" << volumes[igeom-1]->get_name_from_volume(prev_rank) << '"'
            << std::endl;
        }

        if(rank>=0) {
          if(compo!=prev_compo) {
            std::cout << "Test #" << i << ": COMPO MISMATCH:"
              << "\n    point = "
              << point[0] << ", " << point[1] << ", " << point[2]
              << "\n    rank = " << rank << "; prev_rank = " << prev_rank
              << "\n    igeom = " << igeom
              << "\n    name = \"" << volumes[igeom]->get_name_from_volume(rank)
              << "\"; prev_name = \"" << volumes[igeom-1]->get_name_from_volume(prev_rank)
              << "\"\n    compo = \"" << compo
              << "\"; prev_compo = \"" << prev_compo << '"'
              << std::endl;
          } else if(options.verbosity>0) {
            std::cout << "Test #" << i << ": COMPO OK:"
              << "\n    point = "
              << point[0] << ", " << point[1] << ", " << point[2]
              << "\n    rank = " << rank << "; prev_rank = " << prev_rank
              << "\n    igeom = " << igeom
              << "\n    name = \"" << volumes[igeom]->get_name_from_volume(rank)
              << "\"; prev_name = \"" << volumes[igeom-1]->get_name_from_volume(prev_rank)
              << "\"\n    compo = \"" << compo
              << "\"; prev_compo = \"" << prev_compo << '"'
              << std::endl;
          }
        }
      }
      prev_rank = rank;
      prev_compo = compo;
    }

    // count points inside all geometries
    if(inside_all)
      ++n_inside;
  }
  std::cout << "End of comparison." << std::endl;
  const float inside_percentage = 100.*float(n_inside)/float(options.n_points);
  std::cout << "Points inside all geometries: " << n_inside << "/" << options.n_points
    << " (" << inside_percentage << "%)" << std::endl;
  if(inside_percentage<50.) {
    std::cout << "\nYou may want to manually adjust the bounding box (--bbox) if this percentage is too low."
    << std::endl;
  }

  // ---- End ----
  for(vector<Volumes*>::const_iterator ivol=volumes.begin(), evol=volumes.end(); ivol!=evol; ++ivol) {
    (*ivol)->free();
  }
  delete gen_sobol;
  delete gen_random;
}

// int
// main(int argc, char ** argv)
// {
//   // tracability
//   std::cout << "*** Tripoli-4 geometry comparison ***" << endl;
//   std::cout << "Tripoli-4 Version is $Name:  $\n" << endl;
//   std::cout << "File Version is $Id: visutripoli4.cc,v 1.20 2016/07/26 09:09:13 dm232107 Exp $\n" << endl;
//   t4_output_stream = &cout;
//   t4_language = (T4_language) 2;
//
//   // ---- Read options ----
//   OptionsCompare options;
//   options.get_opts(argc, argv);
//   if (options.help){
//     help();
//     exit(EXIT_SUCCESS);
//   }
//
//   std::cout << "Will test on " << options.n_points << " points" << std::endl;
//   compare_geoms(options);
//
//   return 0;
// }

// ---- end of file visutripoli4.cc ----
