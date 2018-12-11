/*
 * MCNPGeometry.h
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
	pair<int, int> pointEvent;
	pair<int, int> volumeMat;
	vector<float> pointXYZ;

	map<int, string> cell2Density;

	vector<int> volumeList;
	int npoints;
	string ptracPath;
	string inputPath;
	string currentLine;
	ifstream ptracFile;
	ifstream inputFile;



public:
	MCNPGeometry();
	MCNPGeometry(string ptracPath, string inputPath);
	virtual ~MCNPGeometry();
	pair<int, int> readPointEvent();
	pair<int, int> readVolumeMaterial();
	vector<float> readPoint();
	void readNextPtracData(int maxReadPoint=1000000000);

	int readMaterialDensity();
	void parseINP();

	void goThroughHeaderPTRAC(int nHeaderLines);

	ifstream& getInputFile() {
		return inputFile;
	}

	const string& getInputPath() const{
		return inputPath;
	}

	void setInputPath(const string& inputPath) {
		this->inputPath = inputPath;
	}

	int getNpoints() const {
		return npoints;
	}

	void setNpoints(int npoints){
		this->npoints = npoints;
	}

	ifstream& getPtracFile() {
		return ptracFile;
	}

	const string& getPtracPath() const {
		return ptracPath;
	}

	void setPtracPath(const string& ptracPath) {
		this->ptracPath = ptracPath;
	}

	const vector<int>& getVolumeList() const {
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

	const pair<int, int>& getPointEvent() const {
		return pointEvent;
	}

	void setPointEvent(const pair<int, int>& pointEvent) {
		this->pointEvent = pointEvent;
	}

	const vector<float>& getPointXyz() const {
		return pointXYZ;
	}

	void setPointXyz(const vector<float>& pointXyz) {
		pointXYZ = pointXyz;
	}

	const pair<int, int>& getVolumeMaterial() const {
		return volumeMat;
	}

	void setVolumeMaterial(const pair<int, int>& volumeMat) {
		this->volumeMat = volumeMat;
	}

	void incrementNpoints(){
		setNpoints(npoints+1);
	}

	map<int, string>& getCell2Density(){
		return cell2Density;
	}

	int finishedReadingCells();

	int isLineAComment(string lineContent);

};


#endif /* MCNPGEOMETRY_H_ */
