def add_time(start, duration, start_day_of_week=False):
    
    def hours2minutes(hours):
        minutes_per_hour = 60  
        minutes = hours * minutes_per_hour
        return minutes   
   
    def am_pm2hours(am_pm):
        if am_pm == 'AM':
            hours = 0
        elif am_pm == 'PM':
            # add up mid day
            hours = 12
        else:
            raise ValueError('Invalid time')
        return hours

    def hhmm2minutes(hhmm):
        """ convert time hh:mm format to minutes

        Args:
            hhmm (str): time hh:mm

        Returns:
            int: minutes
        """
        time_hour = int(hhmm.split(':')[0])
        time_minute = int(hhmm.split(':')[1])
        minutes = hours2minutes(time_hour) + time_minute
        return minutes
   
    def time2minutes(time):
        """ Convert time to minutes

        Args:
            time (string): HH:MM AM (or PM)

        Raises:
            ValueError: if time not in the correct format

        Returns:
            minutes (int): number of minutes from the provided time
        """
        hhmm = time.split(' ')[0]
        am_pm = time.split(' ')[1]
        minutes = hhmm2minutes(hhmm) + hours2minutes(am_pm2hours(am_pm))
                
        return minutes

    def days2hours(days):
        hours_per_day = 24
        hours = days * hours_per_day
        return hours

    def minutes2days(minutes):
        minutes_per_hour = 60
        hours_per_day = 24
        minutes_per_day = minutes_per_hour * hours_per_day
        # 24 [h/day] * 60 [min/h] = 1440 [min/day]
        days = minutes // minutes_per_day 
        return days

    def minutes2hhmm(minutes):
        """ convert minutes to time hh:mm format

        Args:
            int: minutes

        Returns:
            hhmm (str): time hh:mm
        """
        hours_mid_day = 12

        minutes_per_hour = 60
        hours_per_day = 24
        minutes_per_day = minutes_per_hour * hours_per_day
        # 24 [h/day] * 60 [min/h] = 1440 [min/day]
        

        if minutes > minutes_per_day:
            days = minutes2days(minutes)
            minutes -= days * minutes_per_day
        
        hours = minutes // minutes_per_hour
        time_minute = minutes % minutes_per_hour

        if (hours <= 23) and (hours > hours_mid_day):
            time_hour = hours - hours_mid_day
            am_pm = 'PM'
        elif (hours == hours_mid_day): # mid_day
            time_hour = hours_mid_day
            am_pm = 'PM'
        elif (hours > 0) and  (hours < hours_mid_day):
            time_hour = hours
            am_pm = 'AM'
        elif (hours == 0):  # midnight
            time_hour = hours_mid_day
            am_pm = 'AM'
        else:
            raise ValueError('hours must be between 0 and 23 inclusive')

        time = f'{time_hour}:{time_minute:02d} {am_pm}'

        return time
    
    def get_add_days_str(add_days):
        if add_days == 0:
            add_days_str = ''
        elif add_days == 1:
            add_days_str = ' (next day)'
        elif add_days > 1:
            add_days_str = f' ({add_days} days later)'
        else:
            raise ValueError('add_days not valid')
        
        return add_days_str
    
    def get_key_from_val(dct, search_val):
        return {v:k for k, v in dct.items()}[search_val]

    def get_end_day_of_week(start_day_of_week, add_days):
        dct_day_of_week = {
            "Sunday":    0,
            "Monday":    1,
            "Tuesday":   2,
            "Wednesday": 3,
            "Thursday":  4,
            "Friday":    5,
            "Saturday":  6
        }

        if start_day_of_week:
            start_day_of_week = start_day_of_week.title()
            start_day_of_week_id = dct_day_of_week[start_day_of_week]

            days_per_week = len(dct_day_of_week) # 7
            end_day_of_week_id = (start_day_of_week_id + add_days) % days_per_week

            end_day_of_week = get_key_from_val(dct_day_of_week, end_day_of_week_id)
            end_day_of_week = f', {end_day_of_week}'
        else:
            end_day_of_week = ''
        
        return end_day_of_week
    
    start_minutes = time2minutes(start)
    duration_minutes = hhmm2minutes(duration)
    end_minutes = start_minutes + duration_minutes

    end_hhmm = minutes2hhmm(end_minutes)
    
    add_days = minutes2days(end_minutes)
    add_days_str = get_add_days_str(add_days)
    
    end_day_of_week = get_end_day_of_week(start_day_of_week, add_days)
    
    new_time = end_hhmm + end_day_of_week + add_days_str

    return new_time