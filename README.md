# time-converter

  string_to_datetime.py :
    Converts a sting like date or time to a datetime object.
    
    For example,
      Mary will open her shop at 10am mondays and 11am tuesdays.
      
      will be converted to,
      
        {
          'possible_dates' : [datetime.datetime(2018, 4, 30, 10, 0, 0, 0), datetime.datetime(2018, 5, 1, 11, 0, 0, 0)],
          'text' : 'Mary will open her shop at 10am mondays and 11am tuesdays.'
        }
