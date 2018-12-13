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
#include <cctype>

MCNPGeometry::MCNPGeometry(string ptracPath, string inputPath) {
	npoints = 0;
	volumeList = {};

	this->ptracPath=ptracPath;
	this->inputPath=inputPath;
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
	// TODO Auto-generated destructor stub
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


vector<float> MCNPGeometry::readPoint() {
	getline(ptracFile, currentLine);
	istringstream iss(currentLine);
	float pointX, pointY, pointZ;
	iss >> pointX >> pointY >> pointZ;
	return {pointX, pointY, pointZ};
}


int MCNPGeometry::readNextPtracData(int maxReadPoint) {
	if(ptracFile && !ptracFile.eof() && getNpoints() < maxReadPoint){
		incrementNpoints();
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
	int cellNum, matNum;
	string density;
	if (iss >> cellNum){
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

void MCNPGeometry::addCell2Density(int key, string value){
	if (cell2Density.find(key) == cell2Density.end()){
		cell2Density[key] = value;
	}
}


void MCNPGeometry::parseINP() {
	if (inputFile){
		while(getline(inputFile, currentLine)){
			if (!isLineAComment(currentLine) && isdigit(currentLine[0])){
				readMaterialDensity();
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
	if(getline(inputFile, currentLine)){
		return currentLine.length() == 0;
	}
	else{
		return 0;
	}
}


int MCNPGeometry::isLineAComment(string lineContent){
	return lineContent[0] == 'c' || lineContent[0] == 'C';
}
