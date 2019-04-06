import requests
import bs4
# Получение погоды
def get_weather(city: str = "москва") -> list:
    request = requests.get("https://sinoptik.com.ru/погода-" + city)
    b = bs4.BeautifulSoup(request.text, "html.parser")
        
    p3 = b.select('.temperature .p3')
    weather1 = p3[0].getText()
    p4 = b.select('.temperature .p4')
    weather2 = p4[0].getText()
    p5 = b.select('.temperature .p5')
    weather3 = p5[0].getText()
    p6 = b.select('.temperature .p6')
    weather4 = p6[0].getText()
    result = ''
        
    temp = b.select('.rSide .description')
    weather = temp[0].getText()
    result = result + weather.strip()
    result = result + ('\nУтром :' + weather1 + ' ' + weather2) + '\n'
    result = result + ('Днём :' + weather3 + ' ' + weather4) + '\n'
        
    return result