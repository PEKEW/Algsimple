#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <time.h>
#include <map>
#include <unordered_map>
using namespace std;

#define hashMultiplu 10

void getInput(vector<vector<double>>& s, ifstream& i) {
	string a;
	vector<double> v;
	while (i >> a) {
		if (a[0] == '#') {
			if (!v.empty()) {
				s.push_back(v);
				v.clear();
			}
		}
		else {
			v.push_back(stod(a));
		}
	}
	s.push_back(v);
	return;
}

int res[1000][2] = { 0 };

multimap<double, int> mp[10000/hashMultiplu];
unordered_map<double, bool>checkMp[10000];
vector<bool*> resetList;
void resetCM() {
	for (int i = 0; i < resetList.size();i++) {
		*resetList[i] = false;
	}
	resetList.clear();
}

void initMap(ifstream& i) {
	string a;
	int index = -1;
	bool ret = false;
	while (i >> a) {
		if (a[0] == '#') {
			index++;
			continue;
		}
		double num = stod(a);
		mp[(int)(num)/hashMultiplu].insert(pair<double, int>(num,index));
		checkMp[index].insert(pair<double, int>(num, false));
	}
	return;
}

int check[10001] = { 0 };
int countHit[10000] = { 0 };
vector<int*> resetCheckList;
void resetCheck() {
	for (int i = 0; i < resetCheckList.size();i++) {
		*resetCheckList[i] = 0;
	}
	resetCheckList.clear();
	return;
}
void resetCountHit() {
	for (int i = 0; i < 10000; i++) {
		if (countHit[i])
			countHit[i] = 0;
	}
	return;
}
int main() {
	clock_t start = clock();
	ifstream pin("P.txt");
	initMap(pin);

	ifstream sin("S.txt");
	vector<vector<double>> s;
	s.reserve(1000);
	getInput(s, sin);
	clock_t readOver = clock();
	std::cout << "readFile:" << (double)(readOver - start) / CLOCKS_PER_SEC << endl;
	for (int si = 0; si < 1000; si++) {
		resetCM();
		resetCountHit();
		vector<double>& ss = s[si];
		int max = 0;
		int maxIter = 0;

		for (auto num : ss) {
			int Znum = (int)num/hashMultiplu;
			resetCheck();
			auto iter = mp[Znum].upper_bound(num - 0.01);
			while (iter != mp[Znum].end() && iter->first < (num + 0.01)) {
				int id = iter->second;
				if (check[id]) {
					iter++;
					continue;
				}
				if (checkMp[id][iter->first]) {
					iter++;
					continue;
				}
				check[id] = true;
				resetCheckList.push_back(&id);
				checkMp[id][iter->first] = true;
				resetList.push_back(&checkMp[id][iter->first]);
				countHit[id]++;
				iter++;
			}
		}

		for (int i = 0; i < 10000; i++) {
			if (max < countHit[i]) {
				max = countHit[i];
				maxIter = i + 1;
			}
		}
		res[si][0] = maxIter;
		res[si][1] = max;
	}

	clock_t cptOver = clock();
	std::cout << "compute:" << (double)(cptOver-readOver) / CLOCKS_PER_SEC << endl;
	ofstream fout("rr.txt");
	for (int i = 0; i < 1000; i++) {
		fout << res[i][0] << '\t' << res[i][1] << endl;
	}
	return 0;
}
