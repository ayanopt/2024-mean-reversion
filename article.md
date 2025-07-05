# Statistical Arbitrage Through Normalized Price Deviation: A Mean-Reversion Trading Algorithm

## Abstract

This paper presents a systematic trading algorithm that exploits short-term price deviations from statistical norms in equity markets. The algorithm employs a normalized price deviation strategy based on rolling window standardization and dynamic threshold-based position management. Through real-time price monitoring and statistical analysis, the system identifies trading opportunities when asset prices deviate significantly from their recent statistical mean. While the strategy demonstrates consistent profitability under normal market conditions, it exhibits vulnerability to regime changes where statistical outliers represent the beginning of sustained directional trends rather than temporary deviations.

**Keywords:** Statistical arbitrage, mean reversion, algorithmic trading, normalized price deviation, risk management

## 1. Introduction

Statistical arbitrage strategies have long been employed in quantitative finance to exploit temporary price inefficiencies in financial markets. These strategies typically rely on the assumption that asset prices exhibit mean-reverting behavior over short time horizons, allowing traders to profit from temporary deviations from statistical norms.

This paper examines a real-time trading algorithm that implements a normalized price deviation strategy for equity trading. The system operates on the principle that when an asset's price deviates significantly from its recent statistical mean (measured in standard deviations), it will likely revert to the mean, creating profitable trading opportunities.

## 2. Methodology

### 2.1 System Architecture

The trading system follows a modular architecture consisting of four primary components:

1. **Price Stream Module** (`stream_wrapper.py`): Real-time price data acquisition via Alpaca API
2. **Data Processing Module** (`norm_data_loader.cpp`): Statistical analysis and normalization
3. **Trading Logic Module** (`norm_trader.cpp`): Decision-making and position management
4. **Execution Module** (`norm_trade.py`): Order placement and portfolio management

### 2.2 Statistical Framework

#### 2.2.1 Price Normalization

The core statistical methodology centers on price normalization using a rolling window approach. For each asset price $P_t$ at time $t$, the normalized price deviation $Z_t$ is calculated as:

$$Z_t = \frac{P_t - \mu_{60}}{\sigma_{60}}$$

where:
- $\mu_{60}$ is the 60-period rolling mean: $\mu_{60} = \frac{1}{60}\sum_{i=t-59}^{t} P_i$
- $\sigma_{60}$ is the 60-period rolling standard deviation: $\sigma_{60} = \sqrt{\frac{1}{60}\sum_{i=t-59}^{t}(P_i - \mu_{60})^2}$

This normalization transforms price movements into standardized units, allowing for consistent threshold-based decision making regardless of the absolute price level of the underlying asset.

#### 2.2.2 Correlation-Based Divergence Calculation

The system implements an additional divergence metric that incorporates correlation analysis:

$$D_t = \frac{V_t}{e^{\rho_t - 1}}$$

where:
- $V_t$ represents the current price deviation value
- $\rho_t$ is the correlation coefficient between recent price movements
- The exponential transformation $e^{\rho_t - 1}$ serves as a volatility adjustment factor

This formulation ensures that $\rho_t - 1 \leq 0$, making $e^{\rho_t - 1} \leq 1$, which amplifies the divergence signal when correlation is low.

### 2.3 Trading Strategy Implementation

#### 2.3.1 Multi-Strategy Framework

The algorithm employs multiple concurrent strategies with varying threshold parameters. Each strategy $i$ is defined by two key parameters:

- **Opening Threshold** ($\theta_{open,i}$): Minimum normalized deviation required to initiate a position
- **Closing Threshold** ($\theta_{close,i}$): Maximum normalized deviation for position closure

The implemented strategy parameters are:

| Strategy | $\theta_{open}$ | $\theta_{close}$ |
|----------|-----------------|------------------|
| 0        | 0.70547        | 0.51837         |
| 1        | 0.51837        | 0.34083         |
| 2        | 1.13223        | 0.90739         |
| 3        | 1.13223        | 0.70547         |
| 4        | 2.21282        | 1.93660         |
| 5        | 2.21282        | 1.72407         |
| 6        | 3.12963        | 0.51837         |
| 7        | 3.12963        | 0.90739         |
| 8        | 3.12000        | 2.00000         |
| 9        | 3.50000        | 2.00000         |

#### 2.3.2 Position Management Logic

For each strategy $i$, the trading logic follows this decision tree:

1. **Position Opening**: If $|Z_t| \geq \theta_{open,i}$ and no position exists:
   - If $Z_t > 0$: Short position (expecting mean reversion downward)
   - If $Z_t < 0$: Long position (expecting mean reversion upward)

2. **Position Closing**: If position exists and $|Z_t| \leq \theta_{close,i}$:
   - Close position and realize profit/loss

3. **Position Sizing**: Each position size is calculated as:
   $$Q_t = \max\left(\left\lfloor\frac{0.02 \times C_t}{P_t}\right\rfloor, 1\right)$$
   
   where $C_t$ is current capital and $P_t$ is current price, ensuring 2% capital allocation per trade with minimum quantity of 1 share.

#### 2.3.3 Risk Management

The system implements several risk management mechanisms:

- **Time-based Exit**: All positions are forcibly closed at 3:40 PM EST to avoid overnight risk
- **Capital Allocation**: Maximum 2% of total capital per individual trade
- **Position Limits**: Only one position per strategy at any given time
- **Liquidation Protocol**: Complete portfolio liquidation at market close (intra-day trading only)

## 3. Performance Analysis

### 3.1 Strategy Effectiveness Under Normal Conditions

Under typical market conditions, the algorithm demonstrates consistent profitability through its mean-reversion approach. The multi-threshold strategy allows for:

- **Diversified Entry Points**: Different sensitivity levels capture various magnitudes of price deviations
- **Systematic Profit Taking**: Predetermined exit thresholds ensure consistent profit realization
- **Risk Distribution**: Multiple concurrent strategies reduce dependence on any single threshold parameter

### 3.2 Vulnerability to Regime Changes

#### 3.2.1 The Outlier Problem

The algorithm's primary weakness manifests when statistical outliers represent the beginning of sustained directional trends rather than temporary deviations. In such scenarios:

1. **False Signal Generation**: Large normalized deviations ($|Z_t| >> \theta_{open}$) trigger position opening
2. **Trend Continuation**: Instead of mean reversion, the price continues in the deviation direction
3. **Amplified Losses**: The larger the initial deviation, the greater the potential loss as the trend continues

#### 3.2.2 Mathematical Formulation of Loss Scenarios

Consider a scenario where the algorithm shorts at price $P_{short}$ when $Z_t = 3.5$ (triggering the highest threshold strategy). If this represents the beginning of an upward trend rather than a temporary deviation, the loss $L$ at price $P_{current}$ becomes:

$$L = Q \times (P_{current} - P_{short})$$

where the loss grows linearly with trend continuation, potentially exceeding the typical small gains from successful mean-reversion trades.

#### 3.2.3 Regime Detection Limitations

The current implementation lacks regime detection capabilities, relying solely on:
- Fixed lookback windows (60 periods)
- Static threshold parameters
- No trend momentum analysis
- No volatility regime adjustment

## 4. Technical Implementation Details

### 4.1 Real-time Data Processing

The system processes price updates every 10 seconds through a continuous loop which calls the trader function with the most recent standardized price

### 4.2 Statistical Calculations

The rolling statistics are maintained efficiently using circular buffer logic:

```cpp
void pop_front(vector<double> &in){
    vector<double> new_vector(in.begin()+1, in.end());
    in = new_vector;
}
```

This ensures constant memory usage while maintaining the 60-period rolling window for statistical calculations.

### 4.3 Order Execution

Position management integrates with the Alpaca trading API through a Python wrapper, ensuring:
- Market order execution for immediate fills
- JSON-based trade tracking for position management
- Automated position closure based on statistical signals

## 5. Discussion

### 5.1 Strengths of the Approach

1. **Statistical Rigor**: The normalization approach provides robust, scale-invariant trading signals
2. **Risk Management**: Multiple built-in safeguards limit downside exposure
3. **Systematic Execution**: Removes emotional bias through algorithmic decision-making
4. **Scalability**: Framework can be extended to multiple assets and timeframes

### 5.2 Areas for Improvement

#### 5.2.1 Regime Detection Enhancement

Future iterations should incorporate:
- **Volatility Regime Analysis**: Adjust thresholds based on current market volatility
- **Trend Momentum Indicators**: Incorporate directional bias detection
- **Correlation Monitoring**: Track inter-asset relationships for market regime identification

#### 5.2.2 Dynamic Parameter Adjustment

The static threshold approach could benefit from:
- **Adaptive Thresholds**: Parameters that adjust based on recent market behavior
- **Machine Learning Integration**: Pattern recognition for regime change detection
- **Multi-timeframe Analysis**: Incorporate longer-term trend analysis

#### 5.2.3 Enhanced Risk Management

Additional risk controls could include:
- **Maximum Drawdown Limits**: Portfolio-level loss limits
- **Correlation-based Position Sizing**: Reduce exposure during high-correlation periods
- **Volatility-adjusted Position Sizing**: Scale positions based on current volatility

## 6. Conclusion

The normalized price deviation trading algorithm presents a systematic approach to statistical arbitrage that demonstrates effectiveness under normal market conditions. The mathematical framework provides a robust foundation for identifying mean-reversion opportunities through standardized price analysis.

However, the strategy's vulnerability to regime changes—particularly when statistical outliers represent trend beginnings rather than temporary deviations—highlights the importance of incorporating regime detection mechanisms in quantitative trading systems. The linear relationship between deviation magnitude and potential loss during trend continuation scenarios creates asymmetric risk profiles that require careful management.

Future research should focus on developing hybrid approaches that combine the statistical rigor of the current methodology with dynamic regime detection capabilities. This would allow the system to distinguish between temporary price dislocations (suitable for mean-reversion strategies) and the beginning of sustained directional movements (requiring trend-following or position avoidance strategies).

The modular architecture and systematic approach provide a solid foundation for such enhancements, making this work a valuable contribution to the field of algorithmic trading research.

## References

1. Avellaneda, M., & Lee, J. H. (2010). Statistical arbitrage in the US equities market. *Quantitative Finance*, 10(7), 761-782.

2. Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G. (2006). Pairs trading: Performance of a relative-value arbitrage rule. *The Review of Financial Studies*, 19(3), 797-827.

3. Pole, A. (2007). *Statistical arbitrage: Algorithmic trading insights and techniques*. John Wiley & Sons.

4. Vidyamurthy, G. (2004). *Pairs Trading: quantitative methods and analysis*. John Wiley & Sons.

5. Chan, E. (2009). *Quantitative trading: how to build your own algorithmic trading business*. John Wiley & Sons.
