import pandas as pd
from datetime import datetime

class FlightDetails:
    def __init__(self, carrierCode, flightDate, flightNum, origination, destination, status, lastUpdated, flightKey):
        self.carrierCode = carrierCode
        self.flightDate = flightDate
        self.flightNum = flightNum
        self.origination = origination
        self.destination = destination
        self.status = status
        self.lastUpdated = lastUpdated
        self.flightKey = flightKey

    def __repr__(self):
        return str(self.__dict__)

def getAllFlightsStatus(fileName):
    mydict = {}
    try:
        df = pd.read_excel(fileName, skiprows=7, header=0)
    except FileNotFoundError:
        print(f"Error: The file '{fileName}' was not found.")
        return []
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{fileName}' is empty.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

    for index, row in df.iterrows():
        if 'flightkey' not in row or pd.isna(row['flightkey']):
            print(f"Skipping row {index} due to missing or NaN 'flightkey'.")
            continue

        key = row['flightkey']

        required_cols = ['Carrier Code', 'flight_dt', 'flightnum', 'orig_arpt', 'dest_arpt', 'flightstatus', 'lastupdt']
        if not all(col in row and not pd.isna(row[col]) for col in required_cols):
            continue

        if key not in mydict:
            mydict[key] = FlightDetails(row['Carrier Code'], row['flight_dt'], row['flightnum'], row['orig_arpt'], row['dest_arpt'], row['flightstatus'], row['lastupdt'], row['flightkey'])
        else:
            try:
                date_time_str = row['flight_dt'] + " " + row['lastupdt'] + ":00"
                date_time_obj = datetime.strptime(date_time_str, '%m/%d/%y %H:%M:%S')

                prev_date_time_str = mydict[key].flightDate + " " + mydict[key].lastUpdated + ":00"
                prev_date_time_obj = datetime.strptime(prev_date_time_str, '%m/%d/%y %H:%M:%S')

                if date_time_obj > prev_date_time_obj:
                    mydict[key] = FlightDetails(row['Carrier Code'], row['flight_dt'], row['flightnum'], row['orig_arpt'], row['dest_arpt'], row['flightstatus'], row['lastupdt'], row['flightkey'])
            except ValueError as ve:
                print(f"Skipping row {index} due to date parsing error: {ve} with data: flight_dt='{row['flight_dt']}', lastupdt='{row['lastupdt']}'")
                continue

    return list(mydict.values())

display(getAllFlightsStatus("Data Engineer_Assessment_Data Set_Flight Leg.xlsx"))
