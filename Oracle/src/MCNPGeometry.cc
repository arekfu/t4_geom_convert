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
#include <cassert>
#include <unistd.h>

using namespace std;

MCNPGeometry::MCNPGeometry(const string &inputPath) :
  nps(-1),
  inputPath(inputPath),
  inputFile(inputPath)
{
  if (inputFile.fail()) {
    std::cerr << "INP file not found." << endl;
    exit(EXIT_FAILURE);
  }
}

void MCNPGeometry::associateCell2Density()
{
  istringstream iss(currentLine);
  unsigned long cellNum;
  string density;
  if (iss >> cellNum) {
    unsigned long matNum;
    iss >> matNum;
    if (matNum == 0) {
      addCell2Density(cellNum, {0, "void"});
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
      addCell2Density(cellNum, {matNum, density});
    }
  }
}

void MCNPGeometry::addCell2Density(unsigned long key, const std::pair<unsigned long, std::string> &value)
{
  if (cell2Density.find(key) == cell2Density.end()) {
    std::string value_str = std::to_string(value.first) + "_" + value.second;
    cell2Density[key] = value_str;
  } else {
    std::cerr << "This cellID " << key << " already appeared in the MCNP input file." << endl;
    std::cerr << "Check MCNP input file for errors..." << endl;
  }
}

void MCNPGeometry::parseINP()
{
  if (inputFile) {
    while (getline(inputFile, currentLine)) {
      if(finishedReading()) {
        break;
      }
      if (!isLineAComment(currentLine) && isdigit(currentLine[0])) {
        associateCell2Density();
      }
    }
    while (getline(inputFile, currentLine)) {
      if (currentLine.find("NPS") != string::npos || currentLine.find("nps") != string::npos) {
        istringstream iss(currentLine);
        string dummy;
        double nps;
        iss >> dummy >> nps;
        this->nps = long(nps);
        break;
      }
    }
    std::cout << "...read " << cell2Density.size() << " MCNP cells and their densities" << std::endl;
  }
}

bool MCNPGeometry::finishedReading()
{
  return currentLine.empty();
}

bool MCNPGeometry::isLineAComment(string const &lineContent) const
{
  return lineContent[0] == 'c' || lineContent[0] == 'C';
}

bool MCNPGeometry::isLineAMaterial(string const &lineContent) const
{
  return lineContent[0] == 'm' || lineContent[0] == 'M';
}

string const &MCNPGeometry::getCellDensity(unsigned long cellID) const
{
  return cell2Density.at(cellID);
}

const string &MCNPGeometry::getInputPath()
{
  return inputPath;
}

long MCNPGeometry::getNPS()
{
  return nps;
}

map<unsigned long, string> &MCNPGeometry::getCell2Density()
{
  return cell2Density;
}


/************************************
*                                  *
*  methods of the MCNPPTRAC class  *
*                                  *
************************************/

MCNPPTRAC::MCNPPTRAC() :
  nbPointsRead(0)
{
}

void MCNPPTRAC::incrementNbPointsRead()
{
  ++nbPointsRead;
}

long MCNPPTRAC::getNbPointsRead()
{
  return nbPointsRead;
}

void MCNPPTRACASCII::getNextLinePtrac()
{
  getline(ptracFile, currentLine);
}

bool MCNPPTRACASCII::finishedReading()
{
  return currentLine.empty();
}

PTRACRecord const &MCNPPTRAC::getPTRACRecord() const
{
  return record;
}


/************************************
*                                  *
*  methods of the MCNPPTRACASCII class  *
*                                  *
************************************/

MCNPPTRACASCII::MCNPPTRACASCII(std::string const &ptracPath) :
  MCNPPTRAC(),
  nbDataCellMaterialLine(0),
  ptracFile(ptracPath)
{
  if(ptracFile.fail()) {
    std::cerr << "PTRAC file " << ptracPath << " not found." << endl;
    exit(EXIT_FAILURE);
  }
  // The number of header lines must be 8!!
  goThroughHeaderPTRAC(8);
}


pair<int, int> MCNPPTRACASCII::readPointEvent()
{
  istringstream iss(currentLine);
  int pointID, eventID;
  iss >> pointID >> eventID;
  return {pointID, eventID};
}

pair<int, int> MCNPPTRACASCII::readCellMaterial()
{
  istringstream iss(currentLine);
  int dummy, volumeID, materialID;
  for (int ii = 1; ii <= nbDataCellMaterialLine - 2; ii++) {
    iss >> dummy;
  }
  iss >> volumeID >> materialID;
  return {volumeID, materialID};
}

std::vector<double> MCNPPTRACASCII::readPoint()
{
  istringstream iss(currentLine);
  double pointX, pointY, pointZ;
  iss >> pointX >> pointY >> pointZ;
  return {pointX, pointY, pointZ};
}

bool MCNPPTRACASCII::readNextPtracData(long maxReadPoint)
{
  if ((ptracFile && !ptracFile.eof()) && (getNbPointsRead() <= maxReadPoint)) {
    getline(ptracFile, currentLine);
    if (!finishedReading()) {
      auto const pointEvent = readPointEvent();
      getline(ptracFile, currentLine);
      auto const cellMaterial = readCellMaterial();
      getline(ptracFile, currentLine);
      auto const point = readPoint();
      incrementNbPointsRead();
      record = {pointEvent.first, pointEvent.second,
        cellMaterial.first, cellMaterial.second,
        point};
      return true;
    } else {
      return false;
    }
  } else {
    return false;
  }
}

void MCNPPTRACASCII::goThroughHeaderPTRAC(int nHeaderLines)
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

int MCNPPTRACASCII::getDataFromLine5Ptrac(const string &line5)
{
  int nbDataPointEventLine;
  istringstream iss(line5);
  iss >> nbDataPointEventLine >> nbDataCellMaterialLine;
  int nbData = nbDataPointEventLine + nbDataCellMaterialLine;
  return nbData;
}

void MCNPPTRACASCII::checkDataFromLine6Ptrac(const string &line6, int nbData)
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
