'''
利用selenium爬取携程上北京大兴机场近七日全部出港、到港航班及相关信息
'''
'''
Author: YingjiaWang-HUST
Date: 2020-05-18
RelatedPage: https://blog.csdn.net/qq_37571708/article/details/103543172?ops_request_misc=&request_id=&biz_id=102&utm_source=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-2
'''

import time, datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

from get_info import get_info
from parse_info import parse_info
from change_depcity_get_info import change_depcity_get_info
from change_arrcity_get_info import change_arrcity_get_info

citys = {"YIE":"阿尔山","AKU":"阿克苏","AXF":"阿拉善左旗","AAT":"阿勒泰","AQG":"安庆","AVA":"安顺","AOG":"鞍山"
    ,"RLK":"巴彦淖尔","AEB":"百色","BAV":"包头","BSD":"保山","BHY":"北海","DBC":"白城","NBS":"白山","BFJ":"毕节"
    ,"BPL":"博乐","CKG":"重庆","BPX":"昌都","CGD":"常德","CZX":"常州" ,"CHG":"朝阳","CTU":"成都","JUH":"池州"
    ,"CIF":"赤峰","SWA":"潮州","CGQ":"长春","CSX":"长沙","CIH":"长治","CDE":"承德" ,"CWJ":"沧源","DAX":"达州"
    ,"DLU":"大理","DLC":"大连","DQA":"大庆","DAT":"大同","DDG":"丹东","DCY":"稻城","DOY":"东营" ,"DNH":"敦煌"
    ,"DAX":"达县","LUM":"德宏","EJN":"额济纳旗","DSN":"鄂尔多斯","ENH":"恩施","ERL":"二连浩特","FUO":"佛山" 
    ,"FOC":"福州","FYJ":"抚远","FUG":"阜阳","KOW":"赣州","GOQ":"格尔木","GYU":"固原","GYS":"广元","CAN":"广州","KWE":"贵阳" 
    ,"KWL":"桂林","HRB":"哈尔滨","HMI":"哈密","HAK":"海口","HLD":"海拉尔","HDG":"邯郸","HZG":"汉中","HGH":"杭州","HFE":"合肥" 
    ,"HTN":"和田","HEK":"黑河","HET":"呼和浩特","HIA":"淮安","HJJ":"怀化","TXN":"黄山","HUZ":"惠州","JXA":"鸡西","TNA":"济南" 
    ,"JNG":"济宁","JGD":"加格达奇","JMU":"佳木斯","JGN":"嘉峪关","SWA":"揭阳","JIC":"金昌","KNH":"金门","JNZ":"锦州" 
    ,"CYI":"嘉义","JHG":"景洪","JSJ":"建三江","JJN":"晋江","JGS":"井冈山","JDZ":"景德镇","JIU":"九江","JZH":"九寨沟","KHG":"喀什" 
    ,"KJH":"凯里","KGT":"康定","KRY":"克拉玛依","KCA":"库车","KRL":"库尔勒","KMG":"昆明","LXA":"拉萨","LHW":"兰州","HZH":"黎平" 
    ,"LJG":"丽江","LLB":"荔波","LYG":"连云港","LPF":"六盘水","LFQ":"临汾","LZY":"林芝","LNJ":"临沧","LYI":"临沂","LZH":"柳州" 
    ,"LZO":"泸州","LYA":"洛阳","LLV":"吕梁","JMJ":"澜沧","LCX":"龙岩","NZH":"满洲里","LUM":"芒市","MXZ":"梅州","MIG":"绵阳" 
    ,"OHE":"漠河","MDG":"牡丹江","MFK":"马祖" ,"KHN":"南昌","NAO":"南充","NKG":"南京","NNG":"南宁","NTG":"南通","NNY":"南阳" 
    ,"NGB":"宁波","NLH":"宁蒗","PZI":"攀枝花","SYM":"普洱","NDG":"齐齐哈尔","JIQ":"黔江","IQM":"且末","BPE":"秦皇岛","TAO":"青岛" 
    ,"IQN":"庆阳","JUZ":"衢州","RKZ":"日喀则","RIZ":"日照","SYX":"三亚","XMN":"厦门","SHA":"上海","SZX":"深圳","HPG":"神农架" 
    ,"SHE":"沈阳","SJW":"石家庄","TCG":"塔城","HYN":"台州","TYN":"太原","YTY":"泰州","TVS":"唐山","TCZ":"腾冲","TSN":"天津" 
    ,"THQ":"天水","TGO":"通辽","TEN":"铜仁","TLQ":"吐鲁番","WXN":"万州","WEH":"威海","WEF":"潍坊","WNZ":"温州","WNH":"文山" 
    ,"WUA":"乌海","HLH":"乌兰浩特","URC":"乌鲁木齐","WUX":"无锡","WUZ":"梧州","WUH":"武汉","WUS":"武夷山","SIA":"西安","XIC":"西昌" 
    ,"XNN":"西宁","JHG":"西双版纳","XIL":"锡林浩特","DIG":"香格里拉(迪庆)","XFN":"襄阳","ACX":"兴义","XUZ":"徐州" 
    ,"YNT":"烟台","ENY":"延安","YNJ":"延吉","YNZ":"盐城","YTY":"扬州","LDS":"伊春","YIN":"伊宁","YBP":"宜宾","YIH":"宜昌" 
    ,"YIC":"宜春","YIW":"义乌","INC":"银川","LLF":"永州","UYN":"榆林","YUS":"玉树","YCU":"运城","ZHA":"湛江","DYG":"张家界" 
    ,"ZQZ":"张家口","YZY":"张掖","ZAT":"昭通","CGO":"郑州","ZHY":"中卫","HSN":"舟山","ZUH":"珠海","WMT":"遵义(茅台)","ZYI":"遵义(新舟)"} 

citys = list(citys.values())

def main():
    # 列表分别为出港直达，出港中转，进港直达，进港中转
    flights_out_direct = []
    flights_out_transit = []
    flights_in_direct = []
    flights_in_transit = []
    
    # 时间设定为最近三个月
    dates = []
    total_days = 30
    day = datetime.date.today() + datetime.timedelta(days = 12)
    dates.append(str(day))
    for i in range(total_days-1):
        day = day + datetime.timedelta(days = 1)
        dates.append(str(day))

    # 导出文件列名
    columns_direct = ['date', 'airlineName', 'flightNumber', 'craftTypeName', 'departureCity','departureAirport', 'departureTime',
        'arrivalCity', 'arrivalAirport', 'arrivalTime', 'stopoverCity', 'lowestPrice', 'punctualRate'
        ]

    columns_transit = ['date', 'airlineName', 'flightNumber', 'departureCity', 'departureAirport', 'departureTime',
        'arrivalCity', 'arrivalAirport', 'arrivalTime', 'transitCity', 'transitInterval', 'lowestPrice', 'punctualRate'
        ]
    '''
    # 爬取大兴出港航班
    first_city = True
    for date in dates:
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 20)
        print('时间: ' + date + '\n')

        for city in citys:
            if first_city:
                print('北京 -> ' + city + ':')                    
                source = get_info(browser,wait,u'北京(大兴国际机场)',city,date)
                parse_info(date,u'北京',city,flights_out_direct,flights_out_transit,source)
                first_city = False
            else:
                print('北京 -> ' + city + ':')
                source = change_arrcity_get_info(browser,wait,city,date)
                parse_info(date,u'北京',city,flights_out_direct,flights_out_transit,source)
        first_city = True
        print('')
        browser.quit()
        time.sleep(5)

        # 出港航班导出csv文件
        csv_out_direct = pd.DataFrame(columns=columns_direct,data=flights_out_direct)
        csv_out_direct_name = date + '_out_direct.csv'
        csv_out_direct.to_csv('./info_direct/'+csv_out_direct_name, encoding = 'utf8')

        csv_out_transit = pd.DataFrame(columns=columns_transit,data=flights_out_transit)
        csv_out_transit_name = date + '_out_transit.csv'
        csv_out_transit.to_csv('./info_transit/'+csv_out_transit_name, encoding = 'utf8')


        print('flights_out_direct has {} items.'.format(len(flights_out_direct)))
        print('flights_out_transit has {} items.'.format(len(flights_out_transit)))

        flights_out_direct = []
        flights_out_transit = []
    '''
    # 爬取大兴入港航班
    first_city = True
    for date in dates:
        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 20)
        print('时间: ' + date + '\n')

        for city in citys:
            if first_city:
                print(city + ' -> 北京:')                    
                source = get_info(browser,wait,city,u'北京(大兴国际机场)',date)
                parse_info(date,city,u'北京',flights_in_direct,flights_in_transit,source)
                first_city = False
            else:
                print(city + ' -> 北京:')
                source = change_depcity_get_info(browser,wait,city,date)
                parse_info(date,city,u'北京',flights_in_direct,flights_in_transit,source)
        first_city = True
        print('')

        browser.quit()
        time.sleep(5)

        # 入港航班导出csv文件
        csv_in_direct = pd.DataFrame(columns=columns_direct,data=flights_in_direct)
        csv_in_direct_name = date + '_in_direct.csv'
        csv_in_direct.to_csv('./info_direct/'+csv_in_direct_name, encoding = 'utf8')

        csv_in_transit = pd.DataFrame(columns=columns_transit,data=flights_in_transit)
        csv_in_transit_name = date + '_in_transit.csv'
        csv_in_transit.to_csv('./info_transit/'+csv_in_transit_name, encoding = 'utf8')

        print('flights_in_direct has {} items.'.format(len(flights_in_direct)))
        print('flights_in_transit has {} items.'.format(len(flights_in_transit)))

        flights_in_direct = []
        flights_in_transit = []

    print('Work is done.')

main()



