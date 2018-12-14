/**
 * @file T4Geometry.cc
 *
 *
 * @brief T4Geometry class
 *
 * @author J. Faustin
 * @version 1.0
 */

#include "T4Geometry.hh"

T4Geometry::T4Geometry(const string& t4Filename, double delta) : t4Filename(t4Filename){
  this->delta = delta;
  readT4input();
}


T4Geometry::~T4Geometry() {
  // TODO Auto-generated destructor stub
}


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

bool T4Geometry::materialInMap(string matDens){
  return (equivalenceMap.find(matDens) != equivalenceMap.end());
}

void T4Geometry::addEquivalence(string matDens, const string& compo){
  if (!materialInMap(matDens)){
    equivalenceMap[matDens] = compo;
  }
}

bool T4Geometry::weakEquivalence(string matDens, const string& compo){
  if (!materialInMap(matDens)){
    cerr << "ERROR : Testing weak equivalence on non-registered material" << endl;
    return false;
  }
  return (equivalenceMap[matDens] == compo);
}

string T4Geometry::getFilename(){
  return t4Filename;
}

Volumes* const & T4Geometry::getVolumes(){
  return volumes;
}

Compos* const & T4Geometry::getCompos(){
  return compos;
}

bool T4Geometry::isPointNearSurface(const vector<double>& point, long rank){
  double shortestDist=1.0e+10;
  pair<double, long> result;
  vector<vector<double> >directions = { { 0.0, 0.0, 1.0},
                                        { 0.0, 0.0,-1.0},
                                        { 0.0, 1.0, 0.0},
                                        { 0.0,-1.0, 0.0},
                                        { 1.0, 0.0, 0.0},
                                        {-1.0, 0.0, 0.0} };
  for(vector<vector<double> >::iterator idir=directions.begin(), edir=directions.end();
      idir!=edir; ++idir){
        result = volumes->next_surface_in_direction(rank, point, *idir);
        shortestDist = min(result.first, shortestDist);
      }
  return shortestDist <= delta;
}
