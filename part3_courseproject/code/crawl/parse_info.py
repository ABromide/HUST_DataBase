import time
from bs4 import BeautifulSoup

def parse_info(date,depcity,arrcity,flights_direct,flights_transit,source):
    '''
    解析页面源代码，获得需要的信息并保存
    '''
    bs = BeautifulSoup(source, 'html.parser')
    divs_direct = bs.find_all('div', class_='search_box search_box_tag search_box_light Label_Flight')

    # 爬取直飞机票信息
    for div in divs_direct:
        #航空公司名称
        try:
            info = div.find('div', class_='logo-item flight_logo').find('strong')
            airlineName = info.get_text()
        except:
            airlineName = None
        #航班号
        try:
            info = div.find('div', class_='logo-item flight_logo').find_all('span')[2]
            flightNumber = info.string
        except:
            flightNumber = None
        #机型
        try:
            info = div.find('span', class_='direction_black_border low_text')
            craftTypeName = info.string
        except:
            craftTypeName = None
        #离开机场
        try:
            info = div.find('div', class_='inb right').find('div', class_='airport')
            departureAirport = info.string
        except:
            departureAirport = None
        #离开时间
        try:
            info = div.find('div', class_='inb right').find('strong', class_='time')
            departureTime = info.string
        except:
            departureTime = None
        #到达机场
        try:
            info = div.find('div', class_='inb left').find('div', class_='airport')
            arrivalAirport = info.string
        except:
            arrivalAirport = None
        #到达时间 (判断是否隔日到达)
        try:
            info = div.find('div', class_='inb left').find('strong', class_='time')
            arrivalTime = info.string
            try:
                dayPass = div.find('div', class_='inb left').find('span',class_='c-react-frame')
                arrivalTime = arrivalTime + ' ' + dayPass.string
            except:
                pass
        except:
            arrivalTime = None
        #是否经停
        try:
            info = div.find('div', class_='inb center').find('span', class_='stopover no-help').find('span')
            stopoverCity = info.string
        except:
            stopoverCity = None
        #最低价格
        try:
            info = div.find('span', class_='base_price02')
            lowestPrice = info.get_text()[1:]
        except:
            lowestPrice = None
        #准点率
        try:
            info = div.find('div', class_='inb service').find('span', class_='direction_black_border')
            punctualRate = info.string
        except:
            punctualRate = None

        #将新的提取到的航班增加到数据库中
        add_flight = [date, airlineName, flightNumber, craftTypeName, depcity, departureAirport, departureTime,
            arrcity, arrivalAirport, arrivalTime, stopoverCity, lowestPrice, punctualRate
            ]

        for info in add_flight:
            print(info,end=' ')
        print('')
        
        flights_direct.append(add_flight)
        time.sleep(1)

    divs_transit = bs.find_all('div', class_='search_box search_box_tag search_box_light Label_Transit')
    # 爬取中转机票信息
    for div in divs_transit:
        # 航空公司名称
        try:
            info_1 = div.find_all('div', class_='logo-item flight_logo')[0].find('strong')
            info_2 = div.find_all('div', class_='logo-item flight_logo')[1].find('strong')
            airlineName = info_1.get_text() + ' ' + info_2.get_text()
        except:
            airlineName = None
        #航班号
        try:
            info_1 = div.find_all('div', class_='logo-item flight_logo')[0].find_all('span')[2]
            info_2 = div.find_all('div', class_='logo-item flight_logo')[1].find_all('span')[2]
            flightNumber = info_1.string + ' ' + info_2.string
        except:
            flightNumber = None
        #没有显示机型属性

        #离开机场
        try:
            info = div.find('div', class_='inb right').find('div', class_='airport')
            departureAirport = info.string
        except:
            departureAirport = None
        #离开时间
        try:
            info = div.find('div', class_='inb right').find('strong', class_='time')
            departureTime = info.string
        except:
            departureTime = None
        #到达机场
        try:
            info = div.find('div', class_='inb left').find('div', class_='airport')
            arrivalAirport = info.string
        except:
            arrivalAirport = None
        #到达时间 (判断是否隔日到达)
        try:
            info = div.find('div', class_='inb left').find('strong', class_='time')
            arrivalTime = info.string
            try:
                dayPass = div.find('div', class_='inb left').find('span',class_='c-react-frame')
                arrivalTime = arrivalTime + ' ' + dayPass.string
            except:
                pass
        except:
            arrivalTime = None
        #中转城市
        try:
            info = div.find('div', class_='inb center').find('span',class_='city-name')
            transitCity = info.string
        except:
            transitCity = None
        #中转时间
        try:
            info = div.find('div', class_='inb center').find('span',class_='stay-time')
            transitInterval = info.string
        except:
            transitInterval = None
        #最低价格
        try:
            info = div.find('span', class_='base_price02')
            lowestPrice = info.get_text()[1:]
        except:
            lowestPrice = None
        #准点率
        punctualRate = ''
        try:
            info_1 = div.find('div', class_='inb service').find_all('span', class_='direction_black_border')[0]
            punctualRate = punctualRate + info_1.string
        except:
            punctualRate = punctualRate + 'None'
        punctualRate = punctualRate + ' '
        try:
            info_2 = div.find('div', class_='inb service').find_all('span', class_='direction_black_border')[1]
            punctualRate = punctualRate + info_2.string
        except:
            punctualRate = punctualRate + 'None'

        #将新的提取到的航班增加到数据库中
        add_flight = [date, airlineName, flightNumber, depcity, departureAirport, departureTime,
            arrcity, arrivalAirport, arrivalTime, transitCity, transitInterval, lowestPrice, punctualRate
            ]

        for info in add_flight:
            print(info,end=' ')
        print('')

        flights_transit.append(add_flight)
        time.sleep(1)
