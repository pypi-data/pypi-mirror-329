from src.yelllovkitten.TimeData import TimeData, timedata


def color(text: str,color: str=None,color_light: bool=True):
    """
    Changes the text color in console.
    This function should be added to yelllovkitten.text.out() (or text.info(), text.warn(), text.error()) or print() for output.
    :param text: Text.
    :param color: color of text.
    :param color_light: If True color is light, else dark.
    :return: Modified text.
    """
    if not color_light:
        if color == 'red':
            command = '31m'
        elif color == 'green':
            command = '32m'
        elif color == 'yellow' or color == 'yelllov':
            command = '33m'
        elif color == 'blue':
            command = '34m'
        elif color == 'magenta':
            command = '35m'
        elif color == 'cyan':
            command = '36m'
        elif color == 'white':
            command = '37m'
        elif color == 'black':
            command = '30m'
        else:
            return text
    else:
        if color == 'red':
            command = '91m'
        elif color == 'green':
            command = '92m'
        elif color == 'yellow' or color == 'yelllov':
            command = '93m'
        elif color == 'blue':
            command = '94m'
        elif color == 'magenta':
            command = '95m'
        elif color == 'cyan':
            command = '96m'
        elif color == 'white':
            command = '97m'
        elif color == 'black':
            command = '90m'
        else:
            return text
    return f'\033[{command}{text}\033[m'

def font(text: str,font: str=None):
    """
    Changes the text font in console.
    This function should be added to yelllovkitten.text.out() (or text.info(), text.warn(), text.error()) or print() for output.
    :param text: Text.
    :param font: Font, example: bold, italic, underline or reverse.
    :return: Modified text.
    """
    if font == None:
        return text
    elif font == 'bold':
        command = '1m'
    elif font == 'italic':
        command = '3m'
    elif font == 'underline':
        command = '4m'
    elif font == 'reverse':
        command = '7m'
    else:
        return text

    return f'\033[{command}{text}\033[m'

def background(text: str,color: str=None,color_light: bool=True):
    """
    Changes the background color in console.
    This function should be added to yelllovkitten.text.out() (or text.info(), text.warn(), text.error()) or print() for output.
    :param text: Text.
    :param color: Color of background.
    :param color_light: If True color is light, else dark.
    :return: Modified text.
    """
    if not color_light:
        if color == 'red':
            command = '41m'
        elif color == 'green':
            command = '42m'
        elif color == 'yellow' or color == 'yelllov':
            command = '43m'
        elif color == 'blue':
            command = '44m'
        elif color == 'magenta':
            command = '45m'
        elif color == 'cyan':
            command = '46m'
        elif color == 'white':
            command = '47m'
        elif color == 'black':
            command = '40m'
        else:
            return text
    else:
        if color == 'red':
            command = '101m'
        elif color == 'green':
            command = '102m'
        elif color == 'yellow' or color == 'yelllov':
            command = '103m'
        elif color == 'blue':
            command = '104m'
        elif color == 'magenta':
            command = '105m'
        elif color == 'cyan':
            command = '106m'
        elif color == 'white':
            command = '107m'
        elif color == 'black':
            command = '100m'
        else:
            return text
    return f'\033[{command}{text}\033[m'

def info(text_: str, settings: TimeData=None, utc: bool=True):
    """
    Outputs the green text to the console.
    :param text_: Text.
    :param settings: TimeData.
    :param utc: Time, True if UTC, else local data and time.
    :return: None.
    """
    return out(font(color(str(text_),'green'),'bold'), settings=settings,return_time_info=True,utc=utc)
def warn(text_: str, settings: TimeData=None, utc: bool=True):
    """
    Outputs the yellow(yelllov) text to the console.
    :param text_: Text.
    :param settings: TimeData.
    :param utc: Time, True if UTC, else local data and time.
    :return: None.
    """
    return out(font(color(str(text_),'yellow'),'bold'), settings=settings,return_time_info=True,utc=utc)
def error(text_: str, settings: TimeData=None, utc: bool=True):
    """
    Outputs the red text to the console.
    :param text_: Text.
    :param settings: TimeData.
    :param utc: Time, True if UTC, else local data and time.
    :return: None.
    """
    return out(font(color(str(text_),'red'),'bold'), settings=settings,return_time_info=True,utc=utc)


def out(text_, settings: TimeData=None, utc: bool=True, return_time_info: bool=True, only_return: bool=False,out_time: bool=True):
    """
    Outputs the text to the console.
    :param text_: Text.
    :param settings: TimeData.
    :param utc: Time, True if UTC, else local data and time.
    :param return_time_info: IF True return time + text, else return only text.
    :param only_return: If True the text will not be output to the console.
    :param out_time: If True outputs the text to the console with time, else only text.
    :return: If return_time_info is False return text, else time + text.
    """
    if settings is not None:
        textout = timedata(settings) + str(text_)
        time_now = timedata(settings)
    else:
        from datetime import datetime, timezone
        if utc: time_now = str(datetime.now(timezone.utc))[:19]
        else: time_now = str(datetime.now())[:19]
        if out_time:
            textout = '\n' + time_now + ' | ' + str(text_)
        else:
            textout = '\n' + str(text_)
    if not only_return:
        print(textout,end='')
    if return_time_info:
        return time_now + ' | ' + str(text_)
    else:
        return text

def text(text_: str, color_text: str=None, color_text_light: bool=True,color_background: str=None, color_background_light: bool=True, font_text: str=None):
    """
    Modifies the text to output to the console.
    This function should be added to yelllovkitten.text.out() (or text.info(), text.warn(), text.error()) or print() for output.
    :param text_: Text.
    :param color_text: Color of text.
    :param color_text_light: True if you need light color of text, else dark color of text.
    :param color_background: Color of background.
    :param color_background_light: True if you need light color of background, else False.
    :param font_text: Font, example: bold, italic, underline or reverse.
    :return: Modified text.
    """
    return color(background(font(text_,font_text),color_background,color_background_light),color_text,color_text_light)