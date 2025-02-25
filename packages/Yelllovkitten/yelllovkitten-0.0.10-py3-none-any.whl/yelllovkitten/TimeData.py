class TimeData:
    def __init__(self, utc_edit_hours=0, time12=True, mdy=True, cdat=' | ', end='', data=True, sec=False):
        self.utc_edit_hours = utc_edit_hours
        self.time12 = time12
        self.mdy = mdy
        self.cdat = cdat
        self.end = end
        self.data = data
        self.sec = sec

def timedata(settings: TimeData=None, utc_edit_hours: int=0, time12: bool=True, mdy: bool=True, cdat: str=' | ', end: str='',data: bool=True,sec: bool=False):
    '''
    TimeData
    :param settings: class yelllovkitten.TimeData.TimeData
    :param utc_edit_hours: add or remove hours to utc
    :param time12: twelve-hour format
    :param mdy: date format MDY if True else YMD
    :param cdat: text between date and time
    :param end: the text at the end
    :param data: show data if True
    :param sec: show sec if True
    :return:
    '''
    if settings is not None:
        utc_edit_hours = settings.utc_edit_hours
        time12 = settings.time12
        mdy = settings.mdy
        cdat = settings.cdat
        end = settings.end
        data = settings.data
        sec = settings.sec
    import datetime
    time_now = datetime.datetime.now(datetime.timezone.utc)
    time_now = time_now + datetime.timedelta(hours=utc_edit_hours)
    return time_now.strftime(f'{f'{'%m-%d-%Y' if mdy else '%Y-%m-%d'}' if data else ''}{cdat}{'%I' if time12 else '%H'}:%M{':%S' if sec else ''}{'%p' if time12 else ''}{end}')