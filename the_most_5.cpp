#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <time.h>
#include <map>
#include <unordered_set>
#include <unordered_map>
using namespace std;


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



struct Info {
	double num;
	int index;
	Info* next=nullptr;
	Info(double n, int id) :num(n), index(id) {}
};
Info ListStart(0,0);
multimap<double, Info> mp;
unordered_set<double>checkMp;
void resetCM() {
	checkMp.clear();
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
		mp.insert(pair<double, Info>(num, { num,index }));
	}
	Info* last = &ListStart;
		for (auto iter = mp.begin(); iter != mp.end(); iter++) {
			last->next = &iter->second;
			last = last->next;
		}
	return;
}

bool check[10000] = { false };
int countHit[10000] = { 0 };
vector<bool*> resetCheckList;
void resetCheck() {
	for (int i = 0; i < resetCheckList.size();i++) {
		*resetCheckList[i] = false;
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
	std::ios::sync_with_stdio(false);
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
			resetCheck();
			auto iter = mp.upper_bound(num - 0.01);
			Info* n_info = &iter->second;
			double upperB = num + 0.01;
			while (n_info && n_info->num < upperB) {
				int id = n_info->index;
				if (check[id]) {
					n_info = n_info->next;
					continue;
				}
				if (checkMp.find((double)(id<<12)+n_info->num) != checkMp.end()) {
					n_info = n_info->next;
					continue;
				}
				check[id] = true;
				resetCheckList.push_back(&check[id]);
				checkMp.insert((double)(id<<12)+n_info->num);
				countHit[id]++;
				n_info = n_info->next;
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


	ofstream fout("rr.txt");
	for (int i = 0; i < 1000; i++) {
		fout << res[i][0] << '\t' << res[i][1] << endl;
	}

  clock_t cptOver = clock();
	std::cout << "compute:" << (double)(cptOver-readOver) / CLOCKS_PER_SEC << endl;
	return 0;
}


