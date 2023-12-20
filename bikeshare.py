import time
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
#import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = {'all', 'january', 'february', 'march', 'april', 'may', 'june'}
DAY_DATA  = {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        c_in = input("Enter city name: (c)hicago, (n)ew york city, (w)ashington): ").lower()
        city = next((key for key in CITY_DATA.keys() if key.startswith(c_in)), None)
        if city:
            break
        else:
            print("Invalid entry. Enter a city name!")
            
    # get user input for month (all, january, february, ... , june)
    while True:
        m_in = input("Enter month: ((j)anuary, (f)ebruary, (m)arch, (a)pril, (ma)y, (j)une) or (all): ").lower()
        month = next((m for m in MONTH_DATA if m.startswith(m_in)), None)
        if month:
            break
        else:
            print("Invalid entry. Enter a month or (all)!")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        d_in = input("Enter day of week: (mo)nday, (tu)esday, (we)dnesday, (th)ursday, (fr)iday, (sa)turday, (su)nday), or (all): ").lower()
        day = next((d for d in DAY_DATA if d.startswith(d_in)), None)
        if day:
            break
        else:
            print("Invalid day of week. Enter a day or (all)!")      
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()    #weekday_name incorrect old pandas!
    
    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]
    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #Import calendar to convert the integer to the value 
    print("Most popular/common month:", calendar.month_name[int(df["month"].mode()[0])] )
       
    # display the most common day of week
    print("Most popular/common day of week:", df['day_of_week'].mode()[0])

    # display the most common start hour  
    print("Most popular/common start hour:", pd.to_datetime(df["Start Time"]).dt.hour.mode()[0])
    ###
 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station:", df["Start Station"].mode()[0])

    # display most commonly used end station
    print("Most commonly used end station:", df["End Station"].mode()[0])

    # display most frequent combination of start station and end station trip
    df["Start End Station"] = df["Start Station"] + " <and> " + df["End Station"]
    print("Most frequent combination of start station and end station trip between:", df["Start End Station"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time for selected bike data in seconds:", df["Trip Duration"].sum())

    # display mean travel time
    print("Mean travel time for selected bike data in seconds:", df["Trip Duration"].mean())

    ###
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types: ", df["User Type"].value_counts())
    
    # Display counts of gender
    if "Gender" in df.columns:
        print("Counts of gender: ", df["Gender"].value_counts())
    else:
        print("Counts of gender: not available in washington")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        print("Earliest year of birth: ", int(df["Birth Year"].min()))
        print("Most recent year of birth: ", int(df["Birth Year"].max()))
        print("Most common year of birth: ", int(df["Birth Year"].mode()[0]))
        print("Missing birth year values:", df["Birth Year"].isna().sum())   
    else:
        print("Birth data not available in washington") 
        
    ##
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Display 5 lines of raw data upon request """
    
    showdata = input('\nDo you want to see 5 lines of raw data? (yes) or (no)\n')
    count = 0
    while showdata.lower() == "yes":
        print(df.iloc[count:count + 5])
        count += 5
        showdata = input("\nDo you want to see the next 5 lines of raw data? (yes) or (no)\n")
    print('-'*40)

def matplot(df):
    """Plot a statistic of the bike usage accross the year in the selected city. Mainly the mean trip duration across the year per month."""
    
    mean_month = df.groupby('month')['Trip Duration'].mean()
    plt.figure(figsize=(15, 10))
    #plt.plot(mean_month.index, mean_month.values, marker='x')
    plt.bar(mean_month.index, mean_month.values, color='black')
    plt.title("Average bike trip duration per month in the Year (in seconds)")
    plt.ylabel("Average bike trip duration in seconds")
    plt.xlabel("Months")
    plt.xticks(mean_month.index, [calendar.month_name[i] for i in mean_month.index], rotation=0)
    plt.grid(False)
    plt.show()
    print('-'*40)
    
## BEGIN MAIN ##  
def main():
    print('\n')
    print('-'*40)
    while True:
        city, month, day = get_filters()
        #city = "washington"
        #month = "june"
        #day = "tuesday"
        print("\nThe input values are city: {}, month: {}, day: {}\n".format(city, month, day))     # PRINT VALUES
        df = load_data(city, month, day)
    
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print(df.head(10))
        print(df.describe())
        raw_data(df)            # ask input to raw data and display 5 lines  
        
        showplot = input('\nDo you want to see a plot of the avareage monthly usage time of the bikes across all data in your selected city? (yes) or (no)\n')
        if showplot.lower() == "yes":
            df = load_data(city, "all", "all")   # load yearly data for all months accross the city
            matplot(df)       
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
