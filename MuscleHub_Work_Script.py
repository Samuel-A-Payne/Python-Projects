from codecademySQL import sql_query
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency


#----------------------------
#----------------------------


#The following code re-orients the dataframe: The first line of code allows every column to be viewed, while the second line prevents each column from wrapping, so that
#every column is on the same line/axis
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)


#----------------------------
#----------------------------

### INSPECTING AND CLEANING DATA TO PRODUCE WORKABLE DATAFRAME ###

visits = sql_query('''
SELECT *
FROM visits
LIMIT 5
''')
print(visits)
print('\n')

fitness_tests = sql_query('''
SELECT *
FROM fitness_tests
LIMIT 5
''')
print(fitness_tests)
print('\n')

applications = sql_query('''
SELECT *
FROM applications
LIMIT 5
''')
print(applications)
print('\n')

purchases = sql_query('''
SELECT *
FROM purchases
LIMIT 5
''')
print(purchases)
print('\n----------------------------------------\n')

#Creating a dataframe with all relevant info from four datasets using SQL Queries:
df = sql_query('''
SELECT visits.first_name,
       visits.last_name,
       visits.email,
       visits.gender,
       visits.visit_date,
       fitness_tests.fitness_test_date,
       applications.application_date,
       purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON fitness_tests.first_name = visits.first_name
    AND fitness_tests.last_name = visits.last_name
    AND fitness_tests.email = visits.email
LEFT JOIN applications
    ON applications.first_name = visits.first_name
    AND applications.last_name = visits.last_name
    AND applications.email = visits.email
LEFT JOIN purchases
    ON purchases.first_name = visits.first_name
    AND purchases.last_name = visits.last_name
    AND purchases.email = visits.email
WHERE visits.visit_date >= '7-1-17'
''')
print(df)
print('\n----------------------------------------\n')


#----------------------------
#----------------------------

### ADDING COLUMNS TO DATAFRAME (DF) ###

df['ab_test_group'] = df.fitness_test_date.apply(lambda x: 'A' if pd.notnull(x) else 'B')
print(df)
print('\n----------------------------------------\n')

#Counting up the number of Group A vs. Group B people using Groupby and counting up each person using their first_name -- ***NOTE: We'll be using 'first_name' to count up each group!
ab_counts = df.groupby('ab_test_group').first_name.count().reset_index()
print(ab_counts)
print('\n')

#Creating a pie chart to visualize our frequency table - ***NOTE: We add the legend in the first line by using labels
# plt.pie(ab_counts.first_name.values, labels=['A', 'B'], autopct='%0.2f%%')
# plt.axis('equal')
# plt.show()
# # Saving the pie chart to our project notebook as a png file
# plt.savefig('ab_test_pie_chart.png')

#------------------------------

#Creating another column for number of actual applicants (Same as we did above for fitness_test_dates)
df['is_application'] = df.application_date.apply(lambda x: 'Application' if pd.notnull(x) else 'No Application')
print(df)
print('\n')

#Creating another frequency table, but this time for applicants vs ab_counts
app_counts = df.groupby(['ab_test_group', 'is_application']).first_name.count().reset_index()
print(app_counts)
print('\n')

#Rearranging the newly created frequency table by using "pivot()" function to rearrange "app_counts"
app_pivot = app_counts.pivot(columns='is_application',
                             index='ab_test_group',
                             values='first_name')\
                             .reset_index()
print(app_pivot)
print('\n')

#Creating a new column for our pivoted frequency table that totals number of apps vs. no_apps
app_pivot['Total'] = app_pivot.Application + app_pivot['No Application']
print(app_pivot)
print('\n')

#Creating a new column for our pivoted frequency table that calculates the percentages of apps vs. no_apps
app_pivot['Percent with Application'] = app_pivot.Application / app_pivot.Total
print(app_pivot)
print('\n')

#----------------------------
#----------------------------

### RUNNING A HYPOTHESIS TEST TO MEASURE SIGNIFICANCE BETWEEN BOTH GROUPS ###

#Since we're comparing statistical significance between two cat variables with multiple sub-variables, we should use a chi-squared test

#Creating the contingency table -- ***NOTE: We're running the test with Group A first
contingency = [[250,2254], [325,2175]]

#Running a chi-squared test
chi2_contingency(contingency)

print('The results of our chi-squared test DID in fact reveal statistically significant difference between GroupA and GroupB, as shown below:\
\n' + str(chi2_contingency(contingency)))
print('\n------------------------------\n')


#----------------------------
#----------------------------

### CREATING A FREQUENCY CHART FOR APPLICATIONS VS. ACTUAL PURCHASES ###

#We're going to add another column to our main DF that shows the number of applications that resulted in a purchase
print(df)
print('\n')

df['is_member'] = df.purchase_date.apply(lambda x: 'Member' if pd.notnull(x) else 'Not Member')
print(df)
print('\n')

#Creating a new DF for people who ONLY picked up an application. THIS IS IMPORTANT! Because we are ONLY interested in actual applications because
#nobody will have made a purchase if they didn't first apply! For the purposes of creating a frequency table next, we don't need to use our main DF, "df", just "just_apps"
just_apps = df[df.is_application == 'Application']
print(just_apps)

#Creating a frequency table of people who submitted an application to see what A or B group they belong to - ***NOTE: We DO NOT need to include "Application Counts" in
#our frequency table. Why? Because we already filtered a new dataframe called, "just_apps" that is ONLY made up of data from people who submitted Applications! So really wer're
#just trying to determine from that DF, what number/percent went on to actually become a member by making a purchase from "purchase_date"
member_counts = just_apps.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()
print(member_counts)
print('\n')

#Rearranging the newly created frequency table by using "pivot()" function to rearrange "member_counts"
member_pivot = member_counts.pivot(columns='is_member',
                                   index='ab_test_group',
                                   values='first_name')\
                                   .reset_index()
print(member_pivot)
print('\n')

#Creating a new column for our pivoted frequency table that totals number of Members vs. Non-members
member_pivot["Total"] = member_pivot['Member'] + member_pivot['Not Member']
print(member_pivot)
print('\n')

#Creating a new column for our pivoted frequency table that calculates the percentages of Members vs. Not Members
member_pivot['Percent Purchase'] = member_pivot['Member'] / member_pivot['Total']
print(member_pivot)
print('\n')


#----------------------------
#----------------------------

### RUNNING A HYPOTHESIS TEST TO MEASURE SIGNIFICANCE BETWEEN BOTH GROUPS ###

#Since we're comparing statistical significance between two cat variables with multiple sub-variables, we should use a chi-squared test just as before!

#Creating the contingency table -- ***NOTE: We're running the test with Group A first
contingency2 = [[200,50], [250,75]]

#Running a chi-squared test
chi2_contingency(contingency2)

print('The results of our chi-squared test DID NOT in fact reveal statistically significant difference between GroupA and GroupB, as shown below:\
\n' + str(chi2_contingency(contingency2)))
print('\n------------------------------\n')


#----------------------------
#----------------------------

### CREATING A FREQUENCY TABLE FOLLOWED-BY A CHI-SQUARED TEST TO TEST FOR SIGNIFICANCE BETWEEN VISITORS AND PURCHASES ###

#Let's start by creating a frequency table as we did twice before, but instead of filtering out info, we're going to compare total number of visitors
#from Groups A and B by their membership status! -- ***HINT: It's the same block of code as before, but we're just using the "df" dataframe instead of "just_apps"!
final_member_counts = df.groupby(['ab_test_group', 'is_member']).first_name.count().reset_index()
# print(final_member_counts)
# print('\n')

#Rearranging the newly created frequency table by using "pivot()" function to rearrange "final_member_counts" DF
final_member_pivot = final_member_counts.pivot(columns='is_member',
                                               index='ab_test_group',
                                               values='first_name')\
                                               .reset_index()
# print(final_member_pivot)
# print('\n')

#Creating a new column for our pivoted frequency table that totals number of Members vs. Non-members
final_member_pivot['Total'] = final_member_pivot['Member'] + final_member_pivot['Not Member']
# print(final_member_pivot)
# print('\n')


#Creating a new column for our pivoted frequency table that calculates the percentages of Members vs. Not Members
final_member_pivot['Percent Purchase'] = final_member_pivot.Member / final_member_pivot['Total']
print(final_member_pivot)
print('\n')


#----------------------------
#----------------------------

### RUNNING A HYPOTHESIS TEST TO MEASURE SIGNIFICANCE BETWEEN BOTH GROUPS ###

#Since we're comparing statistical significance between two cat variables with multiple sub-variables, we should use a chi-squared test just as before!

#Creating the contingency table -- ***NOTE: We're running the test with Group A first
contingency3 = [[200,2304], [250,2250]]

#Running a chi-squared test
chi2_contingency(contingency3)

print('The results of our chi-squared test DID in fact reveal statistically significant difference between GroupA and GroupB, as shown below:\
\n' + str(chi2_contingency(contingency3)))
print('\n------------------------------\n')


#----------------------------
#----------------------------

### VISUALIZING OUR DATA BY USING BARCHARTS USING MATPLOTLIB (You can also use Seaborn!) ###

#Creating a barchart for the percentage of visitors who applied
ax = plt.subplot()
plt.bar(range(len(app_pivot)), app_pivot['Percent with Application'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.title('Percentage of Visitors who Applied for Membership')
plt.show()
plt.savefig('percent_visitors_apply.png')


#Creating a barchart for the percentage of applicants who purchased membership
ax = plt.subplot()
plt.bar(range(len(member_pivot)), member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(member_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
plt.title('Percentage of Applicants who Purchased Membership')
plt.show()
plt.savefig('percent_applicants_purchase.png')


#Creating a barchart for the percentage of visitors who purchased membership
ax = plt.subplot()
plt.bar(range(len(final_member_pivot)), final_member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(final_member_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.title('Percentage of Total Visitors who Purchased Membership')
plt.show()
plt.savefig('percent_visitors_purchase.png')