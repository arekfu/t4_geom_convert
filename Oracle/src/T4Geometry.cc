/*
 * T4Geometry.cc
 *
 *  Created on: 11 dec. 2018
 *      Author: jofausti
 */

#include "T4Geometry.hh"
/**
	Class constructor

  @param t4Filename The Tripoli-4 geometry file to be checked
*/
T4Geometry::T4Geometry(string t4Filename){
  this->t4Filename = t4Filename;
  //pair<Volumes*, Compos*> t4Geom = readT4input(t4Filename);
  readT4input(t4Filename);
  // volumes = t4Geom.first;
  // compos = t4Geom.second;
}

T4Geometry::~T4Geometry() {
	// TODO Auto-generated destructor stub
}

void T4Geometry::readT4input(const string t4Filename) {
	bool has_t4_geom = false;

	// for(std::vector<std::string>::const_iterator fname=filenames.begin(), efname=filenames.end();
	//     fname!=efname; ++fname) {
	std::cout << "\n--- Reading filename: " << t4Filename << std::endl;

	std::string c_tmpfilename;
  string fname = "slab.t4";
  
	const GeometryType geom_type = detect_geometry(fname);
  cerr << geom_type << endl;

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
      c_tmpfilename = preprocess(fname, "GEOMCOMP");
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

	// switch(geom_type) {
	// 	case T4_GEOMETRY_TYPE:
	// 	// first check that we have at most one T4 geometry
	// 	if(has_t4_geom) {
	// 		std::cerr << "\n---------------------------" << endl ;
	// 		std::cerr << "More than one T4 geometry" << endl ;
	// 		std::cerr << "detected; this is not allowed" << endl;
	// 		std::cerr << "-----------------------------" << endl ;
	// 		exit(EXIT_FAILURE);
	// 	}
  //
	// 	// Compositions
	// 	c_tmpfilename = preprocess(t4Filename, "GEOMCOMP");
	// 	if (c_tmpfilename.size() > 0) {
	// 		std::cout << "# Compositions - preprocessing file: " << c_tmpfilename << endl ;
	// 	} else {
	// 		std::cerr << "\n---------------------------" << endl ;
	// 		std::cerr << "T4 geometry detected, but" << endl ;
	// 		std::cerr << "GEOMCOMP is missing from the" << endl;
	// 		std::cerr << "input file." << endl ;
	// 		std::cerr << "-----------------------------" << endl ;
	// 		exit(EXIT_FAILURE);
	// 	}
	// 	has_t4_geom = true;
	// 	break;
	// 	default:
	// 	std::cerr << "\n---------------------------" << endl ;
	// 	std::cerr << "Unrecognized geometry: " << geom_type << endl ;
	// 	std::cerr << "-----------------------------" << endl ;
	// 	exit(EXIT_FAILURE);
	// }
	this->volumes = new AnyVolumes(geom_type, c_tmpfilename);
	this->compos = new ComposFromGeom();
	std::cout << "# Reading Volumes data" << endl;
	this->volumes->read(t4Filename);
	// Compos
	std::cout << "# Reading Compos data" << endl;
	this->compos->set_volumes(volumes);
	this->compos->read(c_tmpfilename);

	// push the object in the return vectors
	//return make_pair(volumes, compos);
}
