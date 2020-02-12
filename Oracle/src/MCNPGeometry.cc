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
#include <algorithm>
#include <cassert>
#include <cctype>
#include <unistd.h>

MCNPGeometry::MCNPGeometry(const std::string &inputPath) : nps(-1),
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
  std::string lineLower;
  std::transform(std::begin(currentLine), std::end(currentLine),
                 std::back_inserter(lineLower),
                 [](char c) { return std::tolower(c); });
  std::string::size_type const pos = lineLower.find("like");

  std::istringstream iss(currentLine);
  unsigned long cellNum;
  iss >> cellNum;

  if(pos != std::string::npos) {
    handleLikeNBut(cellNum, pos);
    return;
  }

  std::string density;
  if (iss) {
    unsigned long matNum;
    iss >> matNum;
    if (matNum == 0) {
      addCell2Density(cellNum, {0, "void"});
    } else {
      iss >> density;
      std::istringstream istest(density);
      double fdensity;
      istest >> fdensity;
      if (istest.fail()) {
        std::cerr << "WRONG DENSITY / CELL Definition" << endl;
        std::cerr << density << endl;
        std::cerr << currentLine << endl;
        exit(EXIT_FAILURE);
      }
      auto last_non_zero = density.find_last_not_of('0');
      if(last_non_zero == std::string::npos) {
        addCell2Density(cellNum, {matNum, density});
      } else {
        std::string density_norm = density.substr(0, last_non_zero+1);
        if(density_norm.back() == '.') {
          density_norm.push_back('0');
        }
        addCell2Density(cellNum, {matNum, density_norm});
      }
    }
  }
}

void MCNPGeometry::handleLikeNBut(unsigned long cellNum, std::string::size_type pos)
{
  std::istringstream iss(currentLine.substr(pos+4));
  unsigned long likeNum;
  iss >> likeNum;
  std::string but_str;
  iss >> but_str;
  decltype(cell2Density)::mapped_type newValue = cell2Density.at(likeNum);
  while(iss) {
    std::string token;
    iss >> token;
    std::string tokenLower;
    std::transform(std::begin(token), std::end(token),
                   std::back_inserter(tokenLower),
                   [](char c) { return std::tolower(c); });
    if(tokenLower.substr(0, 4) == "rho=") {
      newValue.second = token.substr(4);
    } else if(tokenLower.substr(0, 4) == "mat=") {
      std::istringstream issMatNum(token.substr(4));
      unsigned long matNum;
      issMatNum >> matNum;
      newValue.first = matNum;
    }
  }
  addCell2Density(cellNum, newValue);
}

void MCNPGeometry::addCell2Density(unsigned long key, const std::pair<unsigned long, std::string> &value)
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
    int emptyLinesRemaining = 1;
    getline(inputFile, currentLine);
    if(currentLine.substr(0, 8) == "message:" || currentLine.substr(0, 8) == "message:") {
      ++emptyLinesRemaining;
    }
    while (getline(inputFile, currentLine)) {
      if (currentLine.empty()) {
        --emptyLinesRemaining;
      }
      if(emptyLinesRemaining == 0) {
        break;
      }
      if(isLineAComment(currentLine)) {
        continue;
      }
      auto const pos = currentLine.find_first_of("0123456789");
      if(pos != std::string::npos && pos < 5) {
        associateCell2Density();
      }
    }
    while (getline(inputFile, currentLine)) {
      if (currentLine.find("NPS") != std::string::npos || currentLine.find("nps") != std::string::npos) {
        std::istringstream iss(currentLine);
        std::string dummy;
        double nps;
        iss >> dummy >> nps;
        this->nps = long(nps);
        break;
      }
    }
    std::cout << "...read " << cell2Density.size() << " MCNP cells and their densities" << std::endl;
  }
}

bool MCNPGeometry::isLineAComment(std::string const &lineContent) const
{
  return lineContent[0] == 'c' || lineContent[0] == 'C';
}

bool MCNPGeometry::isLineAMaterial(std::string const &lineContent) const
{
  return lineContent[0] == 'm' || lineContent[0] == 'M';
}

std::string MCNPGeometry::getCellDensity(unsigned long cellID) const
{
  auto const &value = cell2Density.at(cellID);
  std::string value_str = std::to_string(value.first) + "_" + value.second;
  return value_str;
}

const std::string &MCNPGeometry::getInputPath()
{
  return inputPath;
}

long MCNPGeometry::getNPS()
{
  return nps;
}

std::map<unsigned long, std::pair<unsigned long, std::string>> &MCNPGeometry::getCell2Density()
{
  return cell2Density;
}

/************************************
*                                  *
*  methods of the MCNPPTRAC class  *
*                                  *
************************************/

MCNPPTRAC::MCNPPTRAC() : nbPointsRead(0)
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

PTRACRecord const &MCNPPTRAC::getPTRACRecord() const
{
  return record;
}

/*****************************************
*                                       *
*  methods of the MCNPPTRACASCII class  *
*                                       *
*****************************************/

MCNPPTRACASCII::MCNPPTRACASCII(std::string const &ptracPath) : MCNPPTRAC(),
                                                               nbDataCellMaterialLine(0),
                                                               ptracFile(ptracPath)
{
  if (ptracFile.fail()) {
    std::cerr << "PTRAC file " << ptracPath << " not found." << endl;
    exit(EXIT_FAILURE);
  }
  // The number of header lines must be 8!!
  goThroughHeaderPTRAC(8);
}

std::pair<int, int> MCNPPTRACASCII::readPointEvent()
{
  std::istringstream iss(currentLine);
  int pointID, eventID;
  iss >> pointID >> eventID;
  return {pointID, eventID};
}

std::pair<int, int> MCNPPTRACASCII::readCellMaterial()
{
  std::istringstream iss(currentLine);
  int dummy, volumeID, materialID;
  for (int ii = 1; ii <= nbDataCellMaterialLine - 2; ii++) {
    iss >> dummy;
  }
  iss >> volumeID >> materialID;
  return {volumeID, materialID};
}

std::vector<double> MCNPPTRACASCII::readPoint()
{
  std::istringstream iss(currentLine);
  double pointX, pointY, pointZ;
  iss >> pointX >> pointY >> pointZ;
  return {pointX, pointY, pointZ};
}

bool MCNPPTRACASCII::readNextPtracData(long maxReadPoint)
{
  if ((ptracFile && !ptracFile.eof()) && (getNbPointsRead() <= maxReadPoint)) {
    getline(ptracFile, currentLine);
    if (!currentLine.empty()) {
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
  std::string line5, line6;
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

int MCNPPTRACASCII::getDataFromLine5Ptrac(const std::string &line5)
{
  int nbDataPointEventLine;
  std::istringstream iss(line5);
  iss >> nbDataPointEventLine >> nbDataCellMaterialLine;
  int nbData = nbDataPointEventLine + nbDataCellMaterialLine;
  return nbData;
}

void MCNPPTRACASCII::checkDataFromLine6Ptrac(const std::string &line6, int nbData)
{
  vector<int> data(nbData);
  constexpr int cellIDPtracCode = 17;
  constexpr int materialIDPtracCode = 18;
  std::istringstream iss(line6);
  for (int jj = 0; jj < nbData; jj++) {
    iss >> data[jj];
  }
  if ((data[nbData - 2] != cellIDPtracCode) && (data[nbData - 1] != materialIDPtracCode)) {
    std::cerr << "PTRAC file format not suitable. Please see Oracle/data/slapb file for example..." << endl;
    exit(EXIT_FAILURE);
  }
}

/*****************************************
*                                        *
*  methods of the MCNPPTRACBinary class  *
*                                        *
******************************************/

MCNPPTRACBinary::MCNPPTRACBinary(std::string const &ptracPath) : ptracFile(ptracPath, std::ios_base::binary)
{
  if (ptracFile.fail()) {
    std::cerr << "PTRAC file " << ptracPath << " not found." << endl;
    exit(EXIT_FAILURE);
  }
  parseHeader();
}

bool MCNPPTRACBinary::readNextPtracData(long maxReadPoint)
{
  if ((ptracFile && ptracFile.peek() != EOF) && getNbPointsRead() <= maxReadPoint) {
    parsePTRACRecord();
    incrementNbPointsRead();
    return true;
  }
  return false;
}

void MCNPPTRACBinary::parseHeader()
{
  skipHeader();
  skipPtracInputData();
  parseVariableIDs();
}

void MCNPPTRACBinary::skipHeader()
{
  readRecord(ptracFile); // header
  readRecord(ptracFile); // code, version, dates
  readRecord(ptracFile); // calculation title
}

void MCNPPTRACBinary::skipPtracInputData()
{
  std::string buffer = readRecord(ptracFile);
  std::stringstream bufferStream(buffer);
  int n_fields_total = (int)readBinary<double>(bufferStream);
  int n_fields_read = 0;
  int n_desc = 0;

  while (n_fields_read < n_fields_total) {
    if (bufferStream.peek() == EOF) {
      buffer = readRecord(ptracFile);
      bufferStream.str(buffer);
      bufferStream.clear();
    }
    if (n_desc == 0) {
      n_desc = (int)readBinary<double>(bufferStream);
      ++n_fields_read;
    } else {
      --n_desc;
      readBinary<double>(bufferStream); // throw away field descriptor
    }
  }
}

void MCNPPTRACBinary::parseVariableIDs()
{
  std::string buffer = readRecord(ptracFile); // line 6
  auto const fields = reinterpretBuffer<int, long, long>(buffer);
  const int nbDataNPS = std::get<0>(fields);
  const long nbDataSrcLong = std::get<1>(fields);
  const long nbDataSrcDouble = std::get<2>(fields);

  buffer = readRecord(ptracFile); // line 7
  std::stringstream bufferStream(buffer);

  // Skip over the NPS data line. For some reason these fields are written as
  // longs.
  for (int i = 0; i < nbDataNPS; ++i) {
    reinterpretBuffer<long>(bufferStream);
  }

  constexpr int eventID = 7;
  constexpr int cellID = 17;
  constexpr int matID = 18;
  int eventIdx = -1;
  int cellIdx = -1;
  int matIdx = -1;
  for (int i = 0; i < nbDataSrcLong; ++i) {
    const int varID = std::get<0>(reinterpretBuffer<int>(bufferStream));
    switch (varID) {
    case eventID:
      eventIdx = i;
      break;
    case cellID:
      cellIdx = i;
      break;
    case matID:
      matIdx = i;
      break;
    }
  }

  constexpr int pointXID = 20;
  constexpr int pointYID = 21;
  constexpr int pointZID = 22;
  int pointXIdx = -1;
  int pointYIdx = -1;
  int pointZIdx = -1;
  for (int i = 0; i < nbDataSrcDouble; ++i) {
    const int varID = std::get<0>(reinterpretBuffer<int>(bufferStream));
    switch (varID) {
    case pointXID:
      pointXIdx = i;
      break;
    case pointYID:
      pointYIdx = i;
      break;
    case pointZID:
      pointZIdx = i;
      break;
    }
  }

  indices = PTRACRecordIndices{eventIdx, cellIdx, matIdx, pointXIdx, pointYIdx, pointZIdx, nbDataSrcLong, nbDataSrcDouble};
}

void MCNPPTRACBinary::parsePTRACRecord()
{
  long point = -1;
  long event = -1, oldEvent = -1;
  constexpr long lastEvent = 9000;
  constexpr long sourceEvent = 1000;
  long cell = -1;
  long mat = -1;
  double px = 0.;
  double py = 0.;
  double pz = 0.;

  std::string buffer = readRecord(ptracFile); // NPS line
  std::tie(point, event) = reinterpretBuffer<long, long>(buffer);
  if(event != sourceEvent) {
    throw std::logic_error("expected source event at the start of the history");
  }

  while (event != lastEvent) {
    buffer = readRecord(ptracFile); // data line (all doubles, even though the
                                    // first group are actually longs)
    std::stringstream bufferStream(buffer);
    for (int i = 0; i < indices.nbDataSrcLong; ++i) {
      const auto someLong = static_cast<long>(std::get<0>(reinterpretBuffer<double>(bufferStream)));
      if (i == indices.event) {
        oldEvent = event;
        event = someLong;
      } else if (i == indices.cell) {
        cell = someLong;
      } else if (i == indices.mat) {
        mat = someLong;
      }
    }
    for (int i = 0; i < indices.nbDataSrcDouble; ++i) {
      const auto someDouble = std::get<0>(reinterpretBuffer<double>(bufferStream));
      if (i == indices.px) {
        px = someDouble;
      } else if (i == indices.py) {
        py = someDouble;
      } else if (i == indices.pz) {
        pz = someDouble;
      }
    }

    if(oldEvent == sourceEvent) {
      record = PTRACRecord{point, oldEvent, cell, mat, {px, py, pz}};
    }
  }
}
