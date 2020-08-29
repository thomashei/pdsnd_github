import time
import pandas as pd
import numpy as np
import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def data_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Users can only choose data from Chicago, NY City and Washington
    while True:
        city = input('Would you like to see data of Chicago, New Youk City or Washington?\n')
        if city.title() in ['Chicago', 'New York City', 'Washington']:
            break
        else:
            print("\nYou are only able to choose from 'Chicago', 'New York City' or 'Washington'!")
    
    # Users are asked if they want to filter data by month and day of week
    while True:
        d_filter = input('Would you like to filter by month and day? Please enter yes or no.\n')
        
        if d_filter not in ['yes', 'no']:
            print('\nPlease answer yes or no.\n')
            continue
        
        # Users enter month and day of week to see relevant data, but only available for January to June
        if d_filter == 'yes':
            while True:
                month = input("Which month? e.g. January (you can enter 'all' to check the whole year) \n")
                if month in ['January', 'February', 'March', 'April', 'May', 'June', 'all']:
                    break
                elif month in ['July', 'August', 'September', 'October', 'November', 'December']:
                    print('\nSorry, we only provide data from January to June.')
                else:
                    print("\nPlease input a vaild month.")
          
            while True:
                day = input("Which day? e.g. Monday? (you can enter 'all' to check the whole week) \n")
                if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all']:
                    break
                else:
                    print("\nPlease input a valid day of week.")
        break
    
    if d_filter == 'no':
            month = 'all'
            day = 'all'
    
    print('-'*40)

    df = pd.read_csv(CITY_DATA[city.lower()])
    df.rename(columns={'Unnamed: 0':'Rent ID'}, inplace=True )
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        df = df[df['Month'] == month]
    
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month (small dialogs if users have chosen specific month and day)
    popular_month = df['Month'].value_counts().idxmax()
    popular_month_count = df['Month'].value_counts().max()
    a = df['Month'].values
    r = (a[0] == a).all()
    if r == True:
        print('The most common month: {} (Of course! You chose {}!) Count: {}'.format(popular_month, popular_month, popular_month_count),'\n')
    elif r == False:
        print('The most common month: {}  Count: {}'.format(popular_month, popular_month_count), '\n')
    
    # display the most common day of week
    popular_day = df['Day of Week'].value_counts().idxmax()
    popular_day_count = df['Day of Week'].value_counts().max()
    b = df['Day of Week'].values
    t = (b[0] == b).all()
    if t == True:
        print('The most common day of week: {} (No doubt because you chose {}!) Count: {}'.format(popular_day, popular_day, popular_day_count),'\n')
    elif t == False:
        print('The most common day of week: {}  Count: {}'.format(popular_day, popular_day_count),'\n')
    
    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['Start Hour'].value_counts().idxmax()
    popular_start_count = df['Start Hour'].value_counts().max()
    print('The most common start hour: {}  Count: {}'.format(popular_start_hour, popular_start_count),'\n')
    
    # display the most common end hour
    df['End Hour'] = df['End Time'].dt.hour
    popular_end_hour = df['End Hour'].value_counts().idxmax()
    popular_end_count = df['End Hour'].value_counts().max()
    print('The most common end hour: {}  Count: {}'.format(popular_end_hour, popular_end_count),'\n')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display the top 3 used start station
    popular_start_stations = df.groupby(['Start Station']).size().nlargest(3).rename_axis(index=' ')
    print('The top 3 start stations:', popular_start_stations, '\n')
    
    # display the top 3 used end station
    popular_end_stations = df.groupby(['End Station']).size().nlargest(3).rename_axis(index=' ')
    print('The top 3 end stations:', popular_end_stations, '\n')
    
    # display most frequent combination of start station and end station trip
    popular_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    combination_count = df.groupby(['Start Station', 'End Station']).size().max()
    print('The most popular combination of start and end station: {}  Count: {}'.format(popular_combination, combination_count), '\n')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time and convert it to minutes and seconds
    total_travel_time = df['Trip Duration'].sum()
    total_mins = (int(total_travel_time) // 60)
    total_secs = (int(total_travel_time) % 60)
    print('The total duration of travel: {} secs ({} mins and {} secs)'.format(int(total_travel_time), total_mins, total_secs), '\n')
    
    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('The average travel time per person: ', int(average_travel_time), 'secs \n')
    
    # display total and average travel time by gender
    if 'Gender' in df:
        g_sum_duration = df.groupby(['Gender'])['Trip Duration'].sum()
        g_avg_duration = df.groupby(['Gender'])['Trip Duration'].mean()
        m_duration = pd.DataFrame([[g_sum_duration['Male'],g_avg_duration['Male']]], index=['Male'], columns=['Total', 'Average'])
        f_duration = pd.DataFrame([[g_sum_duration['Female'],g_avg_duration['Female']]], index=['Female'], columns=['Total', 'Average'])
        print('Total and average travel duration by gender:')
        print(f_duration)
        print(m_duration)
    else:
        pass
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    type_count = df.groupby(['User Type']).size().rename_axis(index=' ')
    print('Count of user type:', type_count, '\n')
    
    # Display counts of gender
    if 'Gender' in df:
        gender_count = df.groupby(['Gender']).size().rename_axis(index=' ')
        print('Count of gender:',gender_count, '\n')
    else:
        print('No gender information recorded for Washington')
      
    # display count of birth yaer with 10 years as a interval
    if 'Birth Year' in df:
        y_bins = np.arange(1890, 2021, 10)
        y_labels = ['1890 - 1899', '1900 - 1909', '1910 - 1919', '1920 - 1929', '1930 - 1939', 
                  '1940 - 1949', '1950 - 1959', '1960 - 1969', '1970 - 1979', '1980 - 1989', 
                  '1990 - 1999', '2000 - 2009', '2010 - 2019']
        catagory_year = pd.cut(df['Birth Year'], bins=y_bins, labels=y_labels) 
        count_range = df.groupby(catagory_year).size()
        print("Users'birth year count in ranges:\n", count_range, 'Total:', count_range.sum())
    else:
        pass
    
    # Display most common, earliest, most recent year of birth
    if 'Birth Year' in df:
        common_birth_year = df['Birth Year'].value_counts().idxmax().astype(np.int64)
        oldest_birth = int(df['Birth Year'].min())
        youngest_birth = int(df['Birth Year'].max())
        print('\nThe most common year of birth: ', common_birth_year, '\n')
        print('The oldest and youngest year of birth: {}, {}'.format(oldest_birth, youngest_birth))
    else:
        print('No birth year information recorded for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw(df):
    # Ask if users want to see raw data. If yes, display 5 sets of data
    detail = input('\nWould you like to see the raw data? Please enter yes or no.\n')
    if detail.lower() == 'yes':
        raw_df = df.filter(['Gender', 'User Type', 'Birth Year', 'Rent ID', 'Start Station', 'Start Time', 'End Station', 'End Time', 'Trip Duration'], axis=1)
        raw_dict = raw_df.to_dict(orient='index')
        for i in sorted(raw_dict)[0:6]:
            pprint.pprint(raw_dict[i])
        
        # Ask if users want to see more raw data. Keep display 5 sets of data if answer yes
        start_num = 6
        while True:
            c = input('Would you like to see more data? Enter yes or no. \n')
            if c == 'no':
                break
            elif c == 'yes': 
                for i in sorted(raw_dict)[start_num:start_num+6]:
                    pprint.pprint(raw_dict[i])
                start_num += 6
                continue
            else:
                continue
            
    elif detail.lower() == 'no':
        pass
            
    else:
        print("\nPlease enter 'yes' or 'no'")
        return(raw(df)) 
    
        
def main():
    while True:
        df = data_filters()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
               
main()

    
    
    