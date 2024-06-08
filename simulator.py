import yfinance as yfin

""" But say you have one (or more) arguments in method1:

def method1(param):
    return 'hello ' + str(param)

def method2(methodToRun):
    result = methodToRun()
    return result

Then you can simply invoke method2 as method2(lambda: method1('world')).

method2(lambda: method1('world'))
>>> hello world
method2(lambda: method1('reader'))
>>> hello reader """



def simulate_strategy_day(symbol, day, strategy):
    