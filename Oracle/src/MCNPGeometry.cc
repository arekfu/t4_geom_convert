/**
* @file MCNPGeometry.cc
*
*
* @brief MCNPGeometry class
*
* @author J. Faustin
* @version 1.0
*/

#include "MCNPGeometry.hh"
#include "help.hh"
#include <cstdio>
#include <cstdlib>
#include <unistd.h>

using namespace std;

MCNPGeometry::MCNPGeometry(const string &ptracPath, const string &inputPath) : pointID(1),
                                                                               eventID(1),
                                                                               cellID(1),
                                                                               materialID(1),
                                                                               nbDataCellMaterialLine(0),
                                                                               nbPointsRead(0),
                                                                               nps(-1),
                                                                               ptracPath(ptracPath),
                                                                               inputPath(inputPath),
                                                                               ptracFile(ptracPath),
                                                                               inputFile(inputPath)
{
  if (ptracFile.fail()) {
    std::cerr << "PTRAC file not found." << endl;
    exit(EXIT_FAILURE);
  }
  if (inputFile.fail()) {
    std::cerr << "INP file not found." << endl;
    exit(EXIT_FAILURE);
  }
}

pair<int, int> MCNPGeometry::readPointEvent()
{
  istringstream iss(currentLine);
  int pointID, eventID;
  iss >> pointID >> eventID;
  return {pointID, eventID};
}

pair<int, int> MCNPGeometry::readCellMaterial()
{
  istringstream iss(currentLine);
  int dummy, volumeID, materialID;
  for (int ii = 1; ii <= nbDataCellMaterialLine - 2; ii++) {
    iss >> dummy;
  }
  iss >> volumeID >> materialID;
  return {volumeID, materialID};
}

vector<double> MCNPGeometry::readPoint()
{
  istringstream iss(currentLine);
  double pointX, pointY, pointZ;
  iss >> pointX >> pointY >> pointZ;
  return {pointX, pointY, pointZ};
}

bool MCNPGeometry::readNextPtracData(long maxReadPoint)
{
  if ((ptracFile && !ptracFile.eof()) && (getNbPointsRead() <= maxReadPoint)) {
    getline(ptracFile, currentLine);
    if (!finishedReading()) {
      setPointEvent(readPointEvent());

      getline(ptracFile, currentLine);
      setCellMaterial(readCellMaterial());

      getline(ptracFile, currentLine);
      setPointXyz(readPoint());
      incrementNbPointsRead();
      return true;
    } else {
      return false;
    }
  } else {
    return false;
  }
}

void MCNPGeometry::associateCell2Density()
{
  istringstream iss(currentLine);
  int cellNum;
  string density;
  if (iss >> cellNum) {
    int matNum;
    iss >> matNum;
    if (matNum == 0) {
      addCell2Density(cellNum, "void");
    } else {
      iss >> density;
      istringstream istest(density);
      double fdensity;
      istest >> fdensity;
      if (istest.fail()) {
        std::cerr << "WRONG DENSITY / CELL Definition" << endl;
        std::cerr << density << endl;
        std::cerr << currentLine << endl;
        exit(EXIT_FAILURE);
      }
      addCell2Density(cellNum, density);
    }
  }
}

void MCNPGeometry::addCell2Density(int key, const string &value)
{
  if (cell2Density.find(key) == cell2Density.end()) {
    cell2Density[key] = value;
  } else {
    std::cerr << "This cellID " << key << " already appeared in the MCNP input file." << endl;
    std::cerr << "Check MCNP input file for errors..." << endl;
  }
}

void MCNPGeometry::parseINP()
{
  if (inputFile) {
    while (getline(inputFile, currentLine)) {
      if (finishedReading()) {
        break;
      }
      if (!isLineAComment(currentLine) && isdigit(currentLine[0])) {
        associateCell2Density();
      }
    }
  }
  readNPS();
}

void MCNPGeometry::readNPS()
{
  string dummy;
  if (inputFile) {
    while (getline(inputFile, currentLine)) {
      if (isLineAComment(currentLine)) {
        continue;
      }
      if (currentLine.find("NPS") != string::npos || currentLine.find("nps") != string::npos) {
        istringstream iss(currentLine);
        double nps;
        iss >> dummy >> nps;
        this->nps = long(nps);
        break;
      }
    }
  }
}

void MCNPGeometry::goThroughHeaderPTRAC(int nHeaderLines)
{
  string line5, line6;
  for (int ii = 0; ii < nHeaderLines; ii++) {
    getline(ptracFile, currentLine);
    if (ii == 5) {
      line5 = currentLine;
    }
    if (ii == 6) {
      line6 = currentLine;
    }
  }
  int nbData = getDataFromLine5Ptrac(line5);
  checkDataFromLine6Ptrac(line6, nbData);
}

int MCNPGeometry::getDataFromLine5Ptrac(const string &line5)
{
  int nbDataPointEventLine;
  istringstream iss(line5);
  iss >> nbDataPointEventLine >> nbDataCellMaterialLine;
  int nbData = nbDataPointEventLine + nbDataCellMaterialLine;
  return nbData;
}

void MCNPGeometry::checkDataFromLine6Ptrac(const string &line6, int nbData)
{
  vector<int> data(nbData);
  const int cellIDPtracCode = 17;
  const int materialIDPtracCode = 18;
  istringstream iss(line6);
  for (int jj = 0; jj < nbData; jj++) {
    iss >> data[jj];
  }
  if ((data[nbData - 2] != cellIDPtracCode) && (data[nbData - 1] != materialIDPtracCode)) {
    std::cerr << "PTRAC file format not suitable. Please see Oracle/data/slapb file for example..." << endl;
    exit(EXIT_FAILURE);
  }
}

bool MCNPGeometry::finishedReading()
{
  return currentLine.length() == 1 || currentLine.empty();
}

int MCNPGeometry::isLineAComment(string lineContent)
{
  return lineContent[0] == 'c' || lineContent[0] == 'C';
}

void MCNPGeometry::incrementNbPointsRead()
{
  ++nbPointsRead;
}

string MCNPGeometry::getMaterialDensity()
{
  string density = cell2Density[cellID];
  return (to_string(materialID) + density);
}

const string &MCNPGeometry::getInputPath()
{
  return inputPath;
}

long MCNPGeometry::getNPS()
{
  return nps;
}

long MCNPGeometry::getNbPointsRead()
{
  return nbPointsRead;
}

const string &MCNPGeometry::getPtracPath()
{
  return ptracPath;
}

int MCNPGeometry::getPointID()
{
  return pointID;
}

int MCNPGeometry::getEventID()
{
  return eventID;
}

void MCNPGeometry::setPointEvent(const pair<int, int> &pointEvent)
{
  this->pointID = pointEvent.first;
  this->eventID = pointEvent.second;
}

vector<double> MCNPGeometry::getPointXyz()
{
  return pointXYZ;
}

void MCNPGeometry::setPointXyz(const vector<double> &pointXyz)
{
  pointXYZ = pointXyz;
}

int MCNPGeometry::getCellID()
{
  return cellID;
}

int MCNPGeometry::getMaterialID()
{
  return materialID;
}

void MCNPGeometry::setCellMaterial(const pair<int, int> &cellMat)
{
  this->cellID = cellMat.first;
  this->materialID = cellMat.second;
}

map<int, string> &MCNPGeometry::getCell2Density()
{
  return cell2Density;
}

void MCNPGeometry::getNextLine()
{
  getline(ptracFile, currentLine);
}
