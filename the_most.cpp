#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <time.h>
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

void getMaxSim(vector<vector<double>>& s,int si, vector<vector<double>>& p) {
	vector<double>& ss = s[si];
	int spoint = 0;
	int sims[10000] = { 0 };
	int points[10000] = { 0 };
	for (spoint = 0; spoint < ss.size(); spoint++) {
		for (int pi = 0; pi < 10000; pi++) {
			int& ppoint = points[pi];
			vector<double>& pp = p[pi];
			if (ppoint >= pp.size())
				continue;
			while (pp[ppoint] + 0.01 < ss[spoint]) {
				if (ppoint < pp.size())
					ppoint++;
				if (ppoint >= pp.size())
					break;
			}
			double tmp = pp[ppoint] - ss[spoint];
			if (tmp <= 0.01&&tmp >= -0.01) {
				ppoint++;
				sims[pi]++;
				continue;
			}
		}
	}
	int max = 0;
	int maxIter = 0;
	for (int i = 0; i < 10000; i++) {
		if (max < sims[i]) {
			max = sims[i];
			maxIter = i;
		}
	}
	res[si][0] = maxIter+1;
	res[si][1] = max;
}


void getMaxSim2(vector<vector<double>>& s, int si, vector<vector<double>>& p) {
	int max = 0;
	int maxIter = 0;
	vector<double>& ss = s[si];
	for (int pi = 0; pi < 10000; pi++) {
		int sim = 0;
		vector<double>pp = p[pi];
		unsigned int ppi = 0;
		for (int sp = 0; sp < 1000; sp++) {
			double sn = ss[sp];
			while (pp[ppi] + 0.01 < sn) {
				ppi++;
				if (ppi >= pp.size())
					break;
			}
			if (ppi >= pp.size())
				break;
			double m = pp[ppi] - sn;
			if ((m > -0.01) && (m < 0.01)) {
				ppi++;
				sim++;
			}
		}
		if (max < sim) {
			max = sim;
			maxIter = pi;
		}
	}
	res[si][0] = maxIter + 1;
	res[si][1] = max;
}

void getMaxSim3(vector<vector<double>>& s, int si, vector<vector<double>>& p) {
	int max = 0;
	int maxIter = 0;
	vector<double>& ss = s[si];
	for (int pi = 0; pi < 10000; pi++) {
		int sim = 0;
		vector<double>pp = p[pi];
		unsigned int ppi = 0;
		for (int sp = 0; sp < 1000; sp++) {
			double sn = ss[sp];
			while (pp[ppi] + 0.01 < sn) {
				ppi++;
				if (ppi >= pp.size())
					break;
			}
			if (ppi >= pp.size())
				break;
			double m = pp[ppi] - sn;
			if ((m > -0.01) && (m < 0.01)) {
				ppi++;
				sim++;
			}
      if((sim+1000-sp)<max){
        break;
      }
		}
		if (max < sim) {
			max = sim;
			maxIter = pi;
		}
	}
	res[si][0] = maxIter + 1;
	res[si][1] = max;
}


int main()
{
	clock_t start=clock();
	ifstream pin("P.txt");
	vector<vector<double>> p;
	p.reserve(10000);
	getInput(p, pin);
	ifstream sin("S.txt");
	vector<vector<double>> s;
	s.reserve(1000);
	getInput(s, sin);
	clock_t readOver = clock();
	cout << "readFile:" << (readOver - start) / (double)CLOCKS_PER_SEC << endl;
	clock_t As = clock();
	clock_t Ae;
	for (int i = 0; i < 1000; i++) {
		getMaxSim(s,i, p);
	}	
	Ae = clock();
	cout << "compute:" << (Ae - As) / (double)CLOCKS_PER_SEC << endl;
 
 	As = clock();
	for (int i = 0; i < 1000; i++) {
		getMaxSim2(s,i, p);
	}	
	Ae = clock();
	cout << "compute:" << (Ae - As) / (double)CLOCKS_PER_SEC << endl;
 
  As = clock();
	for (int i = 0; i < 1000; i++) {
		getMaxSim3(s,i, p);
	}	
	Ae = clock();
	cout << "compute:" << (Ae - As) / (double)CLOCKS_PER_SEC << endl;
	ofstream fout("rr.txt");
	for (int i = 0; i < 1000; i++) {
		fout << res[i][0] << '\t' << res[i][1] << endl;
	}
	return 0;
}
