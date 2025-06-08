using namespace std;
#include <fstream>
#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <unistd.h>
#include <time.h>
#include <assert.h>
#include "calcs.h"


class stock{
    public:
    vector<double> prices;
    vector<double> std_prices;
    string stock_name;
    stock(string name_in): stock_name(name_in) {}
    int n_fails = 0;
    double get_current_std(){
        // standardize prices -> (x-mean)/std
        return (*prices.rbegin() - mean(prices))/stdev(prices);
    }
    void pop_front(vector<double> &in){
        vector<double> new_vector(in.begin()+1, in.end());
        in = new_vector;
    }

    void update(){
        // get price from price update folder
        string out_file = "../prices/" + stock_name + "_out.txt";
        fstream reader;
        reader.open(out_file);
        assert(reader.good());
        string curr;
        getline(reader, curr);
        double price;
        // possible to not open price because of silly timing problems ----improvement area
        try{
            price = stod(curr);
        }
        catch(...){ // TODO: oof fix this logic 
            if (prices.size() > 0) price = *prices.rbegin();
            else {
                n_fails++;
                if (n_fails > 10){
                    throw std::runtime_error("Redo update");
                }
                usleep(3000000);
                update();
            }
        }
        reader.close();

        prices.push_back(price);
        // possible to standardize
        if (prices.size() > 60){
            std_prices.push_back(get_current_std());
            pop_front(prices);
        }
        // possible to compute stat arb
        if (std_prices.size() > 60){
            pop_front(std_prices);
        }
    

    }

};