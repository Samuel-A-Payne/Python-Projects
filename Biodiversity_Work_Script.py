from matplotlib import pyplot as plt
import pandas as pd
from tabulate import tabulate
import seaborn as sns
from scipy.stats import chi2_contingency


#----------------------------
#----------------------------


#Reading in 'species_info.csv' as a dataframe using pandas
species = pd.read_csv('species_info.csv')

#The following code re-orients the dataframe. The first line allows every column to be viewed. The second line prevents each column from wrapping, so that
#every column is on the same line/axis
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

print(species.head())


#----------------------------
#----------------------------


### ANSWERING QUESTIONS ABOUT THE DATAFRAME ###

#How many different species are in the "Species" dataframe?
nunique_spec = species.scientific_name.nunique()
print('\n')
print('There are ' + str(nunique_spec) + ' species in the dataframe.\n')

#What are the different values in the "Species" dataframe column, 'category'?
spec_cats = species.category.unique()
print('The following categories of animal species are present within the dataframe: ' + str(spec_cats) + '.\n')

#What are the different values in the "Species" dataframe column, 'conservation_status'?
spec_statuses = species.conservation_status.unique()
print('The following conservation statuses are present within the dataframe: ' + str(spec_statuses) + '.\n')


#----------------------------
#----------------------------


### Analysis of Dataframe ###

#Creating a frequency table of conservation status by species scientific_name
#The first line of code takes the null values present in the column and creates a row title as specified, 'No Intervention'
species.fillna('No Intervention', inplace=True)
spec_conser_freqtab = species.groupby('conservation_status').scientific_name.nunique().reset_index()

print(spec_conser_freqtab)
print('\n')

#Creating a new dataframe -- ***NOTE: We took the same code as before and simply added the '.sort_values()' function, which sorts the "scientific_name" column by species counts
protection_counts = species.groupby('conservation_status')\
    .scientific_name.nunique().reset_index()\
    .sort_values(by='scientific_name')

print(protection_counts)
print('\n')


#----------------------------
#----------------------------


### Creating a Barchart ###

#Using Seaborn library to create a barplot
# sns.barplot(data=protection_counts, x="conservation_status", y="scientific_name").set(title="Conservation Status by Species Count")
# plt.show()

#Using matplotlib to generate the same barchart as above
# plt.figure(figsize=(10, 4))
# ax = plt.subplot()
# plt.bar(range(len(protection_counts)),
#         protection_counts["scientific_name"].values)
# ax.set_xticks(range(len(protection_counts)))
# ax.set_xticklabels(protection_counts["conservation_status"].values)
# plt.ylabel('Number of Species')
# plt.title('Conservation Status by Species')
# plt.show()


#----------------------------
#----------------------------


### Are certain types of species more likely to be endangered? ###

#Creating a new column in our dataframe. If there is no intervention, then it's false. If there IS intervention, then it's true
species['is_protected'] = species['conservation_status'] != 'No Intervention'
print(species)

#By using the loc() function, we can select a single row from the species dataframe. Below, we're selecting row 8 (index 7) to check
# whether our != 'No Intervention' equals True works - it does!
print(species.loc[7])
print('\n')

#Grouping the species dataframe by 'category' and 'Is Protected' columns, then counting unique 'scientific_name'
category_counts = species.groupby(['category', 'is_protected']).scientific_name.nunique().reset_index()

#Checking the first 10 rows of our "category_counts" frequency table
print(category_counts.head(10))
print('\n')

#Rearranging the newly created frequency table by using "pivot()" function to rearrange "category_counts"
category_pivot = category_counts.pivot(columns='is_protected', index='category', values='scientific_name').reset_index()

print(category_pivot)
print('\n')

#We have created a solid frequency table! Let's get more descriptive by changing the false and true columns to be more descriptive
category_pivot.columns = ['category', 'not_protected', 'protected']

print(category_pivot)
print('\n')

#Creating a new column in our "category_pivot" DF for percentages of 'not_protected' vs. 'protected' species categories
#Keep in mind that we're just manipulating the values in our "category_pivot" DF, so we don't need to call our "species" DF!
category_pivot['percent_protected'] = category_pivot['protected']/ \
                                      (category_pivot['protected'] + category_pivot['not_protected'])

print(category_pivot, '\n')
print('------------------------------\n')

# Now that we've generated a solid frequency table of protected status by species category, let's do some hypothesis testing.
# Which hypothesis test should we run if we wanted to compare which categories are more likely to be protected/not protected?
# Since we are comparing categorical variables like 'category' and 'protection status', a chi squared test should work fine!


#----------------------------
#----------------------------


### Running a Chi-Squared Hypothesis Test ###

#Let's run a chi-squared test to examine whether mammals are more likely to be endangered than birds, based off our last frequency table

# First, we need to create a contingency table and populate it with our values in question - ***NOTE: our table is populated with protected 1st, not_protected 2nd, AND mammal before bird
contingency = [[30, 146],\
               [75, 413]]

#Running actual chi-squared test using our contingency table and printing results:
print('The results of our chi-squared test did not reveal any statistical significance between mammals and birds, as shown below: \n' + str(chi2_contingency(contingency)) + '\n')

#Running another chi-squared test using our updated contingency table (mammals vs. reptiles) and printing results:
contingency2 = [[30, 146],\
               [5, 73]]
print('The results of our chi-squared test DID in fact reveal statistically significant difference between mammals and reptiles, as shown below:\
\n' + str(chi2_contingency(contingency2)))
print('\n------------------------------\n')


#----------------------------
#----------------------------


### Investigating New "Observations" Dataset ###

#The purpose of this exercise is to determine how many observed species of sheep are in the "observations" dataset. The only problem is that there is no 'common_name' column,
#only scientific name. We're going to create a new column in our "species" DF that spits out whether a species is a sheep or not

#Loading and investigating new dataset
observations = pd.read_csv('observations.csv')
print(observations.head(10))
print('\n')

#Creating a new column in our "species" DF
species['is_sheep'] = species['common_names'].apply(lambda x: 'Sheep' in x)
print(species.head(10))
print('\n')

#Selecting rows in our "species" DF where 'is_sheep' is True:
print(species[species.is_sheep])
print('\n')

#From our output table, it looks like some plant species have "sheep" in the common name. Let's further filter by selecting rows where 'is_sheep' is True
# and 'category' == mammal
sheep_species = species[(species.is_sheep) & (species.category == 'Mammal')]
print(sheep_species)
print('\n')

#Merging our "observations" and "sheep_species" dataframes to link up our sheep values from species to oberservations scientific_name!
sheep_observations = observations.merge(sheep_species)
print(sheep_observations)
print('\n------------------------------\n')


#----------------------------
#----------------------------


### Conducting Further Analysis on the Merged Dataframe ###

#Counting up how many of each sheep species was found at each park by using the 'groupby()' function again:
obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
print('The total number of sheep observations by park in the past 7 days is as follows:\n' + str(obs_by_park) + '\n')

### Try creating a new table that also breaks down the observations by sheep species as a side-task to test your skills! (Made up by me)


#----------------------------
#----------------------------

### Creating Barcharts ###

#Creating a bar chart using seaborn
# sns.barplot(data=obs_by_park, x="park_name", y="observations").set(title="Observations by Sheep per Week")
# plt.show()

#Creating the same bar chart using matplotlib
# plt.figure(figsize=(16,4))
# ax = plt.subplot()
# plt.bar(range(len(obs_by_park)), obs_by_park.observations.values)
# ax.set_xticks(range(len(obs_by_park)))
# ax.set_xticklabels(obs_by_park.park_name)
# plt.xlabel("National Parks")
# plt.ylabel('Number of Observations')
# plt.title('Observations of Sheep per Week')
# plt.show()
print('\n------------------------------\n')

#----------------------------
#----------------------------

### Creating a Sample Size ###

#Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease. Park rangers at Yellowstone National Park have been running a program to reduce the rate
# of foot and mouth disease at that park. The scientists want to test whether or not this program is working. They want to be able to detect reductions of at least 5 percentage points.
# For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.

#Use Codecademy's sample size calculator to calculate the number of sheep that they would need to observe from each park. Use the default level of significance (90%).
#Remember that "Minimum Detectable Effect" is a percent of the baseline.

#----------------------------
# Bryce National Park #
#----------------------------

#Calculating the minimum detectable effect for Bryce National Park
minimum_detectable_effect_bryce = 100 * 0.05 / 0.15
print('Our mimimum detectable effect for Bryce National is: ' + str(minimum_detectable_effect_bryce) + ' percent.')

baseline_conversion_rate_bryce = 15 #percent

#Therefore, our sample size requirement is 870!
sample_size_per_variant_bryce = 870

### How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?

#Below we calculate for Bryce National Park since that was the data we had on hand in the instructions:
bryce = 870 / 250.

#----------------------------
# Yellowstone National Park #
#----------------------------

#Calculating the minimum detectable effect for Yellowstone National Park
minimum_detectable_effect_yellow = 100 * 0.05 / 0.10
print('Our minimum detectable effect for Yellowstone National is: ' + str(minimum_detectable_effect_yellow) + ' percent.\n')

baseline_conversion_rate_yellow = 10 #percent

#Therefore, our sample size requirement is 610!
sample_size_per_variant = 610

### How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

#Below we calculate for Yellowstone National Park since that was the data we had on hand in the instructions:
yellowstone = 610 / 507.

#Outputting the length of time in weeks for each Park:
print('It would therefore take approximately ' + str(bryce) + ' weeks at Bryce National and ' + str(yellowstone) + ' weeks at Yellowstone National to generate sufficient sample sizes.')