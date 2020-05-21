from dateutil import tz


def convert_to_utc(theDate):

  # METHOD 2: Auto-detect zones:
  utc_zone = tz.tzutc()
  local_zone = tz.tzlocal()

  # Tell the datetime object that it's in local time zone since
  # datetime objects are 'naive' by default
  local_time = theDate.replace(tzinfo=local_zone)
  # Convert time to UTC
  utc_time = local_time.astimezone(utc_zone)
  return utc_time