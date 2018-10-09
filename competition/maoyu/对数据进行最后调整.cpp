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
#define pf(a) ((a)*(a))

string s;
int phone, year, mouth, date, hour, loc_id, number;
int t[50][50][50];

int main() {
	freopen("12.final.csv", "w", stdout);
	freopen("12.out.csv", "r", stdin);

	scanf("%s\n", &s);
	printf("loc_id,time_stamp,num_of_people\n");

	while (scanf("%d,%d-%d-%d %d,%d", &loc_id, &year, &mouth, &date, &hour, &number) > 0) {
		t[date][hour][loc_id] = number;
	}
	double percent = 0;
	double percentcache;
	long long  cache = 0;
	long long  lastcache = 0;
	for (percentcache = 1; percentcache <= 200; percentcache++) {
		cache = 0;
		for (int date_ = 1; date_ <= 31; date_++) {
			for (int hour_ = 0; hour_ <= 23; hour_++) {
				for (int loc_ = 1; loc_ <= 33; loc_++) {
					cache += pf(trunc((long long)t[date_][hour_][loc_] * ((percent + percentcache) / 100)));
				}
			}
		}
		if (sqrt((double)cache / 24552)  > 1045.2566&&sqrt((double)lastcache / 24552)  < 1045.2566) {
			lastcache = cache;
			break;
		}
		lastcache = cache;
	}
	percent+=--percentcache;
	percentcache = 1;
	int j;
	for (int i = 1; i <= 10; i++) {
		percentcache /= 10;
		for (j = 0; j <= 10; j++) {
			cache = 0;
			for (int date_ = 1; date_ <= 31; date_++) {
				for (int hour_ = 0; hour_ <= 23; hour_++) {
					for (int loc_ = 1; loc_ <= 33; loc_++) {
						cache += pf(trunc((long long)t[date_][hour_][loc_] * ((percent + percentcache*j) / 100)));
					}
				}
			}
			if (sqrt((double)cache / 24552)  > 1045.2566&&sqrt((double)lastcache / 24552)  < 1045.2566) {
				lastcache = cache;
				break;
			}
			lastcache = cache;
		}
		percent += percentcache*(--j);
	}
	for (int date_ = 1; date_ <= 31; date_++) {
		for (int hour_ = 0; hour_ <= 23; hour_++) {
			for (int loc_ = 1; loc_ <= 33; loc_++) {
				printf("%d,2017-12", loc_);

				if (date_ <= 9)printf("-0%d ", date_);
				else printf("-%d ", date_);

				if (hour_ <= 9) {
					printf("0%d", hour_);
				}
				else printf("%d", hour_);

				printf(",%d\n", (int)trunc((double)t[date_][hour_][loc_]*percent/100));
			}
		}
	}

	fclose(stdin);
	fclose(stdout);
	return 0;
}