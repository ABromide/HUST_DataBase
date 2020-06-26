import pandas as pd
import numpy as np

path = '/home/yingjia/DBlab/crawl_airinfo/'

# 读取数据
directinfo = pd.read_csv(path + 'DirectInfo.csv', encoding='utf8')
transitinfo = pd.read_csv(path + 'TransitInfo2.csv', encoding='utf8')


# 直达
seats = []

CraftType = directinfo['craftTypeName']

# 随机确定座位
for i in range(len(directinfo)):
    # 空值 和 中型 都当成 150座
    if pd.isna(CraftType.iloc[i]) or CraftType[i][-3:-1] == '中型':
        x = np.random.randint(0,2,149)
        y = '1' + ''.join([str(i) for i in x]) + '\t'
        seats.append(y)
    # 大型 当成 240座
    elif CraftType[i][-3:-1] == '大型':
        x = np.random.randint(0,2,239)
        y = '1' + ''.join([str(i) for i in x]) + '\t'
        seats.append(y)

seats = pd.Series(seats)
SeatInfo1 = directinfo[['date','flightNumber','departureCity','arrivalCity']]
SeatInfo1 = pd.concat([SeatInfo1,seats],axis=1)

# 中转
seats = []

for i in range(len(transitinfo)):
    # 前后各 150座
    x1 = np.random.randint(0,2,149)
    x2 = np.random.randint(0,2,149)
    y = '1' + ''.join([str(i) for i in x1]) + '1' + ''.join([str(i) for i in x2]) +'\t'
    seats.append(y)

seats = pd.Series(seats)
SeatInfo2 = transitinfo[['date','flightNumber','departureCity','arrivalCity']]
SeatInfo2 = pd.concat([SeatInfo2,seats],axis=1)

# 汇总
SeatInfo = pd.concat([SeatInfo1,SeatInfo2])

# 输出
SeatInfo.to_csv('SeatInfo.csv',encoding='utf8')



