import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ""
    month = None
    day = None
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = str(input('\nWould you like to see data for Chicago, New York, or Washington? \n'))
        if city.lower() in CITY_DATA.keys():
            break
        else:
            print('{} city is not in our database, please try again'.format(city))

    while True:
        time_str = str(input('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. \n'))
        if time_str.lower() in ['month','day','both','none']:
            break
        else:
            print('type the correct time key')
    # get user input for month (all, january, february, ... , june)
    if time_str in ['month','both']:
        while True:
            month = str(input('\nWhich month? January, February, March, April, May, or June? type "all" for all months. \n'))
            if month.lower() in ['january','february','march','april','may','june','all']:
                break
            else:
                print('type the correct month')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    if time_str in ['day','both']:
        while True:
            day = str(input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday? type all for all days. \n'))
            if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']:
                break
            else:
                print('type the correct day name')



    print('-'*40)
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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all' and month:
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all' and day:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Comon Month:', df['month'].mode()[0])

    # display the most common day of week
    print('The Most Comon Day of Week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('The Most Comon Start Hour:', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station:', df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    df['Start_End_Station'] = df['Start Station'] + ' **** ' + df['End Station']
    print('The most frequent combination of start station and end station trip:',df['Start_End_Station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    #display total travel time
    total_travel_time = time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].sum()))
    print('Total travel time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = time.strftime("%H:%M:%S", time.gmtime(df['Trip Duration'].mean()))
    print('Mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types: ', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of gender: ', df['Gender'].value_counts())
    else:
        print('No Gender Data to share !!!!!')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest Year of Birth', df['Birth Year'].min())
        print('Most Recent Year of Birth',  df['Birth Year'].max())
        print('Most Comon Year of Birth', df['Birth Year'].mode()[0])
    else:
        print('No Birth Year Data to share !!!!!')

    # Display user individual trip data
    i = 0
    while True:
        ch = str(input('\nWould you like to see individual trip data?: enter yes or no.\n'))
        if ch.lower() == 'yes':
            print(df[i:i+5])
            i += 5
        elif ch.lower() == 'no':
            break
        else:
            print('put the correct answer')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
