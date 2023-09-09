import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


#-----------------------------------
#-----------------------------------

### LOADING THE DATASETS AND INSPECTING THEM ###

#The following code re-orients the dataframe. The first line allows every column to be viewed. The second line prevents each column from wrapping, so that
#every column is on the same line/axis
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

#Importing datasets as dataframes
netflix_stocks = pd.read_csv('NFLX.csv')
# print(netflix_stocks)
# print('\n')

netflix_stock_quar = pd.read_csv('NFLX_daily_by_quarter.csv')
print(netflix_stock_quar)
print('\n')

dowjones_industrial = pd.read_csv('DJI.csv')
# print(netflix_stock_quar)
# print('\n')

### What questions can we ask?

#1) What year is represented by the data? 2017
#2) Is the data represented in days, weeks, or months? "netflix_stocks" is by MONTH, and "netflix_stock_quar" & "dowjones_industrial" is DAY


#-----------------------------------
#-----------------------------------

### MANIPULATING THE DATA ###

#Changing column name of "Adj Close" to just "Price" so that it's easier to work with the data. We will do it for both our "netflix_stocks" and "dowjones_industrial" DF's
netflix_stocks.rename(columns={'Adj Close':'Price'}, inplace=True)
# print(netflix_stocks)
# print('\n')

netflix_stock_quar.rename(columns={'Adj Close':'Price'}, inplace=True)
# print(netflix_stock_quar)
# print('\n')

dowjones_industrial.rename(columns={'Adj Close':'Price'}, inplace=True)
# print(dowjones_industrial)
# print('\n')


#-----------------------------------
#-----------------------------------

### VISUALIZING THE DISTRIBUTION OF DATA ###

#Creating a violin plot using seaborn to calculate and measure several distributions like the densities of data points, as well as a 5-point data summary - ***NOTE: It's a combination of box-whisker plots and
#Kernel Density Estimator (KDE) plots! It's super useful as it takes the distribution given by a histogram (smooth line instead of rectangular boxes (think sand pile instead of box on data point) while giving
#5 point data summary of a box-and-whisker plot)

#We're going to plot the "price" column. We're going to set our violin plot to the variable, "ax" because that allows us to instantiate the figure to allow us access to the axes using matplotlib!
# ax = sns.violinplot(netflix_stocks.Price, color='red')
# ax.set(xlabel ="", ylabel = "Price", title ='Distribution of 2017 Netflix Stock Price')
# plt.show()


#-----------------------------------
#-----------------------------------

### VISUALIZING THE DATA USING SCATTERPLOT ###

#In this next exercise, we will chart the performance of dividends by their estimated projected value and their actual value per QUARTER using a very simple scatterplot
x_positions = [1, 2, 3, 4]
chart_labels = ["1Q2017","2Q2017","3Q2017","4Q2017"]
earnings_actual =[.4, .15,.29,.41]
earnings_estimate = [.37,.15,.32,.41]

plt.scatter(x_positions, earnings_estimate, color='blue', alpha=0.5)
plt.scatter(x_positions, earnings_actual, color='red', alpha=0.5)
plt.xticks(x_positions, chart_labels)
plt.legend(['Estimate', 'Actual'])
plt.title("Earnings Per Share in Cents")
plt.show()

#From the scatterplot above, we can determine that any purple shaded data point suggests that both the estimated and actual earning overlaps because they are equal! Note the purple color (blue + red = purple)


#-----------------------------------
#-----------------------------------

### VISUALIZING THE DATA USING SIDE-BY-SIDE BAR CHARTS ###

#In this next exercise, we will create a side-by-side barchart to compare Netflix's earnings to its revenue. Refer to the following code to complete:

#-----------------------------------

#First we need to set up our x-axes (the following lists are provided by Codecademy:
revenue_by_quarter = [2.79, 2.98,3.29,3.7]
earnings_by_quarter = [.0656,.12959,.18552,.29012]
quarter_labels = ["2Q2017","3Q2017","4Q2017", "1Q2018"]

#The following code doesn't ever need to be changed for side-by-side bar graphs. It should ALWAYS work!

# [t*element + w*n for element in range(d)]

#Now, we can create our code schematic to plug in the above code formula into:

#Dataset 1 out of 2
n = 1
#Total number of datasets
t = 2
#Number of sets of bars (4 because there are 4 quarters we are measuring)
d = 4
#Width of the bars (default is 0.8)
w = 0.8
#Our first x-axis values for Dataset 1
bars1_x = [t*element + w*n for element in range(d)]

#Creating our bar chart with Dataset 1!
plt.bar(bars1_x, revenue_by_quarter)

#---------------------------

#Now, we follow the same steps above in our Dataset 1 bar chart schematic, with slight variations:
n = 2
t = 2
d = 4
w = 0.8
bars2_x = [t*element + w*n for element in range(d)]

#Creating our bar chart with Dataset 1!
plt.bar(bars2_x, earnings_by_quarter)

#--------------------------------------------

#Outputting our bar chart with labels!

#Creating our axes object to begin properly labeling our bar chart! ***NOTE: In order to set the tick marks in the MIDDLE of the side-by-side bars,
# we have to specify the lengths of the two bars and divide by 2. We use a list comprehension to achieve this, and store it in a variable, "middle_x"
middle_x = [((a + b) / 2) for a,b in zip(bars1_x, bars2_x)]

#Now, we actually SET the x-ticks by calling the 'middle_x' list after establishing our 'ax = plt.subplot()'!
ax = plt.subplot()
ax.set_xticks(middle_x)
ax.set_xticklabels(quarter_labels)

### Alternatively, we don't even need to set an "ax" variable and call it as in the previous 3 lines of code. The following code will still work:
### plt.xticks(middle_x, quarter_labels)

#Now, let's provide some descriptive labels!

labels = ['Revenue', 'Earnings']
plt.legend(labels)
plt.title("Netflix Revenue and Earnings in $ Billions")
plt.show()


#-----------------------------------
#-----------------------------------

### VISUALIZING THE DATA USING SIDE-BY-SIDE LINE CHARTS ###

#Using the 'plt.subplot()' function, we will create a subplot of our provided variables above
plt.subplot(1, 2, 1)
plt.plot(netflix_stocks.Date, netflix_stocks.Price, marker='o', color='red')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Netflix Stock Price by Month')
plt.xticks(rotation='vertical')

plt.subplot(1, 2, 2)
plt.plot(dowjones_industrial.Date, dowjones_industrial.Price, marker='o', color='blue')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Dow Jones Stock Price by Month')
plt.xticks(rotation='vertical')

#The following function, 'plt.subplots_adjust()' manipulates the height, width, and spacing of our subplots! This is unncecessary to this exercise,
# but it is good practice in customizing subplots!
plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.5,
                    hspace=0.4)

#Finally, we call the 'plt.show()' function to output our line graphs!
plt.show()

#-----------------------------------------------------------

### The following code will achieve the same as above, but it's just creating axes 1 and 2 to modify! ###

### Left plot Netflix
### ax1 = plt.subplot(total rows, total columns, subplot to modify)


# ax1 = plt.subplot(1, 2, 1)
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Stock Price')
# ax1.set_title("Netflix")
#
# plt.xticks(rotation='vertical')
#
# plt.plot(netflix_stocks['Date'], netflix_stocks['Price'], color="purple")

#---------------------------

### Right plot Dow Jones
### ax2 = plt.subplot(total rows, total columns, subplot to modify)


# ax2 = plt.subplot(1, 2, 2)
# ax2.set_xlabel('Date')
# ax2.set_ylabel('Stock Price')
# ax2.set_title("Dow Jones")
# plt.xticks(rotation='vertical')
# plt.plot(dowjones_stocks['Date'], dowjones_stocks['Price'], color="green")
# plt.subplots_adjust(wspace=.5)
# plt.show()