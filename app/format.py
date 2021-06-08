from datetime import datetime as dt
# "transactionDate": "02/19/2019 04:20 AM"


def preprocess_time(time):
    try:
        in_time = dt.strptime(time, "%I:%M %p")
    except:
        in_time = dt.strptime(time, "%I %p")
    out_time = dt.strftime(in_time, "%H:%M:%S")
    return dt.strptime(out_time, "%H:%M:%S").time()


# "openingHours": "Mon, Fri 2:30 pm - 8 pm / Tues 11 am - 2 pm
#  / Weds 1:15 pm - 3:15 am / Thurs 10 am - 3:15 am / Sat 5 am - 11:30 am / Sun 10:45 am - 5 pm",
def preprocess_datetime(input_datetime):
    split_datetime = input_datetime.split()
    input_date = split_datetime[0]
    input_time = split_datetime[1]+" "+split_datetime[2]
    return dt.strptime(input_date+" "+str(preprocess_time(input_time)), "%m/%d/%Y %H:%M:%S")


a = preprocess_time("3 pm")
b = preprocess_time("5 pm")
print(str(a))
if a > b:
    print("a big")
else:
    print("b bigger")
print(type(preprocess_datetime("02/19/2019 04:20 AM")))
