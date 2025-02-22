from  datetime import *

class TimeMachine:
    def __init__(self):
        self.today = date.today()
        self.time_parts = str(self.today).split('-')
        self.right_time = datetime.now()
        self.current_time = self.right_time

    def day(self):
        """This function extracts the day from the current
        date (stored in self.time_parts)and returns it as an integer."""
        the_day = int(self.time_parts[2])
        return the_day

    def month(self):
        """This function extracts the month from the current
         date (stored in self.time_parts)and returns it as an integer."""
        the_month = int(self.time_parts[1])
        return f"{the_month:02}"


    def year(self):
        """This function extracts the year from the current
        date (stored in self.time_parts)and returns it as an integer."""
        the_year = int(self.time_parts[0])
        return the_year

    def month_name(self):
        """This function extracts name of the month from the current
        date (stored in self.time_parts)and returns it as an integer."""
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        the_month = int(self.time_parts[1])
        return months[the_month - 1]

    def hours(self):
        """This function extracts hours from the current
        date (stored in self.time_parts)and returns it as an integer."""
        hour = self.current_time.strftime("%H")
        return hour

    def minutes(self):
        """This function extracts minutes from the current
        date (stored in self.time_parts)and returns it as an integer."""
        minute = self.current_time.strftime("%M")
        return minute

    def seconds(self):
        """This function extracts seconds from the current
        date (stored in self.time_parts)and returns it as an integer."""
        second = self.current_time.strftime("%S")
        return second

    def clock(self):
        """This function extracts time from the current
        date (stored in self.time_parts)and returns it as an integer."""
        time_delay = self.current_time.strftime("%H:%M:%S")
        return print(f"\r{time_delay}", end="", flush=True)