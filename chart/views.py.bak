import json  # ***json 임포트 추가***
from django.http import JsonResponse  # for chart_data()
from django.shortcuts import render
from .models import Passenger
from django.db.models import Count, Q


def home(request):
    return render(request, 'chart/chart_home.html')


def world_population(request):
    return render(request, 'chart/world_population.html')


# def covid19_view(request):
#     return render(request, 'chart/covid19.html')


def ticket_class_view_1(request):  # 방법 1
    print('방법1')
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
            survived_count=Count('ticket_class',
                                 filter=Q(survived=True)),
            not_survived_count=Count('ticket_class',
                                     filter=Q(survived=False))) \
        .order_by('ticket_class')
    return render(request, 'chart/ticket_class_1.html', {'dataset': dataset})
#  dataset = [
#    {'ticket_class': 1, 'survived_count': 200, 'not_survived_count': 123},
#    {'ticket_class': 2, 'survived_count': 119, 'not_survived_count': 158},
#    {'ticket_class': 3, 'survived_count': 181, 'not_survived_count': 528}
#  ]


def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()             # for xAxis
    survived_series = list()        # for series named 'Survived'
    not_survived_series = list()    # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])       # for xAxis
        survived_series.append(entry['survived_count'])             # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])     # for series named 'Not survived'

    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'chart/ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series)
    })


def ticket_dump():
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'
    survived_rate = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s 등석' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'
        survived_rate.append(entry['survived_count'] / (entry['survived_count'] + entry['not_survived_count']) * 100.)

    chart = {
        'chart': {
            'zoomType': 'xy',
            'borderColor': '#9DB0AC',
            'borderWidth': 3,
        },
        'title': {'text': '좌석 등급에 따른 타이타닉 생존/비 생존 인원 및 생존율'},
        'xAxis': {'categories': categories},
        'yAxis': [{  # Primary yAxis
            'labels': {
                'format': '{value} %',
                'style': {'color': 'blue'}
            }, 'title': {
                'text': '생존율',
                'style': {'color': 'blue'}
            },
        }, {  # Secondary yAxis
            'labels': {
                'format': '{value} 명',
                'style': {'color': 'black'}
            }, 'title': {
                'text': '인원',
                'style': {'color': 'black'}
            },
            'opposite': 'true'
        }, ],
        'tooltip': {
            'shared': 'true'
        },
        'legend': {
            'layout': 'vertical',
            'align': 'left',
            'x': 120,
            "verticalAlign": 'top',
            "y": 100,
            'floating': 'true',
            # 'backgroundColor':
            #     Highcharts.defaultOptions.legend.backgroundColor | | # theme
            #     'rgba(255,255,255,0.25)'
        },
        'series': [{
            'name': '생존',
            'type': 'column',
            'yAxis': 1,
            'data': survived_series_data,
            'color': 'green',
            'tooltip': {'valueSuffix': ' 명'}
        }, {
            'name': '비 생존',
            'type': 'column',
            'yAxis': 1,
            'color': 'red',
            'data': not_survived_series_data,
            'tooltip': {'valueSuffix': ' 명'}
        }, {
            'name': '생존율',
            'type': 'spline',
            'data': survived_rate,
            'tooltip': {'valueSuffix': ' %'}
        },
        ]
    }

    dump = json.dumps(chart)
    return dump


def ticket_class_view_3(request):  # 방법 3

    return render(request, 'chart/ticket_class_3.html', {'chart': ticket_dump()})


def json_example(request):  # 접속 경로 'json-example/'에 대응하는 뷰
    return render(request, 'chart/json_example.html')


def chart_data(request):  # 접속 경로 'json-example/data/'에 대응하는 뷰
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')
    #  [
    #    {'embarked': 'S', 'total': 914}
    #    {'embarked': 'C', 'total': 270},
    #    {'embarked': 'Q', 'total': 123},
    #  ]

    # # 탑승_항구 상수 정의
    # CHERBOURG = 'C'
    # QUEENSTOWN = 'Q'
    # SOUTHAMPTON = 'S'
    # PORT_CHOICES = (
    #     (CHERBOURG, 'Cherbourg'),
    #     (QUEENSTOWN, 'Queenstown'),
    #     (SOUTHAMPTON, 'Southampton'),
    # )
    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {
            'type': 'pie',
            'borderColor': '#9DB0AC',
            'borderWidth': 3,
        },
        'title': {'text': '승선 항구에 따른 타이타닉 승객 수'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)


import pandas as pd
from datetime import timezone, datetime
import arrow

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def covid_dump():
    # Section 2 - Loading and Selecting Data
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                     parse_dates=['Date'])
    # print(df.head())
    # print(len(df), '행 x', len(df.columns), '열')
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]
    # print(df.head())

    # Section 3 - Creating a Summary Column
    # df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df['Cases'] = df[['Confirmed']].sum(axis=1)
    # df['Cases'] = df[['Deaths']].sum(axis=1)

    # Section 4 - Restructuring our Data
    df = df.pivot(index='Date', columns='Country', values='Cases')
    # countries 리스트 생성
    countries = list(df.columns)
    # df.reset_index()를 통하여 기존 인덱스 열을 데이터 열로 변경
    covid = df.reset_index('Date')
    # covid 인덱스와 columns를 새로 지정
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries
    # print(covid.head())

    # Section 5 - Calculating Rates per 1,000,000
    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    # date_line = list()
    # for d in list(percapita.index):
    #     date_line.append(d.strftime('%Y-%m-%d'))
    # print(date_line)
    date_line = percapita.index.tolist()
    # print('###')

    my_data = list()
    for country in list(percapita.columns):
        my_series = list()
        for d in percapita.index.tolist():
            # print(country, d.year, d.month, d.day, round(percapita.loc[d][country], 1))
            # print(country, d, round(percapita.loc[d][country], 1))
            # t = int(datetime.datetime.strptime(d, '%d.%m.%Y %H:%M:%S,%f')) * 1000
            # dt = datetime.date(d.year, d.month, d.day)
            # timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
            my_series.append([arrow.get(d.year, d.month, d.day).timestamp * 1000, round(percapita.loc[d][country], 1)])

        my_dict = dict()
        my_dict['country'] = country
        my_dict['series'] = my_series
        my_data.append(my_dict)
    # for my_d in my_data:
    #     print(my_d['country'], my_d['series'], '\n')
    print(list(map(
        lambda entry: {'name': entry['country'], 'data': entry['series']},
        my_data)))


        # mydata.append([d, percapita[country]])
    # print(list(map(
    #         lambda country: {'name': country, 'data': percapita[country].values.tolist()},
    #         percapita.columns)))


    # Section 6 - highchart
    chart = {
        'chart': {
            'type': 'spline',
            'borderColor': '#9DB0AC',
            'borderWidth': 3,
        },
        'title': {'text': '인구 대비 COVID-19 확진자 비율'},
        'subtitle': {'text': 'Source: Johns Hopkins University Center for Systems Science and Engineering'},
        'xAxis': {'type': 'datetime',
                  # 'dateTimeLabelFormats': {'month': '%b \'%y'}
        },
        'yAxis': [{  # Primary yAxis
            'labels': {
                'format': '{value} 건/백만 명',
                'style': {'color': 'blue'}
            }, 'title': {
                'text': '누적 비율',
                'style': {'color': 'blue'}
            },
        }, ],
        'plotOptions': {
            'spline': {
                'lineWidth': 3,
                'states': {
                    'hover': {'lineWidth': 5}
                },
                # 'marker': {
                #     'enabled': 'false'
                # },
                # 'dataLabels': {
                #     'enabled': 'False'
                # },
            }
        },
        'series': list(map(
                    lambda entry: {'name': entry['country'], 'data': entry['series']},
                    my_data)
        ),
        'navigation': {
            'menuItemStyle': {'fontSize': '10px'}
        },
    }
    dump = json.dumps(chart, default=myconverter)
    return dump


def covid19_view_new(request):  # 방법 3
    return render(request, 'chart/covid19_new.html', {'chart': covid_dump()})
