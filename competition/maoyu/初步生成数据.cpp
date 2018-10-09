#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <fstream>
#include <iostream>
#include <map>
#include <vector>
using namespace std;
#define max__(a,b) (a>b?a:b)
#define min__(a,b) (a<b?a:b)

string s;
int phone, year, mouth, date, hour, loc_id, number;
int t[50][50][50];
vector<int> days[10][50][50];//day,loc,hour
int week[10][50][50];//day,loc,hour
int people[7] = { 4343,
5629,
5682,
5485,
5534,
5392,
4235,
};
int peopleofday[7] = { 4450,
5720,
5743,
5488,
5672,
5357,
4237,
};

int main() {
	freopen("12.out.csv", "w", stdout);
	freopen("11.out.csv", "r", stdin);

	scanf("%s\n", &s);
	printf("loc_id,time_stamp,num_of_people\n");

	while (scanf("%d,%d-%d-%d %d,%d", &loc_id, &year, &mouth, &date, &hour, &number) > 0) {
		t[date][hour][loc_id] = number;
	}

	int whichday;
	for (int date_ = 1; date_ <= 30; date_++) {
		whichday = (date_ + 2) % 7;
		for (int hour_ = 0; hour_ <= 23; hour_++) {
			for (int loc_ = 1; loc_ <= 33; loc_++) {
				if (t[date_][hour_][loc_] == 0)continue;
				days[whichday][loc_][hour_].push_back(t[date_][hour_][loc_]);
			}
		}
	}

	int cache,cache1,maxx,minn;

	for (int date_ = 0; date_ <= 6; date_++) {
		for (int hour_ = 0; hour_ <= 23; hour_++) {
			for (int loc_ = 1; loc_ <= 33; loc_++) {
				if (days[date_][loc_][hour_].size() == 0) {
					days[date_][loc_][hour_].push_back(0);
				}
			}
		}
	}

	for (int date_ = 0; date_ <= 6; date_++) {
		for (int hour_ = 0; hour_ <= 23; hour_++) {
			for (int loc_ = 1; loc_ <= 33; loc_++) {
				cache = 0;
				maxx = 0;
				minn = 10000000;
				cache1 = 0;
				for (int i = 0; i < days[date_][loc_][hour_].size(); i++) {
					maxx = max__(maxx, days[date_][loc_][hour_][i]);
					minn = min__(minn, days[date_][loc_][hour_][i]);
					cache += days[date_][loc_][hour_][i]/**(i+4)*/;
					cache1 += 1/*i+4*/;
				}
				week[date_][loc_][hour_] =  cache/cache1;
			}
		}
	}

	for (int date_ = 1; date_ <= 31; date_++) {
		whichday = (date_ + 4) % 7;
		for (int hour_ = 0; hour_ <= 23; hour_++) {
			for (int loc_ = 1; loc_ <= 33; loc_++) {
				printf("%d,2017-12", loc_);

				if (date_ <= 9)printf("-0%d ", date_);
				else printf("-%d ", date_);

				//int nowpeople = (week[whichday][loc_][hour_]*2+ days[whichday][loc_][hour_][(date_/(30 / days[whichday][loc_][hour_].size()))>(days[whichday][loc_][hour_].size()-1)? (days[whichday][loc_][hour_].size() - 1): (date_ / (30 / days[whichday][loc_][hour_].size()))])/3;

				if (hour_ <= 9) {
					/*if (date_%10==0&&hour_<=7) printf("0%d,%d\n", hour_, 0);
					else*/ printf("0%d", hour_);
				}
				else {
					 printf("%d", hour_);
				}
				printf(",%d\n", week[whichday][loc_][hour_] /**peopleofday[whichday]/people[whichday]/*nowpeople*/);
			}
		}
	}

	fclose(stdin);
	fclose(stdout);
	return 0;
}