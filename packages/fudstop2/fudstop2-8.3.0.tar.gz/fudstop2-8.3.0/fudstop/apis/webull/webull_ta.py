import re
import pandas as pd
import asyncio
import time

import httpx
import numpy as np



class WebullTA:
    def __init__(self):
        self.cycle_indicators = {
        "HT_DCPERIOD": {
            "description": "Hilbert Transform - Dominant Cycle Period. Measures the dominant cycle period in the price series.",
            "ideal_scan": "Look for stable or increasing cycle periods to identify trend continuation or weakening."
        },
        "HT_DCPHASE": {
            "description": "Hilbert Transform - Dominant Cycle Phase. Represents the phase of the dominant cycle.",
            "ideal_scan": "Identify phase changes for potential reversals or trend accelerations."
        },
        "HT_PHASOR": {
            "description": "Hilbert Transform - Phasor Components. Provides complex components (real and imaginary) of the phasor.",
            "ideal_scan": "Use changes in real or imaginary components to detect shifts in price momentum or trend."
        },
        "HT_SINE": {
            "description": "Hilbert Transform - SineWave. Produces sine and lead sine wave values for trend identification.",
            "ideal_scan": "Crossovers between sine and lead sine waves can signal potential trend changes."
        },
        "HT_TRENDMODE": {
            "description": "Hilbert Transform - Trend vs. Cycle Mode. Identifies if the market is in a trending or cyclic mode.",
            "ideal_scan": "HT_TRENDMODE = 1 for trending conditions; HT_TRENDMODE = 0 for cyclic conditions."
        },
    },
        
        self.pattern_recognition_indicators = {
        # Pattern Recognition Indicators
        "CDL2CROWS": {
            "description": "Two Crows - A bearish reversal pattern that occurs after an uptrend.",
            "ideal_scan": "Look for Two Crows at resistance levels or after a strong uptrend."
        },
        "CDL3BLACKCROWS": {
            "description": "Three Black Crows - A bearish reversal pattern with three consecutive long bearish candles.",
            "ideal_scan": "Appears after an uptrend; confirms bearish momentum."
        },
        "CDL3INSIDE": {
            "description": "Three Inside Up/Down - A candlestick pattern indicating potential reversal.",
            "ideal_scan": "Three Inside Up for bullish reversals; Three Inside Down for bearish reversals."
        },
        "CDL3LINESTRIKE": {
            "description": "Three-Line Strike - A potential continuation pattern after a trend.",
            "ideal_scan": "Look for confirmation with volume or other trend indicators."
        },
        "CDL3OUTSIDE": {
            "description": "Three Outside Up/Down - Indicates reversal of the current trend.",
            "ideal_scan": "Three Outside Up after a downtrend; Three Outside Down after an uptrend."
        },
        "CDL3STARSINSOUTH": {
            "description": "Three Stars In The South - A rare bullish reversal pattern.",
            "ideal_scan": "Forms in a downtrend; confirms reversal when paired with increasing volume."
        },
        "CDL3WHITESOLDIERS": {
            "description": "Three Advancing White Soldiers - A strong bullish reversal pattern.",
            "ideal_scan": "Look for this after a downtrend; confirms bullish momentum."
        },
        "CDLABANDONEDBABY": {
            "description": "Abandoned Baby - A reversal pattern with a gap on both sides of a doji.",
            "ideal_scan": "Bullish after a downtrend; bearish after an uptrend."
        },
        "CDLADVANCEBLOCK": {
            "description": "Advance Block - A bearish reversal pattern with three candles showing weakening momentum.",
            "ideal_scan": "Occurs in an uptrend; look for weakening volume."
        },
        "CDLBELTHOLD": {
            "description": "Belt-hold - A single candlestick pattern indicating reversal or continuation.",
            "ideal_scan": "Bullish at support levels; bearish at resistance levels."
        },
        "CDLBREAKAWAY": {
            "description": "Breakaway - A five-candle reversal pattern.",
            "ideal_scan": "Look for bullish Breakaway in a downtrend; bearish in an uptrend."
        },
        "CDLCLOSINGMARUBOZU": {
            "description": "Closing Marubozu - A candlestick with no shadow on the closing side.",
            "ideal_scan": "Bullish when the close is the high; bearish when the close is the low."
        },
        "CDLCONCEALBABYSWALL": {
            "description": "Concealing Baby Swallow - A bullish reversal pattern formed by four candles.",
            "ideal_scan": "Forms in a downtrend; confirms reversal with increasing volume."
        },
        "CDLCOUNTERATTACK": {
            "description": "Counterattack - A reversal pattern with a strong opposing candle.",
            "ideal_scan": "Bullish at support; bearish at resistance."
        },
        "CDLDARKCLOUDCOVER": {
            "description": "Dark Cloud Cover - A bearish reversal pattern with a strong bearish candle.",
            "ideal_scan": "Occurs at the top of an uptrend; confirms with increased volume."
        },
        "CDLDOJI": {
            "description": "Doji - Indicates indecision in the market.",
            "ideal_scan": "Look for Doji near support or resistance levels to signal potential reversals."
        },
        "CDLDOJISTAR": {
            "description": "Doji Star - A potential reversal pattern with a doji after a trend candle.",
            "ideal_scan": "Bullish after a downtrend; bearish after an uptrend."
        },
        "CDLDRAGONFLYDOJI": {
            "description": "Dragonfly Doji - A bullish reversal pattern with a long lower shadow.",
            "ideal_scan": "Occurs in a downtrend; confirms reversal with higher volume."
        },
        "CDLENGULFING": {
            "description": "Engulfing Pattern - A strong reversal pattern with a larger candle engulfing the previous one.",
            "ideal_scan": "Bullish after a downtrend; bearish after an uptrend."
        },
        "CDLEVENINGDOJISTAR": {
            "description": "Evening Doji Star - A bearish reversal pattern with a doji star.",
            "ideal_scan": "Occurs at the top of an uptrend; confirms with increased volume."
        },
        "CDLEVENINGSTAR": {
            "description": "Evening Star - A bearish reversal pattern.",
            "ideal_scan": "Forms at resistance; confirms bearish reversal."
        },
        "CDLGAPSIDESIDEWHITE": {
            "description": "Up/Down-gap side-by-side white lines - A continuation pattern.",
            "ideal_scan": "Look for confirmation with other trend indicators."
        },
        "CDLGRAVESTONEDOJI": {
            "description": "Gravestone Doji - A bearish reversal pattern with a long upper shadow.",
            "ideal_scan": "Occurs in an uptrend; confirms reversal with high volume."
        },
        "CDLHAMMER": {
            "description": "Hammer - A bullish reversal pattern with a long lower shadow.",
            "ideal_scan": "Appears in a downtrend; confirms reversal with strong volume."
        },
        "CDLHANGINGMAN": {
            "description": "Hanging Man - A bearish reversal pattern with a long lower shadow.",
            "ideal_scan": "Occurs in an uptrend; look for confirmation with volume."
        },
        "CDLHARAMI": {
            "description": "Harami Pattern - A two-candle reversal pattern.",
            "ideal_scan": "Bullish Harami in a downtrend; bearish Harami in an uptrend."
        },
        "CDLHARAMICROSS": {
            "description": "Harami Cross Pattern - A Harami pattern with a doji as the second candle.",
            "ideal_scan": "Stronger reversal signal compared to the standard Harami."
        },
        "CDLHIGHWAVE": {
            "description": "High-Wave Candle - Indicates market indecision.",
            "ideal_scan": "Look for High-Wave candles near key support or resistance levels."
        },
        "CDLHIKKAKE": {
            "description": "Hikkake Pattern - A trap pattern indicating reversal or continuation.",
            "ideal_scan": "Look for false breakout followed by a strong move in the opposite direction."
        },
        "CDLHIKKAKEMOD": {
            "description": "Modified Hikkake Pattern - A variation of the Hikkake pattern.",
            "ideal_scan": "Scan for similar setups as standard Hikkake but with adjusted conditions."
        },
        "CDLHOMINGPIGEON": {
            "description": "Homing Pigeon - A bullish reversal pattern with two candles.",
            "ideal_scan": "Forms in a downtrend; confirms reversal with higher volume."
        },
        "CDLIDENTICAL3CROWS": {
            "description": "Identical Three Crows - A bearish reversal pattern with three identical bearish candles.",
            "ideal_scan": "Appears at the top of an uptrend; confirms bearish continuation."
        },
        "CDLINNECK": {
            "description": "In-Neck Pattern - A bearish continuation pattern.",
            "ideal_scan": "Occurs in a downtrend; confirms bearish momentum."
        },
        "CDLINVERTEDHAMMER": {
            "description": "Inverted Hammer - A bullish reversal pattern with a long upper shadow.",
            "ideal_scan": "Occurs in a downtrend; confirms with higher volume."
        },
        "CDLPIERCING": {
            "description": "Piercing Pattern - A bullish reversal pattern with a strong upward move.",
            "ideal_scan": "Occurs in a downtrend; confirms with increasing volume."
        },
    "CDLKICKING": {
        "description": "Kicking - A strong reversal pattern characterized by a gap between two opposite-colored marubozu candles.",
        "ideal_scan": "Bullish kicking in a downtrend; bearish kicking in an uptrend."
    },
    "CDLKICKINGBYLENGTH": {
        "description": "Kicking by Length - Similar to Kicking but determined by the length of the marubozu.",
        "ideal_scan": "Scan for longer marubozu candles to confirm stronger signals."
    },
    "CDLLADDERBOTTOM": {
        "description": "Ladder Bottom - A bullish reversal pattern that occurs after a downtrend.",
        "ideal_scan": "Look for increasing volume on confirmation."
    },
    "CDLLONGLEGGEDDOJI": {
        "description": "Long-Legged Doji - Indicates market indecision with long upper and lower shadows.",
        "ideal_scan": "Appears near support or resistance; confirms potential reversal."
    },
    "CDLLONGLINE": {
        "description": "Long Line Candle - A single candlestick with a long body, indicating strong momentum.",
        "ideal_scan": "Bullish long lines near support; bearish near resistance."
    },
    "CDLMARUBOZU": {
        "description": "Marubozu - A candlestick with no shadows, indicating strong directional momentum.",
        "ideal_scan": "Bullish marubozu in uptrend; bearish marubozu in downtrend."
    },
    "CDLMATCHINGLOW": {
        "description": "Matching Low - A bullish reversal pattern with two candles having the same low.",
        "ideal_scan": "Occurs in a downtrend; confirms reversal with increased volume."
    },
    "CDLMATHOLD": {
        "description": "Mat Hold - A continuation pattern that indicates strong trend persistence.",
        "ideal_scan": "Bullish Mat Hold in an uptrend; bearish Mat Hold in a downtrend."
    },
    "CDLMORNINGDOJISTAR": {
        "description": "Morning Doji Star - A bullish reversal pattern with a doji and gap.",
        "ideal_scan": "Appears in a downtrend; confirms reversal with strong upward move."
    },
    "CDLMORNINGSTAR": {
        "description": "Morning Star - A bullish reversal pattern with three candles.",
        "ideal_scan": "Occurs in a downtrend; confirms with increasing volume."
    },
    "CDLONNECK": {
        "description": "On-Neck Pattern - A bearish continuation pattern.",
        "ideal_scan": "Occurs in a downtrend; confirms bearish momentum."
    },
    "CDLPIERCING": {
        "description": "Piercing Pattern - A bullish reversal pattern with a strong upward move.",
        "ideal_scan": "Appears in a downtrend; confirms with increasing volume."
    },
    "CDLRICKSHAWMAN": {
        "description": "Rickshaw Man - A variation of the Doji with long upper and lower shadows.",
        "ideal_scan": "Indicates indecision; look for context near support or resistance."
    },
    "CDLRISEFALL3METHODS": {
        "description": "Rising/Falling Three Methods - A continuation pattern with small corrective candles.",
        "ideal_scan": "Bullish in uptrend; bearish in downtrend with trend resumption confirmation."
    },
    "CDLSEPARATINGLINES": {
        "description": "Separating Lines - A continuation pattern with two strong candles.",
        "ideal_scan": "Bullish in an uptrend; bearish in a downtrend."
    },
    "CDLSHOOTINGSTAR": {
        "description": "Shooting Star - A bearish reversal pattern with a long upper shadow.",
        "ideal_scan": "Occurs in an uptrend; confirms reversal with strong bearish move."
    },
    "CDLSHORTLINE": {
        "description": "Short Line Candle - A candlestick with a short body, indicating low momentum.",
        "ideal_scan": "Look for context within larger patterns for confirmation."
    },
    "CDLSPINNINGTOP": {
        "description": "Spinning Top - A candlestick with small real body and long shadows.",
        "ideal_scan": "Indicates indecision; watch for breakouts in the direction of the trend."
    },
    "CDLSTALLEDPATTERN": {
        "description": "Stalled Pattern - A bearish reversal pattern in an uptrend.",
        "ideal_scan": "Appears near resistance; confirms reversal with volume."
    },
    "CDLSTICKSANDWICH": {
        "description": "Stick Sandwich - A bullish reversal pattern with two bearish candles sandwiching a bullish one.",
        "ideal_scan": "Occurs in a downtrend; confirms reversal when price breaks higher."
    },
    "CDLTAKURI": {
        "description": "Takuri - A Dragonfly Doji with an exceptionally long lower shadow.",
        "ideal_scan": "Occurs in a downtrend; confirms reversal with strong upward move."
    },
    "CDLTASUKIGAP": {
        "description": "Tasuki Gap - A continuation pattern with a gap and corrective candle.",
        "ideal_scan": "Bullish in uptrend; bearish in downtrend with gap hold confirmation."
    },
    "CDLTHRUSTING": {
        "description": "Thrusting Pattern - A bearish continuation pattern with partial gap filling.",
        "ideal_scan": "Occurs in a downtrend; confirms bearish continuation."
    },
    "CDLTRISTAR": {
        "description": "Tristar Pattern - A reversal pattern with three doji candles.",
        "ideal_scan": "Bullish Tristar in a downtrend; bearish Tristar in an uptrend."
    },
    "CDLUNIQUE3RIVER": {
        "description": "Unique 3 River - A rare bullish reversal pattern.",
        "ideal_scan": "Forms in a downtrend; confirms with a strong upward move."
    },
    "CDLUPSIDEGAP2CROWS": {
        "description": "Upside Gap Two Crows - A bearish reversal pattern with a gap and two bearish candles.",
        "ideal_scan": "Occurs in an uptrend; confirms bearish reversal."
    },
    "CDLXSIDEGAP3METHODS": {
        "description": "Upside/Downside Gap Three Methods - A continuation pattern with a gap and corrective candles.",
        "ideal_scan": "Bullish in uptrend; bearish in downtrend with confirmation of resumption."
    }}

        self.math_transform_indicators = {
        "ACOS": {
            "description": "Vector Trigonometric ACos - Calculates the arccosine of a vector's values.",
            "ideal_use": "Used in computations requiring the inverse cosine of an angle or value."
        },
        "ASIN": {
            "description": "Vector Trigonometric ASin - Calculates the arcsine of a vector's values.",
            "ideal_use": "Used in computations requiring the inverse sine of an angle or value."
        },
        "ATAN": {
            "description": "Vector Trigonometric ATan - Calculates the arctangent of a vector's values.",
            "ideal_use": "Used to determine the angle whose tangent is a given value."
        },
        "CEIL": {
            "description": "Vector Ceil - Rounds up each value in the vector to the nearest integer.",
            "ideal_use": "Useful for ensuring results are rounded up to whole numbers in trading algorithms."
        },
        "COS": {
            "description": "Vector Trigonometric Cos - Calculates the cosine of a vector's values.",
            "ideal_use": "Commonly used in harmonic analysis or periodic trend modeling."
        },
        "COSH": {
            "description": "Vector Trigonometric Cosh - Calculates the hyperbolic cosine of a vector's values.",
            "ideal_use": "Used in advanced mathematical computations and some exotic indicators."
        },
        "EXP": {
            "description": "Vector Arithmetic Exp - Calculates the exponential (e^x) of a vector's values.",
            "ideal_use": "Commonly used in indicators requiring exponential growth or decay, such as volatility models."
        },
        "FLOOR": {
            "description": "Vector Floor - Rounds down each value in the vector to the nearest integer.",
            "ideal_use": "Used to ensure results are rounded down to whole numbers."
        },
        "LN": {
            "description": "Vector Log Natural - Calculates the natural logarithm (log base e) of a vector's values.",
            "ideal_use": "Used in growth rate computations or natural scaling of data."
        },
        "LOG10": {
            "description": "Vector Log10 - Calculates the base-10 logarithm of a vector's values.",
            "ideal_use": "Helpful in scaling data, especially when dealing with large ranges of values."
        },
        "SIN": {
            "description": "Vector Trigonometric Sin - Calculates the sine of a vector's values.",
            "ideal_use": "Used in harmonic analysis or modeling periodic trends."
        },
        "SINH": {
            "description": "Vector Trigonometric Sinh - Calculates the hyperbolic sine of a vector's values.",
            "ideal_use": "Used in advanced mathematical and financial computations."
        },
        "SQRT": {
            "description": "Vector Square Root - Calculates the square root of a vector's values.",
            "ideal_use": "Common in risk modeling, variance analysis, and volatility computations."
        },
        "TAN": {
            "description": "Vector Trigonometric Tan - Calculates the tangent of a vector's values.",
            "ideal_use": "Used in periodic analysis or advanced technical models."
        },
        "TANH": {
            "description": "Vector Trigonometric Tanh - Calculates the hyperbolic tangent of a vector's values.",
            "ideal_use": "Used in specialized computations requiring hyperbolic functions."
        }
    }

        self.statistical_indicators = {
        "BETA": {
            "description": "Beta - Measures the relationship (sensitivity) between a security's returns and a benchmark index.",
            "ideal_use": "Identify the relative volatility of a security to the market (e.g., BETA > 1 for higher volatility)."
        },
        "CORREL": {
            "description": "Pearson's Correlation Coefficient (r) - Measures the strength and direction of the linear relationship between two data sets.",
            "ideal_use": "Use CORREL > 0.8 or CORREL < -0.8 to identify strong positive or negative correlations."
        },
        "LINEARREG": {
            "description": "Linear Regression - Best-fit line over a specified period for trend analysis.",
            "ideal_use": "Use the slope of LINEARREG to determine trend direction; upward slope for bullish and downward for bearish."
        },
        "LINEARREG_ANGLE": {
            "description": "Linear Regression Angle - The angle of the linear regression line, indicating the strength of the trend.",
            "ideal_use": "Look for high positive angles (> 45°) for strong uptrends and high negative angles (< -45°) for strong downtrends."
        },
        "LINEARREG_INTERCEPT": {
            "description": "Linear Regression Intercept - The Y-intercept of the linear regression line.",
            "ideal_use": "Use in conjunction with slope to project expected price levels."
        },
        "LINEARREG_SLOPE": {
            "description": "Linear Regression Slope - The slope of the linear regression line.",
            "ideal_use": "Positive slope indicates bullish trend strength; negative slope indicates bearish trend strength."
        },
        "STDDEV": {
            "description": "Standard Deviation - Measures the dispersion of data points from the mean.",
            "ideal_use": "High STDDEV indicates high volatility; low STDDEV suggests consolidation."
        },
        "TSF": {
            "description": "Time Series Forecast - Predicts future values based on past linear regression.",
            "ideal_use": "Use TSF to project expected price levels; compare forecast to actual price for potential trades."
        },
        "VAR": {
            "description": "Variance - Measures the variability or spread of data points.",
            "ideal_use": "High VAR indicates high market variability; low VAR indicates stability and potential consolidation."
        }
    }

        self.math_operators = {
        "ADD": {
            "description": "Addition - Adds two data series or constants.",
            "ideal_scan": "Useful for combining indicators or offsetting values."
        },
        "DIV": {
            "description": "Division - Divides one data series or constant by another.",
            "ideal_scan": "Use for creating ratio-based indicators (e.g., price/volume)."
        },
        "MAX": {
            "description": "Maximum - Finds the maximum value over a specified period.",
            "ideal_scan": "Look for peaks in price or indicators to identify resistance levels or extremes."
        },
        "MAXINDEX": {
            "description": "Maximum Index - Returns the index of the maximum value in a period.",
            "ideal_scan": "Use to pinpoint when the highest value occurred."
        },
        "MIN": {
            "description": "Minimum - Finds the minimum value over a specified period.",
            "ideal_scan": "Look for troughs to identify support levels or extremes."
        },
        "MININDEX": {
            "description": "Minimum Index - Returns the index of the minimum value in a period.",
            "ideal_scan": "Use to pinpoint when the lowest value occurred."
        },
        "MINMAX": {
            "description": "Minimum and Maximum - Calculates both the minimum and maximum values over a period.",
            "ideal_scan": "Useful for identifying ranges or volatility."
        },
        "MINMAXINDEX": {
            "description": "Minimum and Maximum Index - Returns the indices of the minimum and maximum values in a period.",
            "ideal_scan": "Identify periods of extreme price movements for potential reversals."
        },
        "MULT": {
            "description": "Multiplication - Multiplies two data series or constants.",
            "ideal_scan": "Useful for scaling or amplifying indicator values."
        },
        "SUB": {
            "description": "Subtraction - Subtracts one data series or constant from another.",
            "ideal_scan": "Commonly used for calculating spreads or deviations."
        },
        "SUM": {
            "description": "Sum - Calculates the sum of values over a specified period.",
            "ideal_scan": "Detect cumulative volume or price movements for momentum analysis."
        }
    }
        self.volume_indicators = {
            # Volume Indicators
            "AD": {
                "description": "Chaikin A/D Line - Measures the cumulative flow of money into and out of a security.",
                "ideal_scan": "AD trending upward with price indicates strong accumulation; downward indicates distribution."
            },
            "ADOSC": {
                "description": "Chaikin A/D Oscillator - Tracks momentum changes in the A/D Line.",
                "ideal_scan": "ADOSC crossing above zero indicates bullish momentum; below zero indicates bearish momentum."
            },
            "OBV": {
                "description": "On Balance Volume - Tracks cumulative volume flow to confirm price trends.",
                "ideal_scan": "OBV making higher highs supports bullish trends; lower lows confirm bearish trends."
            },
            
            # Cycle Indicators
            "HT_DCPERIOD": {
                "description": "Hilbert Transform - Dominant Cycle Period. Identifies the dominant price cycle.",
                "ideal_scan": "Stable or increasing HT_DCPERIOD suggests consistent trends; sharp drops may indicate trend changes."
            },
            "HT_DCPHASE": {
                "description": "Hilbert Transform - Dominant Cycle Phase. Represents the phase of the dominant price cycle.",
                "ideal_scan": "Look for significant phase shifts to anticipate potential reversals."
            },
            "HT_PHASOR": {
                "description": "Hilbert Transform - Phasor Components. Outputs real and imaginary components of the phasor.",
                "ideal_scan": "Use changes in real or imaginary values to detect trend direction shifts."
            },
            "HT_SINE": {
                "description": "Hilbert Transform - SineWave. Produces sine and lead sine wave values for market cycles.",
                "ideal_scan": "Crossovers between sine and lead sine waves can indicate potential trend reversals."
            },
            "HT_TRENDMODE": {
                "description": "Hilbert Transform - Trend vs Cycle Mode. Identifies whether the market is trending or cyclic.",
                "ideal_scan": "HT_TRENDMODE = 1 for trending conditions; HT_TRENDMODE = 0 for cyclic conditions."
            },}
        self.price_transform_indicators ={
    "AVGPRICE": {
        "description": "Average Price - The average of open, high, low, and close prices.",
        "ideal_scan": "Use as a reference point; price above AVGPRICE indicates bullish momentum and below indicates bearish momentum."
    },
    "MEDPRICE": {
        "description": "Median Price - The average of the high and low prices.",
        "ideal_scan": "Use MEDPRICE to identify equilibrium levels; significant deviations may signal breakouts."
    },
    "TYPPRICE": {
        "description": "Typical Price - The average of high, low, and close prices.",
        "ideal_scan": "Use TYPPRICE to identify key levels for trend analysis."
    },
    "WCLPRICE": {
        "description": "Weighted Close Price - Heavily weights the closing price for a more accurate central price.",
        "ideal_scan": "Monitor deviations from WCLPRICE to detect overbought or oversold conditions."
    },}
        self.volatility_indicators ={
    "ATR": {
        "description": "Average True Range - Measures market volatility.",
        "ideal_scan": "ATR increasing signals rising volatility, good for breakout strategies; decreasing ATR indicates consolidation."
    },
    "NATR": {
        "description": "Normalized Average True Range - ATR expressed as a percentage of price.",
        "ideal_scan": "NATR > 5% indicates high volatility; < 2% suggests low volatility or consolidation."
    },
    "TRANGE": {
        "description": "True Range - Measures the absolute price range over a period.",
        "ideal_scan": "Look for high True Range values to signal volatile trading conditions."
    }}

        self.overlap_studies_indicators = {
        # Moving Average Indicators and Trend Analysis Tools
        "BBANDS": {
            "description": "Bollinger Bands - Measures volatility and identifies potential overbought/oversold conditions.",
            "ideal_scan": "Price breaking above upper band for potential bullish continuation; below lower band for bearish continuation."
        },
        "DEMA": {
            "description": "Double Exponential Moving Average - A faster, smoother moving average.",
            "ideal_scan": "DEMA crossover above price for bullish signals; below price for bearish signals."
        },
        "EMA": {
            "description": "Exponential Moving Average - Gives more weight to recent prices for trend tracking.",
            "ideal_scan": "EMA(20) crossing above EMA(50) for bullish signal; EMA(20) crossing below EMA(50) for bearish signal."
        },
        "HT_TRENDLINE": {
            "description": "Hilbert Transform - Instantaneous Trendline. A smoothed trendline for identifying price trends.",
            "ideal_scan": "Price crossing above HT_TRENDLINE for bullish breakout; below for bearish breakdown."
        },
        "KAMA": {
            "description": "Kaufman Adaptive Moving Average - Adjusts its speed based on market volatility.",
            "ideal_scan": "Price crossing above KAMA for potential bullish trend; below KAMA for bearish trend."
        },
        "MA": {
            "description": "Moving Average - A standard average for smoothing price action.",
            "ideal_scan": "MA(50) above MA(200) for bullish trends; MA(50) below MA(200) for bearish trends."
        },
        "MAMA": {
            "description": "MESA Adaptive Moving Average - Adapts to market cycles for smoother trend detection.",
            "ideal_scan": "Price crossing above MAMA for bullish signal; below for bearish signal."
        },
        "MAVP": {
            "description": "Moving Average with Variable Period - A moving average where the period changes dynamically.",
            "ideal_scan": "Crossover logic similar to MA but adjusted for dynamic periods."
        },
        "MIDPOINT": {
            "description": "MidPoint over period - Calculates the midpoint of prices over a specified period.",
            "ideal_scan": "Look for breakouts above midpoint as confirmation of bullish momentum; below for bearish."
        },
        "MIDPRICE": {
            "description": "Midpoint Price over period - The average of the high and low prices over a period.",
            "ideal_scan": "Breakouts above MIDPRICE for bullish trend; below for bearish trend."
        },
        "SAR": {
            "description": "Parabolic SAR - A stop-and-reverse system to identify potential trend reversals.",
            "ideal_scan": "Price crossing above SAR for bullish trend; below SAR for bearish trend."
        },
        "SAREXT": {
            "description": "Parabolic SAR - Extended. A more customizable version of the Parabolic SAR.",
            "ideal_scan": "Similar logic as SAR but allows for custom acceleration settings."
        },
        "SMA": {
            "description": "Simple Moving Average - A basic average over a specified period.",
            "ideal_scan": "SMA(50) crossing above SMA(200) for bullish signal; crossing below for bearish signal."
        },
        "T3": {
            "description": "Triple Exponential Moving Average - A smoother version of EMA with less lag.",
            "ideal_scan": "T3 crossover above price for bullish trend; below price for bearish trend."
        },
        "TEMA": {
            "description": "Triple Exponential Moving Average - Reduces lag and reacts faster to price changes.",
            "ideal_scan": "Price crossing above TEMA for bullish signals; below TEMA for bearish signals."
        },
        "TRIMA": {
            "description": "Triangular Moving Average - Gives more weight to the middle of the data series.",
            "ideal_scan": "TRIMA crossover above price for bullish momentum; below price for bearish momentum."
        },
        "WMA": {
            "description": "Weighted Moving Average - Assigns more weight to recent data points.",
            "ideal_scan": "WMA(10) crossing above WMA(50) for bullish trend; crossing below for bearish trend."
        }
    }

        self.momentum_indicators = {
    "ADX": {
        "description": "Average Directional Movement Index - Measures the strength of a trend.",
        "ideal_scan": "ADX > 25 indicates a strong trend; ADX < 20 indicates a weak trend."
    },
    "ADXR": {
        "description": "Average Directional Movement Index Rating - Smoothed version of ADX.",
        "ideal_scan": "ADXR > 25 indicates a strong trend; ADXR < 20 indicates weak or no trend."
    },
    "APO": {
        "description": "Absolute Price Oscillator - Shows the difference between two moving averages.",
        "ideal_scan": "APO > 0 for bullish momentum; APO < 0 for bearish momentum."
    },
    "AROON": {
        "description": "Aroon - Measures the strength and direction of a trend.",
        "ideal_scan": "Aroon-Up > 70 and Aroon-Down < 30 for bullish signals; Aroon-Up < 30 and Aroon-Down > 70 for bearish signals."
    },
    "AROONOSC": {
        "description": "Aroon Oscillator - The difference between Aroon-Up and Aroon-Down.",
        "ideal_scan": "AroonOsc > 50 for strong bullish momentum; AroonOsc < -50 for strong bearish momentum."
    },
    "BOP": {
        "description": "Balance Of Power - Measures the strength of buying vs selling pressure.",
        "ideal_scan": "BOP > 0.5 for bullish outliers; BOP < -0.5 for bearish outliers."
    },
    "CCI": {
        "description": "Commodity Channel Index - Identifies overbought and oversold levels.",
        "ideal_scan": "CCI > 100 for overbought conditions; CCI < -100 for oversold conditions."
    },
    "CMO": {
        "description": "Chande Momentum Oscillator - Measures momentum of a security.",
        "ideal_scan": "CMO > 50 for strong upward momentum; CMO < -50 for strong downward momentum."
    },
    "DX": {
        "description": "Directional Movement Index - Indicates trend direction and strength.",
        "ideal_scan": "DX > 25 indicates a strong trend; DX < 20 suggests trend weakness."
    },
    "MACD": {
        "description": "Moving Average Convergence/Divergence - Shows the relationship between two moving averages.",
        "ideal_scan": "MACD crossing above Signal Line for bullish; MACD crossing below Signal Line for bearish."
    },
    "MACDEXT": {
        "description": "MACD with controllable MA type - Customizable MACD version.",
        "ideal_scan": "Same logic as MACD but tune MA types for sensitivity."
    },
    "MACDFIX": {
        "description": "Moving Average Convergence/Divergence Fix 12/26 - Fixed parameter MACD.",
        "ideal_scan": "Use 12/26 crossover logic for bullish or bearish momentum."
    },
    "MFI": {
        "description": "Money Flow Index - Measures buying and selling pressure using volume.",
        "ideal_scan": "MFI > 80 for overbought conditions; MFI < 20 for oversold conditions."
    },
    "MINUS_DI": {
        "description": "Minus Directional Indicator - Part of ADX, shows bearish pressure.",
        "ideal_scan": "MINUS_DI > PLUS_DI for bearish trend confirmation."
    },
    "MINUS_DM": {
        "description": "Minus Directional Movement - Measures downward movement strength.",
        "ideal_scan": "High values indicate strong downward moves."
    },
    "MOM": {
        "description": "Momentum - Measures price momentum.",
        "ideal_scan": "MOM > 0 for bullish momentum; MOM < 0 for bearish momentum."
    },
    "PLUS_DI": {
        "description": "Plus Directional Indicator - Part of ADX, shows bullish pressure.",
        "ideal_scan": "PLUS_DI > MINUS_DI for bullish trend confirmation."
    },
    "PLUS_DM": {
        "description": "Plus Directional Movement - Measures upward movement strength.",
        "ideal_scan": "High values indicate strong upward moves."
    },
    "PPO": {
        "description": "Percentage Price Oscillator - MACD in percentage terms.",
        "ideal_scan": "PPO > 0 for bullish momentum; PPO < 0 for bearish momentum."
    },
    "ROC": {
        "description": "Rate of change: ((price/prevPrice)-1)*100 - Measures price change percentage.",
        "ideal_scan": "ROC > 10% for strong bullish moves; ROC < -10% for strong bearish moves."
    },
    "ROCP": {
        "description": "Rate of change Percentage: (price-prevPrice)/prevPrice.",
        "ideal_scan": "Similar to ROC; use significant thresholds based on asset."
    },
    "ROCR": {
        "description": "Rate of change ratio: (price/prevPrice).",
        "ideal_scan": "Use >1 for bullish; <1 for bearish."
    },
    "ROCR100": {
        "description": "Rate of change ratio 100 scale: (price/prevPrice)*100.",
        "ideal_scan": "Use >100 for bullish; <100 for bearish."
    },
    "RSI": {
        "description": "Relative Strength Index - Identifies overbought or oversold conditions.",
        "ideal_scan": "RSI > 70 for overbought; RSI < 30 for oversold."
    },
    "STOCH": {
        "description": "Stochastic - Measures momentum and potential reversals.",
        "ideal_scan": "Stochastic > 80 for overbought; <20 for oversold."
    },
    "STOCHF": {
        "description": "Stochastic Fast - More sensitive version of Stochastic.",
        "ideal_scan": "Same thresholds as Stochastic, but expect quicker signals."
    },
    "STOCHRSI": {
        "description": "Stochastic Relative Strength Index - Combines Stochastic and RSI.",
        "ideal_scan": "Use RSI thresholds (70/30) applied to Stochastic."
    },
    "TRIX": {
        "description": "1-day Rate-Of-Change (ROC) of a Triple Smooth EMA.",
        "ideal_scan": "TRIX > 0 for bullish momentum; TRIX < 0 for bearish momentum."
    },
    "ULTOSC": {
        "description": "Ultimate Oscillator - Combines short, medium, and long-term momentum.",
        "ideal_scan": "ULTOSC > 70 for overbought; ULTOSC < 30 for oversold."
    },
    "WILLR": {
        "description": "Williams' %R - Measures overbought/oversold levels.",
        "ideal_scan": "WILLR > -20 for overbought; WILLR < -80 for oversold."
    }
}

        self.ticker_df = pd.read_csv('files/ticker_csv.csv')
        self.ticker_to_id_map = dict(zip(self.ticker_df['ticker'], self.ticker_df['id']))
        self.intervals_to_scan = ['m5', 'm30', 'm60', 'm120', 'm240', 'd', 'w', 'm']  # Add or remove intervals as needed
    def parse_interval(self,interval_str):
        pattern = r'([a-zA-Z]+)(\d+)'
        match = re.match(pattern, interval_str)
        if match:
            unit = match.group(1)
            value = int(match.group(2))
            if unit == 'm':
                return value * 60
            elif unit == 'h':
                return value * 3600
            elif unit == 'd':
                return value * 86400
            else:
                raise ValueError(f"Unknown interval unit: {unit}")
        else:
            raise ValueError(f"Invalid interval format: {interval_str}")
    async def get_webull_id(self, symbol):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        ticker_id = self.ticker_to_id_map.get(symbol)
        return ticker_id
    async def get_webull_ids(self, symbols):
        """Fetch ticker IDs for a list of symbols in one go."""
        return {symbol: self.ticker_to_id_map.get(symbol) for symbol in symbols}
    async def get_candle_data(self, ticker, interval, headers, count:str='200'):
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPX'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            



            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())
            tickerid = await self.get_webull_id(ticker)
            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query-mini?tickerId={tickerid}&type={interval}&count={count}&timestamp={timeStamp}&restorationType=1&extendTrading=0'

            interval_mapping = {
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            timespan = interval_mapping.get(interval)

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(base_fintech_gw_url)
                r = data.json()
                if r and isinstance(r, list) and 'data' in r[0]:
                    data = r[0]['data']

     
                    split_data = [row.split(",") for row in data]
             
                    df = pd.DataFrame(split_data, columns=['Timestamp', 'Open', 'Close', 'High', 'Low', 'Vwap', 'Volume', 'Avg'])
                    df['Timestamp'] = pd.to_numeric(df['Timestamp'], errors='coerce')
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)

                    # First localize to UTC, then convert to 'US/Eastern' and remove timezone info
                    df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
                    df['Ticker'] = ticker
                    df['timespan'] = interval
                    # Format the Timestamp column into ISO 8601 strings for API compatibility
                    df['Timestamp'] = df['Timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S')  # ISO 8601 format
                    df['Close'] = df['Close'].astype(float)
                    df['Open'] = df['Open'].astype(float)
                    df['High'] = df['High'].astype(float)
                    df['Low'] = df['Low'].astype(float)
                    df['Volume'] = df['Volume'].astype(float)
                    df['Vwap'] = df['Vwap'].astype(float)
                    return df[::-1]
                
        except Exception as e:
            print(e)


    # Simulating async TA data fetching for each timeframe
    async def fetch_ta_data(self, timeframe, data):
        # Simulate an async operation to fetch data (e.g., from an API)

        return data.get(timeframe, {})
    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.

        Parameters:
        - df (pd.DataFrame): DataFrame containing market data with columns ['High', 'Low', 'Open', 'Close', 'Volume', 'Vwap', 'Timestamp']
        - interval (str): Resampling interval based on custom mappings (e.g., 'm5', 'm30', 'd', 'w', 'm')

        Returns:
        - pd.DataFrame: DataFrame with additional columns indicating detected candlestick patterns and their bullish/bearish nature
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
            # Add more mappings as needed
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # Since we want the most recent data first, reverse the DataFrame
        patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df

    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv

    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # No need to reverse the DataFrame; keep it in ascending order
        # patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df.reset_index()
   
    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv
    def detect_patterns(self, ohlcv):
        # Initialize pattern columns
        patterns = ['hammer', 'inverted_hammer', 'hanging_man', 'shooting_star', 'doji',
                    'bullish_engulfing', 'bearish_engulfing', 'bullish_harami', 'bearish_harami',
                    'morning_star', 'evening_star', 'piercing_line', 'dark_cloud_cover',
                    'three_white_soldiers', 'three_black_crows', 'abandoned_baby',
                    'rising_three_methods', 'falling_three_methods', 'three_inside_up', 'three_inside_down',
                     'gravestone_doji', 'butterfly_doji', 'harami_cross', 'tweezer_top', 'tweezer_bottom']



        for pattern in patterns:
            ohlcv[pattern] = False

        ohlcv['signal'] = None  # To indicate Bullish or Bearish signal

        # Iterate over the DataFrame to detect patterns
        for i in range(len(ohlcv)):
            curr_row = ohlcv.iloc[i]
            prev_row = ohlcv.iloc[i - 1] if i >= 1 else None
            prev_prev_row = ohlcv.iloc[i - 2] if i >= 2 else None



            uptrend = self.is_uptrend(ohlcv, i)
            downtrend = self.is_downtrend(ohlcv, i)


            # Single-candle patterns
            if downtrend and self.is_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if downtrend and self.is_inverted_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'inverted_hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_hanging_man(curr_row):
                ohlcv.at[ohlcv.index[i], 'hanging_man'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if uptrend and self.is_shooting_star(curr_row):
                ohlcv.at[ohlcv.index[i], 'shooting_star'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if downtrend and self.is_dragonfly_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'dragonfly_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_gravestone_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'gravestone_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

            # Two-candle patterns
            if prev_row is not None:
                if downtrend and self.is_bullish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_bullish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_piercing_line(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'piercing_line'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_dark_cloud_cover(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'dark_cloud_cover'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_tweezer_bottom(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_bottom'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_tweezer_top(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_top'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_harami_cross(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'harami_cross'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'neutral'

            # Three-candle patterns
            if prev_row is not None and prev_prev_row is not None:
                if downtrend and self.is_morning_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'morning_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_evening_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'evening_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_white_soldiers(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_white_soldiers'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_black_crows(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_black_crows'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_inside_up(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_up'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_inside_down(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_down'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if self.is_abandoned_baby(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'abandoned_baby'] = True
                    if curr_row['Close'] > prev_row['Close']:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                    else:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_rising_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'rising_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_falling_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'falling_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

        return ohlcv
    def is_gravestone_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and lower_shadow == 0 and upper_shadow > 2 * body_length
        
    def is_three_inside_up(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bearish and second_bullish and third_bullish and
                prev_row['Open'] > prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Open'] and
                curr_row['Close'] > prev_prev_row['Open'])


    def is_tweezer_top(self, prev_row, curr_row):
        return (prev_row['High'] == curr_row['High']) and (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open'])

    def is_tweezer_bottom(self, prev_row, curr_row):
        return (prev_row['Low'] == curr_row['Low']) and (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open'])

    def is_dragonfly_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and upper_shadow == 0 and lower_shadow > 2 * body_length


    def is_uptrend(self, df: pd.DataFrame, length: int =7) -> bool:
        """
        Check if the dataframe shows an uptrend over the specified length.
        
        An uptrend is defined as consecutive increasing 'Close' values for the given length.
        The dataframe is assumed to have the most recent candle at index 0.
        """
        try:
            if len(df) < length:
                raise ValueError(f"DataFrame length ({len(df)}) is less than the specified length ({length})")
            
            # Since the most recent data is at index 0, we need to reverse the direction of comparison.
            return (df['Close'].iloc[:length].diff(periods=-1).iloc[:-1] > 0).all()

        except Exception as e:
            print(f"Failed - {e}")

    def is_downtrend(self, df: pd.DataFrame, length: int = 7) -> bool:
        """
        Check if the dataframe shows a downtrend over the specified length.
        
        A downtrend is defined as consecutive decreasing 'Close' values for the given length.
        """
        try:
            if len(df) < length:
                raise ValueError(f"DataFrame length ({len(df)}) is less than the specified length ({length})")
            
            # Since the most recent data is at index 0, we need to reverse the direction of comparison.
            return (df['Close'].iloc[:length].diff(periods=-1).iloc[:-1] < 0).all()
        except Exception as e:
            print(f"Failed - {e}")

    def is_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return (lower_shadow >= 2 * body_length) and (upper_shadow <= body_length)

    def is_inverted_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Open'], row['Close'])
        lower_shadow = min(row['Open'], row['Close']) - row['Low']
        return (upper_shadow >= 2 * body_length) and (lower_shadow <= body_length)

    def is_hanging_man(self, row):
        return self.is_hammer(row)

    def is_shooting_star(self, row):
        return self.is_inverted_hammer(row)

    def is_doji(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range

    def is_bullish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_bearish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bullish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] > prev_row['Close']) and (curr_row['Open'] < curr_row['Close']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bearish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] < prev_row['Close']) and (curr_row['Open'] > curr_row['Close']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_morning_star(self,prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bullish = curr_row['Close'] > curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_above_first_mid = curr_row['Close'] > first_midpoint
        return first_bearish and second_small_body and third_bullish and third_close_above_first_mid

    def is_evening_star(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bearish = curr_row['Close'] < curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_below_first_mid = curr_row['Close'] < first_midpoint
        return first_bullish and second_small_body and third_bearish and third_close_below_first_mid

    def is_piercing_line(self,prev_row, curr_row):
        first_bearish = prev_row['Close'] < prev_row['Open']
        second_bullish = curr_row['Close'] > curr_row['Open']
        open_below_prev_low = curr_row['Open'] < prev_row['Low']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_above_prev_mid = curr_row['Close'] > prev_midpoint
        return first_bearish and second_bullish and open_below_prev_low and close_above_prev_mid
        
    def has_gap_last_4_candles(self, ohlcv, index):
        """
        Checks if there's a gap within the last 4 candles, either up or down.
        A gap up occurs when the current open is higher than the previous close,
        and a gap down occurs when the current open is lower than the previous close.
        
        :param ohlcv: The OHLCV dataframe with historical data.
        :param index: The current index in the dataframe.
        :return: Boolean value indicating whether a gap exists in the last 4 candles.
        """
        # Ensure there are at least 4 candles to check
        if index < 3:
            return False

        # Iterate through the last 4 candles
        for i in range(index - 3, index):
            curr_open = ohlcv.iloc[i + 1]['Open']
            prev_close = ohlcv.iloc[i]['Close']
            
            # Check for a gap (either up or down)
            if curr_open > prev_close or curr_open < prev_close:
                return True  # A gap is found

        return False  # No gap found in the last 4 candles

    def is_abandoned_baby(self, prev_prev_row, prev_row, curr_row):
        # Bullish Abandoned Baby
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        doji = self.is_doji(prev_row)
        third_bullish = curr_row['Close'] > curr_row['Open']
        
        # Check for gaps
        gap_down = prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Low']
        gap_up = curr_row['Open'] > prev_row['Close'] and curr_row['Close'] > prev_row['High']
        
        return first_bearish and doji and third_bullish and gap_down and gap_up

    def is_harami_cross(self, prev_row, curr_row):
        # Harami Cross is a special form of Harami with the second candle being a Doji
        return self.is_bullish_harami(prev_row, curr_row) and self.is_doji(curr_row)

    def is_rising_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Rising Three Methods (Bullish Continuation)
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        small_bearish = prev_row['Close'] < prev_row['Open'] and prev_row['Close'] > prev_prev_row['Open']
        final_bullish = curr_row['Close'] > curr_row['Open'] and curr_row['Close'] > prev_prev_row['Close']
        
        return first_bullish and small_bearish and final_bullish

    def is_falling_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Falling Three Methods (Bearish Continuation)
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        small_bullish = prev_row['Close'] > prev_row['Open'] and prev_row['Close'] < prev_prev_row['Open']
        final_bearish = curr_row['Close'] < curr_row['Open'] and curr_row['Close'] < prev_prev_row['Close']
        
        return first_bearish and small_bullish and final_bearish

    def is_three_inside_down(self, prev_prev_row, prev_row, curr_row):
        # Bearish reversal pattern
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        
        return (first_bullish and second_bearish and third_bearish and
                prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] > prev_prev_row['Open'] and
                curr_row['Close'] < prev_prev_row['Open'])
    def is_dark_cloud_cover(self,prev_row, curr_row):
        first_bullish = prev_row['Close'] > prev_row['Open']
        second_bearish = curr_row['Close'] < curr_row['Open']
        open_above_prev_high = curr_row['Open'] > prev_row['High']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_below_prev_mid = curr_row['Close'] < prev_midpoint
        return first_bullish and second_bearish and open_above_prev_high and close_below_prev_mid

    def is_three_white_soldiers(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bullish and second_bullish and third_bullish and
                prev_row['Open'] < prev_prev_row['Close'] and curr_row['Open'] < prev_row['Close'] and
                prev_row['Close'] > prev_prev_row['Close'] and curr_row['Close'] > prev_row['Close'])

    def is_three_black_crows(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        return (first_bearish and second_bearish and third_bearish and
                prev_row['Open'] > prev_prev_row['Close'] and curr_row['Open'] > prev_row['Close'] and
                prev_row['Close'] < prev_prev_row['Close'] and curr_row['Close'] < prev_row['Close'])
    




    async def get_candle_streak(self, ticker, headers=None):
        """Returns the streak and trend (up or down) for each timespan, along with the ticker"""
        
        async def calculate_streak(ticker, interval, data):
            """Helper function to calculate the streak and trend for a given dataset"""
            # Conversion dictionary to map intervals to human-readable timespans
            conversion = { 
                'm1': '1min',
                'm5': '5min',
                'm30': '30min',
                'm60': '1h',
                'm120': '2h',
                'm240': '4h',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            # Initialize variables
            streak_type = None
            streak_length = 1  # Starting with 1 since the most recent candle is part of the streak

            # Start from the most recent candle and scan forward through the data
            for i in range(1, len(data)):
                current_open = data['Open'].iloc[i]
                current_close = data['Close'].iloc[i]

                # Determine if the candle is green (up) or red (down)
                if current_close > current_open:
                    current_streak_type = 'up'
                elif current_close < current_open:
                    current_streak_type = 'down'
                else:
                    break  # Stop if the candle is neutral (no movement)

                if streak_type is None:
                    streak_type = current_streak_type  # Set initial streak type
                elif streak_type != current_streak_type:
                    break  # Break if the trend changes (from up to down or vice versa)

                streak_length += 1

            if streak_type is None:
                return {f"streak_{conversion[interval]}": 0, f"trend_{conversion[interval]}": "no trend"}

            return {f"streak_{conversion[interval]}": streak_length, f"trend_{conversion[interval]}": streak_type}


        try:
            # Define the intervals of interest
            intervals = ['d', 'w', 'm', 'm5', 'm30', 'm60', 'm120', 'm240']  # Choose 4h, day, and week for your example

            # Fetch the data asynchronously for all intervals
            # Fetch the data asynchronously for all intervals
            data_list = await asyncio.gather(
                *[self.get_candle_data(ticker=ticker, interval=interval, headers=headers, count=200) for interval in intervals]
            )

            # Process each interval's data and gather the streak and trend
            streak_data = {}
            for interval, data in zip(intervals, data_list):
                result = await calculate_streak(ticker, interval, data)
                streak_data.update(result)  # Add the streak and trend for each timespan

            # Add the ticker to the result
            streak_data["ticker"] = ticker

            return streak_data

        except Exception as e:
            print(f"{ticker}: {e}")
            return None



    def classify_candle(self,open_value, close_value):
        if close_value > open_value:
            return "green"
        elif close_value < open_value:
            return "red"
        else:
            return "neutral"

    # Function to classify candle colors across all intervals
    def classify_candle_set(self,opens, closes):
        return [self.classify_candle(open_val, close_val) for open_val, close_val in zip(opens, closes)]

    # Function to classify shapes across rows for one set of rows
    def classify_shape(self,open_val, high_val, low_val, close_val, color, interval, ticker):
        body = abs(close_val - open_val)
        upper_wick = high_val - max(open_val, close_val)
        lower_wick = min(open_val, close_val) - low_val
        total_range = high_val - low_val

        if total_range == 0:
            return None  # Skip if there's no valid data

        body_percentage = (body / total_range) * 100
        upper_wick_percentage = (upper_wick / total_range) * 100
        lower_wick_percentage = (lower_wick / total_range) * 100

        if body_percentage < 10 and upper_wick_percentage > 45 and lower_wick_percentage > 45:
            return f"Doji ({color}) - {ticker} [{interval}]"
        elif body_percentage > 60 and upper_wick_percentage < 20 and lower_wick_percentage < 20:
            return f"Long Body ({color}) - {ticker} [{interval}]"
        elif body_percentage < 30 and lower_wick_percentage > 50:
            return f"Hammer ({color}) - {ticker} [{interval}]" if color == "green" else f"Hanging Man ({color}) - {ticker} [{interval}]"
        elif body_percentage < 30 and upper_wick_percentage > 50:
            return f"Inverted Hammer ({color}) - {ticker} [{interval}]" if color == "green" else f"Shooting Star ({color}) - {ticker} [{interval}]"
        elif body_percentage < 50 and upper_wick_percentage > 20 and lower_wick_percentage > 20:
            return f"Spinning Top ({color}) - {ticker} [{interval}]"
        else:
            return f"Neutral ({color}) - {ticker} [{interval}]"

    # Function to classify candle shapes across all intervals for a given ticker
    def classify_candle_shapes(self, opens, highs, lows, closes, colors, intervals, ticker):
        return [self.classify_shape(open_val, high_val, low_val, close_val, color, interval, ticker)
                for open_val, high_val, low_val, close_val, color, interval in zip(opens, highs, lows, closes, colors, intervals)]



    async def get_candle_patterns(self, ticker:str='AAPL', interval:str='m60', headers=None):

        # Function to compare two consecutive candles and detect patterns like engulfing and tweezers
        def compare_candles(open1, close1, high1, low1, color1, open2, close2, high2, low2, color2, interval, ticker):
            conversion = { 
                'm1': '1min',
                'm5': '5min',
                'm30': '30min',
                'm60': '1h',
                'm120': '2h',
                'm240': '4h',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            # Bullish Engulfing
            if color1 == "red" and color2 == "green" and open2 < close1 and close2 > open1:
                candle_pattern = f"Bullish Engulfing - {ticker} {conversion.get(interval)}"
                return candle_pattern
            # Bearish Engulfing
            elif color1 == "green" and color2 == "red" and open2 > close1 and close2 < open1:
                candle_pattern = f"Bearish Engulfing - {conversion.get(interval)}"
                return candle_pattern
            # Tweezer Top
            elif color1 == "green" and color2 == "red" and high1 == high2:
                candle_pattern = f"Tweezer Top - {conversion.get(interval)}"
                return candle_pattern
            # Tweezer Bottom
            elif color1 == "red" and color2 == "green" and low1 == low2:
                candle_pattern = f"tweezer_bottom"
                return candle_pattern
            
    
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            df = df[::-1]

            color1 = 'red' if df['Open'].loc[0] > df['Close'].loc[0] else 'green' if df['Close'].loc[0] > df['Open'].loc[0] else 'grey'
            color2 = 'red' if df['Open'].loc[1] > df['Close'].loc[1] else 'green' if df['Close'].loc[1] > df['Open'].loc[1] else 'grey'




            candle_pattern = compare_candles(close1=df['Close'].loc[0], close2=df['Close'].loc[1], high1=df['High'].loc[0], high2=df['High'].loc[1], low1=df['Low'].loc[0], low2=df['Low'].loc[1], open1=df['Open'].loc[0], open2=df['Open'].loc[1], color1=color1, color2=color2, interval=interval, ticker=ticker)
            if candle_pattern is not []:
                dict = { 
                    'ticker': ticker,
                    'interval': interval,
                    'shape': candle_pattern
                }

                df = pd.DataFrame(dict, index=[0])
                if df['shape'] is not None:
                    return df
        except Exception as e:
            print(e)


    async def get_second_ticks(self, headers, ticker:str, second_timespan:str='5s',count:str='800'):
        ticker_id = await self.get_webull_id(ticker)
        url=f"https://quotes-gw.webullfintech.com/api/quote/charts/seconds-mini?type={second_timespan}&count={count}&restorationType=0&tickerId={ticker_id}"



        async with httpx.AsyncClient(headers=headers) as client:
            data = await client.get(url)

            data = data.json()

            data = [i.get('data') for i in data]

            for i in data:
                print(i)


    async def macd_rsi(self, rsi_type, macd_type, size:str='50'):

        async with httpx.AsyncClient() as client:
            data = await client.get(f"https://quotes-gw.webullfintech.com/api/wlas/ranking/rsi-macd?rankType=rsi_macd&regionId=6&supportBroker=8&rsi=rsi.{rsi_type}&macd=macd.{macd_type}&direction=-1&pageIndex=1&pageSize={size}")

            data = data.json()
            data = data['data']
            ticker = [i.get('ticker') for i in data]
            symbols = [i.get('symbol') for i in ticker]

            return symbols
