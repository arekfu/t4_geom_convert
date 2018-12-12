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
  readT4input();
}

T4Geometry::~T4Geometry() {
  // TODO Auto-generated destructor stub
}

/**
Reads the T4 input file and stores the volumes and compositions information
*/
void T4Geometry::readT4input() {
  std::cout << "\n--- Reading : " << t4Filename << std::endl;

  std::string c_tmpfilename;

  const GeometryType geom_type = detect_geometry(t4Filename);

  switch(geom_type) {
    case T4_GEOMETRY_TYPE:
    c_tmpfilename = preprocess(t4Filename, "GEOMCOMP");
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
    break;

    default:
    std::cerr << "\n---------------------------" << endl ;
    std::cerr << "Unrecognized geometry: " << geom_type << endl ;
    std::cerr << "-----------------------------" << endl ;
    exit(EXIT_FAILURE);
  }


  this->volumes = new AnyVolumes(geom_type, c_tmpfilename);
  this->compos = new ComposFromGeom();
  std::cout << "# Reading Volumes data" << endl;
  this->volumes->read(t4Filename);
  // Compos
  std::cout << "# Reading Compos data" << endl;
  this->compos->set_volumes(volumes);
  this->compos->read(c_tmpfilename);
}

bool T4Geometry::materialInMap(int materialID){
  return (equivalenceMap.find(materialID) != equivalenceMap.end());
}

void T4Geometry::addEquivalence(int materialID, string compo){
  if (!materialInMap(materialID)){
    equivalenceMap[materialID] = compo;
  }
}

bool T4Geometry::weakEquivalence(int materialID, string compo){
  if (!materialInMap(materialID)){
    cerr << "ERROR : Testing weak equivalence on non-registered material" << endl;
    return false;
  }
  return (equivalenceMap[materialID] == compo);
}
