/*
 * MCNPGeometry.hh
 *
 *  Created on: 7 d�c. 2018
 *      Author: jofausti
 */

#ifndef MCNPGEOMETRY_H_
#define MCNPGEOMETRY_H_

#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <map>

using namespace std;

class MCNPGeometry {
	int pointID;
	int eventID;
	int cellID;
	int materialID;
	vector<float> pointXYZ;

	map<int, string> cell2Density;

	vector<int> volumeList;
	int npoints;
	string ptracPath;
	string inputPath;

	ifstream ptracFile;
	ifstream inputFile;
	string currentLine;
public:
	MCNPGeometry();
	MCNPGeometry(string ptracPath, string inputPath);
	virtual ~MCNPGeometry();
	pair<int, int> readPointEvent();
	pair<int, int> readCellMaterial();
	vector<float> readPoint();
	int readNextPtracData(int maxReadPoint=1000000000);

	void readMaterialDensity();
	void parseINP();

	void goThroughHeaderPTRAC(int nHeaderLines);

	ifstream& getInputFile() {
		return inputFile;
	}

	const string& getInputPath(){
		return inputPath;
	}

	void setInputPath(const string& inputPath) {
		this->inputPath = inputPath;
	}

	int getNpoints() {
		return npoints;
	}

	void setNpoints(int npoints){
		this->npoints = npoints;
	}

	ifstream& getPtracFile() {
		return ptracFile;
	}

	const string& getPtracPath() {
		return ptracPath;
	}

	void setPtracPath(const string& ptracPath) {
		this->ptracPath = ptracPath;
	}

	const vector<int>& getVolumeList() {
		return volumeList;
	}

	void setVolumeList(const vector<int>& volumeList) {
		this->volumeList = volumeList;
	}

	string getCurrentLine(){
		return currentLine;
	}

	int setCurrentLine(ifstream& inFile){
		if(getline(inFile, currentLine)){
			return 1;
		}
		else{
			return 0;
		}
	}

	int getPointID() {
		return pointID;
	}

	int getEventID() {
		return eventID;
	}

	void setPointEvent(const pair<int, int>& pointEvent) {
		this->pointID = pointEvent.first;
		this->eventID = pointEvent.second;
	}

	const vector<float>& getPointXyz() const {
		return pointXYZ;
	}

	void setPointXyz(const vector<float>& pointXyz) {
		pointXYZ = pointXyz;
	}

	int getCellID() {
		return cellID;
	}

	int getMaterialID() {
		return materialID;
	}

	void setCellMaterial(const pair<int, int>& cellMat) {
		this->cellID = cellMat.first;
		this->materialID = cellMat.second;
	}

	void incrementNpoints(){
		setNpoints(npoints+1);
	}

	map<int, string>& getCell2Density(){
		return cell2Density;
	}

	void addCell2Density(int key, string value);

	string getMaterialDensity(){
		string density = cell2Density[cellID];
		return (to_string(materialID)+density);
	}

	int finishedReadingCells();

	int isLineAComment(string lineContent);

};


#endif /* MCNPGEOMETRY_H_ */
