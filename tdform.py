#################-timedelta FORMATTER-#################
def timedeltaformatter(duration):
  days, seconds, microseconds = duration.days, duration.seconds, duration.microseconds
  hours = days * 24 + seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds += (microseconds)/ 1000000
  tiempo =[days,hours,minutes,seconds]
  return tiempo