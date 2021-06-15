import datetime
import json

def get_vaccines():
    vaccines = {}
    with open('../components/gis/data/provincial-vaccination-data.json', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        jsondata = jsondata['data']
        for province in jsondata:
            vaccines[province['name']] = round(province['coverage'] * 100, 2)
    return vaccines

def get_pdata():
    pdata = []
    with open('../components/gis/geo/th-provinces-centroids.json', encoding='utf-8') as json_file:
        jsondata = json.load(json_file)
        for province in jsondata['features']:
            pdata.append(province['properties']['PROV_NAMT'])
    return pdata

def get_start_end(data):
    lastRow = data.tail(1)
    date = list(lastRow['announce_date'])[0].strip()
    start = datetime.datetime.strptime("2020-12-15", "%Y-%m-%d")
    end = datetime.datetime.strptime(date, '%d/%m/%y')
    return (start, end)

def get_provinces(data, start):
    provinces = {}
    for row in data.iterrows():
        row = dict(row[1])
        province = row['province_of_isolation']
        date = row['announce_date']
        if province in provinces:
            if isinstance(date, str):
                parsedDate = datetime.datetime.strptime(date.strip(), '%d/%m/%y')
                if parsedDate >= start:
                    provinces[province].append(parsedDate)
        else:
            provinces[province] = []
    return provinces

def moving_average(ys, N=7):
    cumulative_sum = [0]
    moving_aves = []
    for i, x in enumerate(ys, 1):
        cumulative_sum.append(cumulative_sum[i - 1] + x)
        if i >= N:
            moving_ave = (cumulative_sum[i] - cumulative_sum[i - N]) / N
            # can do stuff with moving_ave here
            moving_aves.append(moving_ave)
    return moving_aves