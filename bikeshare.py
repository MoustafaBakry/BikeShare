import time
import datetime
import pandas as pd
import numpy as np


def chk_lst(val, lst):  # CHICK IN LIST IF THE INPUT IN THE LIST ITEMS OR NOT
    flg = False

    for i in lst:

        if val == i:
            flg = True
            break
        else:
            flg = False
    if flg == False:
        print("Enter the value from the right choise ...!!")
    return flg


def df_filter(df_process_pass):  # FUNCTION TO CREATE NEW FILED IN DF AND STORE NONTH AND DAY FROM START TIME FIELD

    df_process_pass['Month Values'] = df_process_pass['Start Time'].apply(stip_month)
    df_process_pass['Day Values'] = df_process_pass['Start Time'].apply(stip_day)

    return df_process_pass


def stip_month(dt_string):  # CONVERT STRING IN START STATION AND END STATION TO DATETIME TO RETRIVE MONTH
    format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.datetime.strptime(dt_string, format)
    m_value = dt_object.month
    return m_value


def stip_day(dt_string):  # CONVERT STRING IN START STATION AND END STATION TO DATETIME TO RETRIVE DAY
    format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.datetime.strptime(dt_string, format)
    d_value = dt_object.strftime("%a")
    return d_value


def stip_hour(dt_string):  # CONVERT STRING IN START STATION AND END STATION TO DATETIME TO RETRIVE HOUR
    format = "%Y-%m-%d %H:%M:%S"
    dt_object = datetime.datetime.strptime(dt_string, format)
    h_value = dt_object.hour
    return h_value


def time_stats(df):

    global cond_filter,day,month
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Common Start Hour'] = df['Start Time'].apply(
        stip_hour)  # SPLITE THE HOUR FROM START TIME AND STORE IT IN 'COMMON START HOUR' FIELD

    # CONDITION TO KNOW THE TYPE OF FILTERING (MONTH , DAY , BOTH OR NONE FILTER APPLIED)
    if cond_filter.strip().lower() == 'none':
        # display the most common month
        print('Most common month is ', MONTH_LST[df['Month Values'].value_counts().idxmax() - 1])
        # display the most common day of week
        print('Most common day is ', df['Day Values'].value_counts().idxmax())
        # display the most common start hour
        print('Most common Start hour is ', df['Common Start Hour'].value_counts().idxmax())
    elif cond_filter.strip().lower() == 'month':
        # display the most common month
        # Already month known
        # display the most common day of week
        print('Most common day is ', df['Day Values'].value_counts().idxmax())
        # display the most common start hour

        print('Most common Start hour is ', df['Common Start Hour'].value_counts().idxmax())

    elif cond_filter.strip().lower() == 'day':
        # display the most common month
        print('Most common month is ', MONTH_LST[df['Month Values'].value_counts().idxmax() - 1])
        # display the most common day of week
        # Already day of the week known
        # display the most common start hour

        print('Most common Start hour is ', df['Common Start Hour'].value_counts().idxmax())

    else:
        print('We already known the day is {} and the month is {}'.format(day, MONTH_LST[month - 1]))
        print('Most common Start hour is ', df['Common Start Hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total trip duration by hours is ", "%.2f" % float(df['Trip Duration'].sum() / (60 * 60)))  # BY HOUR

    # display mean travel time

    print("\nThe average time of all trips by minutes is  ", "%.2f" % float(df['Trip Duration'].mean() / 60))  # BY MIN

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station is ', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station

    print('Most commonly used end station is ', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    df['Combine Station'] = df['Start Station'] + " " + "to" + " " + df[
        'End Station']  # CONCATUNATE START AND END STATION IN ONE FILED
    print('Most frequent combination of start station and end station trip is ',
          df['Combine Station'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    global city_value
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print(city_value[0])
    # CONDITION TO CHICK WHICH CITY WE ARE
    if city_value[0].capitalize() == 'Washington':
        print('This city did not collect data by gender ...!!')
        print("\nOur user type is : ", df['User Type'].unique())
        print("\nCounts :\n ", df['User Type'].value_counts())


    else:

        print("\nOur user type is : ", df['User Type'].unique())
        print("\nCounts :\n ", df['User Type'].value_counts())
        print('##' * 20)

        print("\nOur cat is : ", df['Gender'].unique())

        # Display counts of gender

        print("\nCounts :\n ", df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('\nYoungest born in :', int(df['Birth Year'].min()), '\t Oldest born in :',
              int(df['Birth Year'].max()))  # ,'\n\n Frequency is\n\n :',df_final['Birth Year'].value_counts())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


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
        city_value = input('Would you like to see data for Chicago , New york city or Washington ? >>   ')
        if chk_lst(city_value.strip().capitalize(), CITY_LST) == True:
            break

    city_filter = CITY_DATA[city_value.strip().capitalize()]

    while True:

        cond_filter = input('Would you like to filter the data by month , day , both ? Type "none" for no time filter ? >>  ')
        if chk_lst(cond_filter.strip().lower(), CHOISE_LST) == True:
            break

    if cond_filter.strip().lower() == "both":

        # get user input for month (all, january, february, ... , june)
        while True:

            month_inpt = input("Which month?\tJan , Feb , Mar , Apr , May or Jun >>  ")
            if chk_lst(month_inpt.strip().capitalize(), MONTH_LST) == True:
                break
        month_filter = MONTH_DATA[month_inpt.strip().capitalize()]

        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day_inpt = input("Which day? \t Sat , Sun, Mon, Tue, Wed, Thu or Fri>> ")
            if chk_lst(day_inpt.strip().capitalize(), WEEK_LST) == True:
                break

        month_filter = MONTH_DATA[month_inpt.strip().capitalize()]
        day = WEEK_DATA[day_inpt.strip().capitalize()]
        day_filter = WEEK_LST[day - 1]
        print('-' * 40)

    elif cond_filter.strip().lower() == "month":
        while True:

            month_inpt = input("Which month?\tJan , Feb , Mar , Apr , May or Jun >>  ")
            if chk_lst(month_inpt.strip().capitalize(), MONTH_LST) == True:
                break

        month_filter = MONTH_DATA[month_inpt.strip().capitalize()]
        day_filter = 'any'
        print('-' * 40)

    elif cond_filter.strip().lower() == "day":
        month_filter = 8

        while True:
            day_inpt = input("Which day? \t Sat , Sun, Mon, Tue, Wed, Thu or Fri>> ")
            if chk_lst(day_inpt.strip().capitalize(), WEEK_LST) == True:
                break

        day = WEEK_DATA[day_inpt.strip().capitalize()]
        day_filter = WEEK_LST[day - 1]
        print('-' * 40)

    else:  # cond_filter =="none" :
        month_filter = 8
        day_filter = 'any'
        print('-' * 40)
    return city_filter, month_filter, day_filter, cond_filter


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
    df = pd.read_csv(city)

    return df



def main():
    pd.options.mode.chained_assignment = None          
    
    global CITY_LST,CITY_DATA,MONTH_DATA,MONTH_LST,WEEK_DATA,WEEK_LST,CHOISE_LST,cond_filter,city_value,day,month
    CITY_LST = ['Chicago', 'New york city', 'Washington']  # CHICKING LIST OF THE CITYS

    CITY_DATA = {'Chicago': 'chicago.csv',
                 'New york city': 'new_york_city.csv',
                 'Washington': 'washington.csv'}

    MONTH_DATA = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6}

    MONTH_LST = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']  # CHICKING LIST OF THE MONTHS

    WEEK_DATA = {'Sat': 1, 'Sun': 2, 'Mon': 3, 'Tue': 4, 'Wed': 5, 'Thu': 6, 'Fri': 7}

    WEEK_LST = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']  # CHICKING LIST OF THE DAYS

    CHOISE_LST = ['month', 'day', 'both', 'none']  # CHICKING LIST OF THE FILTER TYPE



    while True:
        city, month, day, cond_filter = get_filters()
        df = load_data(city, month, day)
        city_value = city.split(".")
        df_process = df.copy()
        df_processed = df_filter(df_process)

        if cond_filter.strip().lower() == 'both':
            print('Processing City = ', city_value[0], '\t\tMonth = ', MONTH_LST[month - 1], ' Day = ', day)
            # df_process['Month Values'] = df_process['Start Time'].apply(stip_month)
            # df_process['Day Values'] = df_process['Start Time'].apply(stip_day)
            df_final = df_processed[(df_processed['Month Values'] == month) & (df_processed['Day Values'] == day)]
            # df_day_month.head(n=10)
            print('End ')

        elif cond_filter.strip().lower() == 'month':
            print('Processing City = ', city_value[0], '\t\tMonth = ', MONTH_LST[month - 1])
            # df_process['Month Values'] = df_process['Start Time'].apply(stip_month)
            df_final = df_processed[df_processed['Month Values'] == month]
            # df_month.head(n=10)
            print('End ')

        elif cond_filter.strip().lower() == 'day':
            print('Processing City = ', city_value[0], '\t\tDay = ', day)
            # df_process['Day Values'] = df_process['Start Time'].apply(stip_day)
            df_final = df_processed[df_processed['Day Values'] == day]
            # df_day.head(n=10)
            print('End ')

        else:
            print('Processing City = ', city_value[0], '\t\t\tNo filter')
            df_final = df_processed
            # df_none.head(n=10)
            print('End ')

        time_stats(df_final)
        station_stats(df_final)
        trip_duration_stats(df_final)
        user_stats(df_final)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

