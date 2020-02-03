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

using namespace std;

const vector<vector<double>> T4Geometry::directions = {{0.0, 0.0, 1.0},
                                                       {0.0, 0.0, -1.0},
                                                       {0.0, 1.0, 0.0},
                                                       {0.0, -1.0, 0.0},
                                                       {1.0, 0.0, 0.0},
                                                       {-1.0, 0.0, 0.0}};

T4Geometry::T4Geometry(const string &t4Filename) : t4Filename(t4Filename)
{
  readT4input();
}

T4Geometry::~T4Geometry() {}

void T4Geometry::readT4input()
{
  std::cout << "\n--- Reading : " << t4Filename << std::endl;

  std::string c_tmpfilename;

  const GeometryType geom_type = detect_geometry(t4Filename);

  switch (geom_type) {
  case T4_GEOMETRY_TYPE:
    c_tmpfilename = preprocess(t4Filename, "GEOMCOMP");
    if (c_tmpfilename.size() > 0) {
      std::cout << "# Compositions - preprocessing file: " << c_tmpfilename << endl;
    } else {
      std::cerr << "\n---------------------------" << endl;
      std::cerr << "T4 geometry detected, but" << endl;
      std::cerr << "GEOMCOMP is missing from the" << endl;
      std::cerr << "input file." << endl;
      std::cerr << "-----------------------------" << endl;
      exit(EXIT_FAILURE);
    }
    break;

  default:
    std::cerr << "\n---------------------------" << endl;
    std::cerr << "Unrecognized geometry: " << geom_type << endl;
    std::cerr << "-----------------------------" << endl;
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

bool T4Geometry::materialInMap(const string &matDens)
{
  return (equivalenceMap.find(matDens) != equivalenceMap.end());
}

void T4Geometry::addEquivalence(const string &matDens, const string &compo)
{
  equivalenceMap.insert(std::pair<string, string>(matDens, compo));
}

bool T4Geometry::weakEquivalence(const string &matDens, const string &compo)
{
  if (!materialInMap(matDens)) {
    cerr << "ERROR: Testing weak equivalence on non-registered material: "
      << matDens << endl;
    return false;
  }
  return (equivalenceMap[matDens] == compo);
}

string T4Geometry::getFilename()
{
  return t4Filename;
}

Volumes *const &T4Geometry::getVolumes()
{
  return volumes;
}

Compos *const &T4Geometry::getCompos()
{
  return compos;
}

double T4Geometry::distanceFromSurface(const vector<double> &point, long rank)
{
  double shortestDist = 1.0e+10;
  pair<double, long> result;
  for (auto const &idir : T4Geometry::directions) {
    result = volumes->next_surface_in_direction(rank, point, idir);
    shortestDist = min(result.first, shortestDist);
  }
  return shortestDist;
}
