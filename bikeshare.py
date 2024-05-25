import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'newyork': 'new_york_city.csv',
             'washington': 'washington.csv'}

MAPPING_WEEKDAY = {
    "1": "Sunday",
    "2": "Monday",
    "3": "Tuesday",
    "4": "Wednesday",
    "5": "Thursday",
    "6": "Friday",
    "7": "Saturday",
}

MAPPING_MONTH = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6
}

filter_month_day = {
    'month': "No",
    'day': "No",
}


def format_input(input):
    return input.lower().strip().replace(" ", "") if type(input == str) else None


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city, month, day = None, None, None

    print('Hello! Let\'s explore some US bikeshare data!')

    # Give the user choose what city user want to see data
    city = format_input(input("Would you like to see data for Chicago, New York, or Washington?\n"))
    while (city not in ('chicago', 'newyork', 'washington')):
        print('You should choose 1 of 3 city: Chicago, New York, or Washington')
        city = format_input(input("Would you like to see data for Chicago, New York, or Washington?\n"))

    # Give the user choose filter by month, day, both or not at all
    filter_data = format_input(input(
        "Would you like to filter the data by \"month\", \"day\", \"both\" or not at all? Type \"no\" for no time filter\n"))
    while (filter_data not in ('month', 'day', 'both', 'no')):
        print('You should choose 1 of 4 opstions: \"month\", \"day\", \"both\" or \"no\"')
        filter_data = format_input(input(
            "Would you like to filter the data by \"month\", \"day\", \"both\" or not at all? Type \"no\" for no time filter\n"))

    if filter_data in ("month", "both"):
        month = format_input(input("Which month - January, February, March, April, May, or June?\n"))
        while (month not in ("january", "february", "march", "april", "may", "june")):
            print('You should choose: January, February, March, April, May, or June')
            month = format_input(input("Which month - January, February, March, April, May, or June?\n"))

    # If user choose day or both, ask user what day user want to see data
    if filter_data in ("day", "both"):
        day = format_input(input(
            "Which day - Please type an integer as: 1=Sunday 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday ?\n"))
        while (day not in ("1", "2", "3", "4", "5", "6", "7")):
            print('You should choose: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday as an integer')
            day = format_input(
                input(
                    "Which day - Please type an integer as: 1=Sunday 2=Monday, 3=Tuesday, 4=Wednesday, 5=Thursday, 6=Friday, 7=Saturday ?\n"))

    print('-' * 60)
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

    # Read csv
    df = pd.read_csv(CITY_DATA.get(city))

    # Create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # filter month, day (if it has)
    if month:
        df = df[df['Month'] == MAPPING_MONTH.get(month)]
        filter_month_day['month'] = month.capitalize()
    else:
        filter_month_day['month'] = "No"

    if day:
        df = df[df['Weekday'] == MAPPING_WEEKDAY.get(day)]
        filter_month_day['day'] = MAPPING_WEEKDAY.get(day)
    else:
        filter_month_day['day'] = "No"

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['Month'].mode()[0]
    count_common_month = df['Month'][df['Month'] == common_month].count()
    print(f"\nMost common month: {common_month}, "
          f"Count: {count_common_month}, "
          f"Filter: {filter_month_day}")

    # Display the most common day of week
    common_weekday = df['Weekday'].mode()[0]
    count_common_weekday = df['Weekday'][df['Weekday'] == common_weekday].count()
    print(f"\nMost common day of week: {common_weekday}, "
          f"Count: {count_common_weekday}, "
          f"Filter: {filter_month_day}")

    # Display the most common start hour
    common_hour = df['Hour'].mode()[0]
    count_common_hour = df['Hour'][df['Hour'] == common_hour].count()
    print(f"\nMost common start hour: {common_hour}, "
          f"Count: {count_common_hour}, "
          f"Filter: {filter_month_day}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    count_common_start_station = df['Start Station'][df['Start Station'] == common_start_station].count()
    print(
        f"\nMost common Start Station: {common_start_station}, "
        f"Count: {count_common_start_station}, "
        f"Filter: {filter_month_day}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    count_common_end_station = df['End Station'][df['End Station'] == common_end_station].count()
    print(
        f"\nMost common Start Station: {common_end_station}, "
        f"Count: {count_common_end_station}, "
        f"Filter: {filter_month_day}")

    # Display most frequent combination of start station and end station trip
    common_combine_station_df = df[['Start Station', 'End Station']].apply(tuple, axis=1).mode()
    common_combine_station = common_combine_station_df[0]
    count_common_combine_station = df['Start Station'][(df['Start Station'] == common_combine_station[0])
                                                       & (df['End Station'] == common_combine_station[1])].count()
    print(
        f"\nMost frequent combination of Start Station: \"{common_combine_station[0]}\" "
        f"and End Station: \"{common_combine_station[1]}\", "
        f"Count: {count_common_combine_station}, "
        f"Filter: {filter_month_day}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    count_travel_time = df['Trip Duration'].count()
    print(
        f"\nTotal travel time: \"{total_travel_time}\" "
        f"Count: {count_travel_time}, "
        f"Filter: {filter_month_day}")

    # Display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print(
        f"\nAverage travel time: \"{avg_travel_time}\" "
        f"Count: {count_travel_time}, "
        f"Filter: {filter_month_day}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"\nUser Type: {str(user_types.to_dict())[1:-1]}, "
          f"Filter: {filter_month_day}")

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nGender: {str(gender.to_dict())[1:-1]}, "
              f"Filter: {filter_month_day}")
    except Exception:
        print("There is no data of Gender for city: {}."
              .format(city.capitalize()))

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        print(f"\nEarliest year of birth: {earliest_birth_year}")

        most_recent_birth_year = int(df['Birth Year'].max())
        print(f"\nMost recent year of birth: {most_recent_birth_year}")

        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"\nMost common year of birth: {most_common_birth_year}")
    except Exception:
        print("There is no data of year of birth for city: {}."
              .format(city.capitalize()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 60)


def view_raw_data(df):
    """ Display raw data in csv"""
    records_per_time = 5
    count_view = 0

    view_data = format_input(input("Would you like to view next 5 records raw data? Enter yes or no.\n"))
    while view_data == "yes":
        print(df[count_view*records_per_time:(count_view + 1)*records_per_time].to_string())
        view_data = format_input(input("Would you like to view next 5 records raw data? Enter yes or no.\n"))
        count_view += 1


def main():
    while True:
        city, month, day = get_filters()
        print(f'city: {city}')
        print(f'month: {month}')
        print(f'day: {day}')
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        view_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
