using namespace std;
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <time.h>
#include <assert.h>
#include <cmath>
#include <optional>



class norm_trade{
    public:

    string stock;

    double open_price;

    double necessary_open;
    double necessary_close;



    norm_trade(){
        
    }
    norm_trade(ifstream &in){

        string line;
        getline(in,line);
        stringstream ss(line);
        // read in trade in this format
        ss >> stock >>open_price >> necessary_open >> necessary_close;


    }
    double tick(double price, double curr_indicator){
        // profit/loss value
        double curr_pl = necessary_open > 0 ?
                        open_price - price :
                        price - open_price;
        if ((curr_indicator <= necessary_close && necessary_close >=0) ||
            (curr_indicator >= necessary_close && necessary_close <=0)){
            return curr_pl;
        }
        return -INT16_MAX;
    }
};