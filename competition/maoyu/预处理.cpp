#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <fstream>
#include <iostream>
#include <map>
using namespace std;
string s;
int phone, year, mouth, date, hour, loc_id;
int t[50][50][50];
int main() {
	//for (int mouth_ = 1; mouth_ <= 10; mouth_++) {
	//	memset(t, 0, sizeof(t));
	//	s.clear();
		/*if (mouth_ <= 9) {
			s = "00.csv";
			s[1] = mouth_ + '0';
			freopen(s.c_str(), "r", stdin);
			s = "00.out.csv";
			s[1] = mouth_ + '0';
			freopen(s.c_str(), "w", stdout);
		}
		else {
			s = "10.csv";
			s[1] = mouth_ - 10 + '0';
			freopen(s.c_str(), "r", stdin);
			s = "10.out.csv";
			s[1] = mouth_ + '0';
			freopen(s.c_str(), "w", stdout);
		}*/
		freopen("11.out.csv", "w", stdout);
		freopen("11.csv", "r", stdin);

		scanf("%s\n", &s);
		printf("loc_id,time_stamp,num_of_people\n");
		while (scanf("%d,%d-%d-%d %d,%d", &phone, &year, &mouth, &date, &hour, &loc_id)>0) {	
			t[date][hour][loc_id]++;
		}

		for (int date_ = 1; date_ <= 30; date_++) {
			for (int hour_ = 0; hour_ <= 23; hour_++) {
				for (int loc_ = 1; loc_ <= 33; loc_++) {
					printf("%d,2017-11", loc_);

					if (date_ <= 9)printf("-0%d ", date_);
					else printf("-%d ", date_);

					if (hour_ == 0)printf("00,%d\n", t[date_][hour_][loc_]);
					else if (hour_ <= 9)printf("0%d,%d\n", hour_, t[date_][hour_][loc_]);
					else printf("%d,%d\n", hour_, t[date_][hour_][loc_]);
				}
			}
		}

		fclose(stdin);
		fclose(stdout);
		return 0;
	//}
}