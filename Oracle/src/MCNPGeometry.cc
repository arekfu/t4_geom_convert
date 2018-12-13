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

MCNPGeometry::MCNPGeometry(string ptracPath, string inputPath) :
volumeList({}), ptracPath(ptracPath), inputPath(inputPath) {
  pointID = -1;
  eventID = -1;
  cellID = -1;
  nps = -1;
  materialID = -1;
  nPointsRead = 0;


  ptracFile.open(ptracPath);
  if(ptracFile.fail()){
    cerr << "PTRAC file not found." << endl;
    exit(EXIT_FAILURE);
  }
  inputFile.open(inputPath);
  if(inputFile.fail()){
    cerr << "INP file not found." << endl;
    exit(EXIT_FAILURE);
  }
}

MCNPGeometry::~MCNPGeometry() {
  ptracFile.close();
  inputFile.close();
}

pair<int, int> MCNPGeometry::readPointEvent() {
  getline(ptracFile, currentLine);
  istringstream iss(getCurrentLine());
  int pointID, eventID;
  iss >> pointID >> eventID;
  return {pointID, eventID};
}

pair<int, int> MCNPGeometry::readCellMaterial() {
  getline(ptracFile, currentLine);
  istringstream iss(currentLine);
  int dummy1, dummy2, dummy3, dummy4, volumeID, materialID;
  iss >> dummy1 >> dummy2 >> dummy3 >> dummy4 >> volumeID >> materialID;
  return {volumeID, materialID};
}


vector<double> MCNPGeometry::readPoint() {
  getline(ptracFile, currentLine);
  istringstream iss(currentLine);
  double pointX, pointY, pointZ;
  iss >> pointX >> pointY >> pointZ;
  return {pointX, pointY, pointZ};
}


int MCNPGeometry::readNextPtracData(int maxReadPoint) {
  if(ptracFile && !ptracFile.eof() && getnPointsRead() < maxReadPoint){
    incrementnPointsRead();
    setPointEvent(readPointEvent());
    setCellMaterial(readCellMaterial());
    setPointXyz(readPoint());
    return 1;
  }
  else{
    return 0;
  }
}


void MCNPGeometry::readMaterialDensity(){
  istringstream iss(currentLine);
  int cellNum;
  string density;
  if (iss >> cellNum){
    int matNum;
    iss >> matNum;
    if(matNum == 0){
      addCell2Density(cellNum, "void");
    }
    else{
      iss >> density;
      addCell2Density(cellNum, density);
    }
  }
}

void MCNPGeometry::addCell2Density(int key, const string& value){
  if (cell2Density.find(key) == cell2Density.end()){
    cell2Density[key] = value;
  }
}


void MCNPGeometry::parseINP() {
  if (inputFile){
    while(getline(inputFile, currentLine, '\n')){
      if (finishedReadingCells()){
        break;
      }
      if (!isLineAComment(currentLine) && isdigit(currentLine[0])){
        readMaterialDensity();
      }
    }
  }
  readNPS();
}

void MCNPGeometry::readNPS() {
  string dummy;
  if (inputFile){
    while(getline(inputFile, currentLine)){
      if (currentLine.find("NPS") != string::npos){
        istringstream iss(currentLine);
        int nps;
        iss >> dummy >> nps;
        this->nps = nps;
        break;
      }
    }
  }
}

void MCNPGeometry::goThroughHeaderPTRAC(int nHeaderLines){
  for (int ii=0; ii<nHeaderLines; ii++){
    getline(ptracFile, currentLine);
  }
}


int MCNPGeometry::finishedReadingCells(){
  return currentLine.length() == 1 || currentLine.empty();
}


int MCNPGeometry::isLineAComment(string lineContent){
  return lineContent[0] == 'c' || lineContent[0] == 'C';
}

void MCNPGeometry::incrementnPointsRead(){
  setnPointsRead(nPointsRead+1);
}

string MCNPGeometry::getMaterialDensity(){
  string density = cell2Density[cellID];
  return (to_string(materialID)+density);
}


ifstream& MCNPGeometry::getInputFile() {
  return inputFile;
}

const string& MCNPGeometry::getInputPath(){
  return inputPath;
}

void MCNPGeometry::setInputPath(const string& inputPath) {
  this->inputPath = inputPath;
}

int MCNPGeometry::getNPS(){
  return nps;
}

int MCNPGeometry::getnPointsRead() {
  return nPointsRead;
}

void MCNPGeometry::setnPointsRead(int nPointsRead){
  this->nPointsRead = nPointsRead;
}

const string& MCNPGeometry::getPtracPath() {
  return ptracPath;
}

string MCNPGeometry::getCurrentLine(){
  return currentLine;
}

int MCNPGeometry::getPointID() {
  return pointID;
}

int MCNPGeometry::getEventID() {
  return eventID;
}

void MCNPGeometry::setPointEvent(const pair<int, int>& pointEvent) {
  this->pointID = pointEvent.first;
  this->eventID = pointEvent.second;
}

vector<double> MCNPGeometry::getPointXyz() {
  return pointXYZ;
}

void MCNPGeometry::setPointXyz(const vector<double>& pointXyz) {
  pointXYZ = pointXyz;
}

int MCNPGeometry::getCellID() {
  return cellID;
}

int MCNPGeometry::getMaterialID() {
  return materialID;
}

void MCNPGeometry::setCellMaterial(const pair<int, int>& cellMat) {
  this->cellID = cellMat.first;
  this->materialID = cellMat.second;
}

map<int, string>& MCNPGeometry::getCell2Density(){
  return cell2Density;
}
