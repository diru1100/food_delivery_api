from datetime import datetime as dt


def preprocess_time(time):
    # Formats given raw input time into standard format of %H:%M:%S
    try:
        in_time = dt.strptime(time, "%I:%M %p")
    except:
        in_time = dt.strptime(time, "%I %p")
    out_time = dt.strftime(in_time, "%H:%M:%S")
    return dt.strptime(out_time, "%H:%M:%S").time()


def preprocess_datetime(input_datetime):
    # Formats given raw input datetime into UTC format datetime object
    split_datetime = input_datetime.split()
    input_date = split_datetime[0]
    input_time = split_datetime[1]+" "+split_datetime[2]
    return dt.strptime(input_date+" "+str(preprocess_time(input_time)), "%m/%d/%Y %H:%M:%S")


def preprocess_opening_hours(input_hours_string):
    '''
        Generates operating hours in a structured manner from raw input string
        Input string: "1:15 pm - 3:15 am "
    '''
    # get open and close times from given string
    input_hours_string = input_hours_string.split("-")
    open_time = input_hours_string[0]
    open_time = open_time.strip()
    close_time = input_hours_string[1]
    close_time = close_time.strip()

    # convert into datetime time objects
    open_time = preprocess_time(open_time)
    close_time = preprocess_time(close_time)

    operating_hours = dict()
    operating_hours['openTime'] = list()
    operating_hours['closeTime'] = list()
    operating_hours['openTime'].append(
        str(open_time))

    # creates another set of opening and close timings for edge case
    if close_time < open_time:
        operating_hours['openTime'].append(
            '00:00:00')
        operating_hours['closeTime'].append(
            '23:59:59')

    operating_hours['closeTime'].append(
        str(close_time))

    return operating_hours


def preprocess_range_of_days(input_days_range_string):
    '''
    Converts given string into range of days
    '''

    # to maintain a reference point
    list_of_days = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']

    # extract start and end days from given range string
    start_day, end_day = input_days_range_string.split("-")

    # removing extra space in strings
    start_day = start_day.strip()
    end_day = end_day.strip()
    # pro-process day names to follow a standard
    if start_day == 'Thu':
        start_day = 'Thurs'
    if end_day == 'Thu':
        end_day = 'Thurs'
    if start_day == 'Wed':
        start_day = 'Weds'
    if end_day == 'Wed':
        end_day = 'Weds'

    # extract day number from using our standard list
    start_day_pos = list_of_days.index(start_day)
    end_day_pos = list_of_days.index(end_day)

    # return range of days depending on start and end days given
    if start_day_pos <= end_day_pos:
        return list_of_days[start_day_pos:end_day_pos+1]
    return list_of_days[start_day_pos:] + list_of_days[:end_day_pos+1]


def preprocess_opening_hours_data(opening_hours_data):
    '''
        Converts given list of data into a structured list of opening hours
        in proper format.
        Input string : "Mon, Fri 2:30 pm - 8 pm / Tues 11 am - 2 pm / Weds 1:15 pm - 3:15 am
         / Thurs 10 am - 3:15 am / Sat 5 am - 11:30 am / Sun 10:45 am - 5 pm",
    '''
    day_wise_opening_hours = list()
    # extract opening hours time which is at the end of any split data
    opening_hours_string = ' '.join(
        opening_hours_data.strip().split(' ')[-5:])

    # transfrom opening hours into standard format
    opening_hours = preprocess_opening_hours(
        opening_hours_string)

    # extract days which have the same opening hours
    only_days_string = opening_hours_data.replace(
        opening_hours_string, '')

    multiple_days_with_same_time = list()

    # including days given in different formats like
    # 'Mon, Tue-Sat'
    temp_list_of_days = only_days_string.split(",")

    for day in temp_list_of_days:
        if '-' in day:
            multiple_days_with_same_time += preprocess_range_of_days(
                day)
        else:
            multiple_days_with_same_time.append(day)

    # Structuring into proper format to load easily
    for day in multiple_days_with_same_time:
        map_day_to_hours = list()
        map_day_to_hours.append(day)
        map_day_to_hours.append(opening_hours)
        day_wise_opening_hours.append(map_day_to_hours)

    return day_wise_opening_hours


if __name__ == '__main__':

    sample_opening_hours_data = 'Mon, Fri 2:30 pm - 8 pm / Tues 11 am - 2 pm / Weds 1:15 pm - 3:15 am / Thurs 10 am - 3:15 am / Sat 5 am - 11:30 am / Sun 10:45 am - 5 pm'

    split_sample_opening_hours_data = sample_opening_hours_data.split('/')

    print(split_sample_opening_hours_data, '\n')
    sample_list = list()
    for data in split_sample_opening_hours_data:
        # sample_list += preprocess_opening_hours_data(data)
        print(preprocess_opening_hours_data(data))

    # print(sample_list)

    sample_input_datetime = '02/10/2020 04:09 AM'
    print(preprocess_datetime(sample_input_datetime))
