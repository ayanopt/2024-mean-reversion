using namespace std;
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <time.h>
#include <assert.h>
#include "stock.h"
#include <unistd.h>


int main(int argc, char **argv){
    assert(argc == 2);
    string a_name(argv[1]);

    stock a_stock(a_name);
    // initialize
    for (int i = 0; i<120; i++){
        a_stock.update();
        usleep(10000000); 
        //usleep(10000000); 
    }

    for (int i = 0; i<2200; i++){
        // add stock price to array
        a_stock.update();
        
        system(("./norm_trader.o " + to_string(*a_stock.prices.rbegin()) + " "
                     +a_stock.stock_name + " "+  to_string(*a_stock.std_prices.rbegin()) + " &").c_str());

        usleep(10000000);


    }
    system("rm ./trades/*");
    return 0;
}
