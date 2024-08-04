import mplfinance as mpf
import pandas as pd
#from PIL import Image
import os

#function takes a dataframe(s) as inputs and displays them if there is 5 or less
# if it is greater than or save flagged itll save the graphs instead to prevent overflow
def candleStickMaker(graphData, save):
    for key in graphData:

        tickerData = graphData[key][0]
        day = graphData[key][1]

        #TODO add trigger subplots to candelstick if they exist
        if len(graphData[key]) == 3:
            #print("hello world!")
            triggers = graphData[key][2]
            #data variable and formatting to display data on top off graph
            #now lets create our buy/sell/other important flags from our strategy data set to add as an overlay on the plot
            #Triggers should be a dataframe of same x axis and y axis as graph data dataframe
            #then we want to process those triggers to either the buy or sells or other respective actions 
            #create a subplot for each action and add to our plot
            buys = []
            sells = []
            #buysPlot = mpf.make_addplot(buys, type='scatter', markersize=200, marker='^')
            #sellsPlot = mpf.make_addplot(sells, type='scatter', markersize=200, marker='v')

        #make sure our x axis index is formatted property
        tickerData.index = pd.to_datetime(tickerData.index)
        tickerData.index = tickerData.index.tz_localize(None)

        plot_args = {
            'type': "candle",
            'title': f"Stock: {key} Day: {day}",
            'style': "yahoo",
            'volume': True,
            'figratio': (16, 6),
            #'figscale': 2,
            'returnfig': True,
            'show_nontrading': False
        }

        if save:
            parentDir = 'C:/Users/tynan/code_work_personal/savedGraphs/'
            pathString = parentDir + day
            if not os.path.exists(pathString):
                print("Making the days folder")
                os.mkdir(pathString)
            filename = pathString + '/' + key + ".png"
            plot_args['savefig'] = filename
        
        #candlestick plot the data for the day
        fig, axlist = mpf.plot(tickerData, **plot_args, block=False, tight_layout=True, scale_padding={'left': 0.15, 'right': 2.25})
            
    if not save:
        mpf.show()
    return

  