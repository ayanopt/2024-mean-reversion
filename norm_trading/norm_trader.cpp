using namespace std;
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <time.h>
#include <sstream>
#include <fstream>
#include <assert.h>
#include <cmath>
#include <cstdio>
#include <optional>
#include "unordered_map"
#include "trade.h"
#include <ctime>

struct strat{
    double necessary_open;
    double necessary_close;
    strat(double necessary_open_in, double necessary_close_in): 
     necessary_open(necessary_open_in), necessary_close(necessary_close_in) {}
};

vector<strat> target_strats = {
    strat(0.70547,0.51837),
    strat(0.51837,0.34083),
    strat(1.13223,0.90739),
    strat(1.13223,0.70547),
    strat(2.21282,1.9366),
    strat(2.21282,1.72407),
    strat(3.12963,0.51837),
    strat(3.12963,0.90739),
    strat(3.12, 2),
    strat(3.5, 2)
};
vector<int> get_todays_strats() {
    std::time_t t = std::time(0);
    
    // Convert to tm struct
    std::tm* now = std::localtime(&t);

    // Get the current day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    int day_of_week = now->tm_wday;

    // Map days to strats

    return {(2*day_of_week)-2, (2*day_of_week)-1};
}
int main(int argc, char **argv){
    assert(argc == 4);
    // strats, currently manually inputted, follows (window, profit taking diff, indicator value)

    double a_price(stod(string(argv[1])));
    string a_name(argv[2]);
    
    // Only trading SPY for now
    assert(a_name == "SPY");
    double norm(stod(string(argv[3])));

    for (int i : get_todays_strats()){
        auto &curr_strat = target_strats[i];
        double div;
        int dir = 0;
        bool update = false;
        // if indicator is above/below threshold
        if (abs(norm) >= curr_strat.necessary_open){ 
            div = norm;
            dir = norm/abs(norm);
            update = true;  
        }

        string open_file = "./trades/"+a_name + "_" + to_string(i) + "_trade.txt";

        ifstream trade(open_file.c_str());
        norm_trade* curr_trade = nullptr;
        // determine format of output file -> in trade.hs
        if (trade.good()){
            norm_trade* tmp = new norm_trade(trade);
            curr_trade = tmp;
            dir = tmp->necessary_open/abs(tmp->necessary_open);
        }
        // if trade exists: tick
        bool trade_closed = false;
        if (trade.good()){
            // use current price for tick
            auto out = curr_trade->tick(a_price,norm);
            // revert to original trade prices for output
            //default output is int_max, if not it is a successful trade
            if (out != -INT16_MAX){
                string cap_file = "./capital/"+a_name+"_"+to_string(i)+"_capital.txt";
                ifstream capital(cap_file.c_str());
                double pl = 0;
                if (capital.good()){
                    string jnk;
                    getline(capital,jnk);
                    pl = stod(jnk);
                    capital.close();
                }
                pl += out;

                system(("echo " + to_string(pl)+" > "+cap_file).c_str());
            }

            if (curr_trade) delete curr_trade;            

            update = true;
            if (out != -INT16_MAX){
                // delete trade
                system(("rm " + open_file).c_str());
                update = false;
                trade_closed = true;
            }
            trade.close();
        } 
        // trade doesn't exist, and direction is positive, buy to open.
        // trade exists and direction is negative, buy to close
        // so on
        if ((!trade.good() && update) || (trade_closed)){
            string open_or_close = !trade_closed ? "open" : "close";
            string buy_or_sell = ((dir < 0 && !trade_closed) ||
                                    (dir>0 && trade_closed)) ?
                                        "buy" : "sell";
            system(("python3 ../trade_operations/norm_trade.py "
                                + a_name + " "
                                + to_string(i) + " "
                                + buy_or_sell + " "
                                + open_or_close +" &").c_str());
        }
        // update the trade file
        if (update){
            // price name open close
            string command = "echo " + a_name+ " " + to_string(a_price) + " "
                    + to_string(dir*curr_strat.necessary_open) + " " + to_string(dir*curr_strat.necessary_close) + " >"+open_file;

            system(command.c_str());
        }
    }
}