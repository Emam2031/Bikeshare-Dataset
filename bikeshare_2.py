import time
import pandas as pd
import numpy as np
from termcolor import colored
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print(colored('Hello! Let\'s explore some US bikeshare data!','red'))
    while True:
        city=input('Would you like to see data from chicago , new york city or washington?  \n\n').lower()
        if city not in CITY_DATA:
            print('please choose a correct city name')
        else:
            print("You have seleted {} ".format(city))
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month=input('Please enter a month to filter on(From january to june),or type "all" for no filter  \n\n').lower()
        months = ['january','february','march','april','may','june']
        if month != 'all' and month not in months:
            print('please enter a full valid month name')
        else:
            print("You have seleted {} ".format(month))
            break
    while True:
        day=input('please enter a day of the week, or type "all" to display all the days: ').lower()
        days = ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']
        if day != 'all' and day not in days:
            print('please enter a full valid day name')
        else:
            print("You have seleted {} ".format(day))
            break    


    print('-'*40+"Loading"+'-'*40)
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
    df = pd.read_csv(CITY_DATA[city])


    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

 
    if month != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]



    if day != 'all':

        df = df[df['day_of_week'] == day.title()] # to match how the day is written in print(df.head)

    return df

def display_raw_data(df):
    """
    display the first 5 rows of data for the specified city and filters by month and day if applicable.
    """

    row_no = 0
    answer = input('would you like to display the first 5 rows of data? Please select (yes/no): ').lower()
    pd.set_option('display.max.columns',None)

    while True:
        if answer == 'no':
            break
        print(df[row_no:row_no+5])
        answer = input("would you like to dispaly the next 5 rows of data? Please select (yes/no): ").lower()
        row_no +=5

    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n\n')
    start_time = time.time()

    common_month =  df['month'].mode()[0] 
    print('Most common Month is : ', calendar.month_name[common_month])

    common_day =  df['day_of_week'].mode()[0] 
    print('Most common Day: ', common_day)

    df['hour']= df['Start Time'].dt.hour
    common_hour=df['hour'].mode()[0]
    print('Most Common Start Hour is: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time).__round__(2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\n\n Calculating The Most Popular Stations and Trip...\n\n')
    start_time = time.time()

    common_start=df['Start Station'].mode()[0]
    print('Most commonly Used Start Station is : ', common_start)

    common_end=df['End Station'].mode()[0]
    print('Most commonly Used End Station is : ', common_end)


    common_start_end = (df['Start Station']+'-'+df['End Station']).mode()[0]
    print('Most frequent combination of Start and End Stations are : ',common_start_end)


    print("\n\nThis took %s seconds." % (time.time() - start_time).__round__(2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time=df['Trip Duration'].sum()
    print('\nTotal Travel Time is : ', total_time, ' seconds , or' , total_time/3600, ' hours')


    avg_time=df['Trip Duration'].mean()
    print('Average Travel Time: ', avg_time.__round__(2), 'seconds, or' , (avg_time/3600).__round__(2), ' hours')

    print("\nThis took %s seconds." % (time.time() - start_time).__round__(2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n\n')
    start_time = time.time()

    print('counts of User Types: \n\n\n',df['User Type'].value_counts());


    if 'Gender' in df:
        print('\n Counts of gender: \n\n\n', df['Gender'].value_counts())


    if 'Birth Year' in df:
        earliest_byear=int(df['Birth Year'].min())
        print('\n Ealiest year of Birth: \n',earliest_byear)
        recent_byear=int(df['Birth Year'].max())
        print('\n Most recent year of Birth: \n',recent_byear)        
        common_byear=int(df['Birth Year'].mode()[0])
        print('\n Most Common year of Birth: \n',common_byear)


    print("\nThis took %s seconds." % (time.time() - start_time).__round__(2))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\n\nWould you like to restart? Enter yes or no.\n\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
