# 알테어 시각화 결과를 장고로 배포하기 

- [신교수 파이썬애니웨어 사이트](http://logistex2021.pythonanywhere.com)
  - {'id'; '손님', 'pw'; '0000'}으로 로그인
  - `차트` 메뉴 중 처음 두 하위 메뉴가 알테어로 작성한 차트 
    - `알테어 산점도`
    - `알테어 상호작용`    
- [신교수 파이썬애니웨어 사이트를 위한 깃허브 저장소](https://github.com/logistex/pa21)
- 알테어 관련 패키지 설치
  ```shell
  $ conda install -c conda-forge altair vega_datasets vega
  ```
- 알테어 차트를 장고로 배포하는 방법
  - 뷰에서 알테어 차트를 json 형식으로 저장하여 템플릿으로 전달
  - 템플릿에서는 전달받은 json 형식 차트 명세를 `spec` 변수에 지정
- `알테어 산점도` 작성을 위한 코드
  - 뷰 코드  
    ```python
    # views.py 
    def alt_django(request):
        import altair as alt
        from vega_datasets import data

        cars = data.cars()
        chart_json = alt.Chart(cars).mark_circle().encode(
            alt.X('Miles_per_Gallon'),
            alt.Y('Horsepower'),
            alt.Color('Origin'),
        ).to_json()                                                                 # 차트를 json 형식으로 저장 
        return render(request, 'chart/alt_chart.html', {'chart_json': chart_json})  # 저장한 json 형식 차트를 템플릿으로 전달
    ```  
  
  - 템플릿 코드
    ```html
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-lite@3"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-embed@4"></script>
      </head>
      <body>
        <div id="vis"></div>                                                                      
        <script type="text/javascript">
            var spec = {{ chart_json|safe }};                    /* json 형식 차트를 지정 */   
            var opt = {"renderer": "canvas", "actions": false};    
            vegaEmbed("#vis", spec, opt);
        </script>
      </body>
    </html>
    ```
- `알테어 상호작용` 작성을 위한 코드
  - 뷰 코드  
    ```python
    # views.py 
    def alt_interactive(request):
        import altair as alt
        from vega_datasets import data
        
        domain = ['Europe', 'Japan', 'USA', ]
        range_ = ['red', 'green', 'blue', ]

        cars = data.cars()
        # x-축 인코딩에 대한 선택 구간 생성하여 브러쉬로 정의
        brush = alt.selection_interval(encodings=['x'], )

        # 브러쉬에 해당하면 진하게, 브러시에서 벗어나면 연하게
        opacity = alt.condition(brush, alt.value(0.9), alt.value(0.1), )

        # 연도별 자동차 도수를 개괄하는 도수분포도
        # 연도별 자동차 도수를 선택하는 상호작용적 구간 브러쉬 추가
        overview = alt.Chart(cars).mark_bar().encode(
            alt.X('Year:O', timeUnit='year',                # 연도를 추출하고 서수형으로 지정
                  axis=alt.Axis(title=None, labelAngle=0),  # 축 제목 생략, 축 눈금 레이블 각도 생략
                  ),
            alt.Y('count()', title=None),                   # 도수, 축 제목 생략
            opacity=opacity,
        ).add_selection(
            brush,                                          # 차트에 대한 구간 브러쉬 선택 추가
        ).properties(
            width=800,                                      # 차트   폭 800 픽셀로 설정
            height=150,                                     # 차트 높이 150 픽셀로 설정
            title = {
                'text': ['', '알테어 상호작용성', ''],
                'subtitle': ['자동차 히스토그램'],
            },
        )

        # 개괄 도수분포도에 대응하는 상세 마력-연비 산점도
        # 브러쉬 선택에 대응하는 산점도 내부 점의 투명도 조절
        detail = alt.Chart(cars).mark_circle().encode(
            alt.X('Miles_per_Gallon', axis=alt.Axis(title='연비 [단위: 갤론 당 마일]'), ),
            alt.Y('Horsepower', axis=alt.Axis(title='마력'), ),
            alt.Color('Origin',
                      legend=alt.Legend(
                          title='원산지',
                          orient='none',
                          legendX=820,
                          legendY=230,
                      ),
                      scale=alt.Scale(domain=domain, range=range_, ), 
            ),
            opacity=opacity,                                # 브러쉬 선택에 대응하여 투명도 조절
        ).properties(
            width=800,                                      # 차트 폭을 상단 차트와 동일하게 설정
            height=500,
            title={
                'text': [''],
                'subtitle': ['연비-마력 산점도'], 
            },
        )

        # '&' 연산자로 차트 수직 병합
        interlinked = overview & detail
        interlinked_json = interlinked.to_json()
        return render(request, 'chart/alt_interactive.html', {'interlinked_json': interlinked_json})
    ```  
  
  - 템플릿 코드
    ```html
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-lite@3"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-embed@4"></script>
      </head>
      <body>
        <div id="vis"></div>                                                                      
        <script type="text/javascript">
            var spec = {{ interlinked_json|safe }};              /* json 형식 차트를 지정 */   
            var opt = {"renderer": "canvas", "actions": false};    
            vegaEmbed("#vis", spec, opt);
        </script>
      </body>
    </html>
    ```



- [깃허브](https://github.com/logistex/pa21)에서 코드 다운로드
- `conda env create --file dstagram.yml` 명령으로 가상환경 복원
- urlencode 관련 오류 대책
  - C:\anaconda3\envs\dstagram\lib\site-packages\disqus\__init__.py 파일에서 urlencode 관련 오류가 발생함
  - 해당 파일을 아래와 같이 수정

```PYTHON {.line-numbers}
import json

# from django.utils.six.moves.urllib.parse import urlencode  # 수정 전
# from django.utils.six.moves.urllib.request import urlopen  # 수정 전
from six.moves.urllib.parse import urlencode  # 수정 후
from six.moves.urllib.request import urlopen  # 수정 후
from django.core.management.base import CommandError
# ...
```
- chart 앱에서 사용하는 pandas 설치 필요
- arrow 설치 필요

- chart.views.py에서 `arrow.get().timestamp()`에서 `timestamp()` 부분의 괄호 누락을 수정

- altair, vega_datasets 설치

- views.py에 알테어 시각화 코드 작성하여 to_json()으로 변수에 저장하고, 템플릿에게 전달

```PYTHON {.line-numbers}
def alt_django(request):
    import altair as alt
    from vega_datasets import data

    cars = data.cars()
    chart_json = alt.Chart(cars).mark_circle().encode(
        alt.X('Horsepower'),
        alt.Y('Miles_per_Gallon'),
        alt.Color('Origin'),
    ).to_json()
    return render(request, 'chart/alt_chart.html', {'chart_json': chart_json})
```

- 템플릿에서 to_json()으로 저장한 변수를 전달받아서 시각화 결과 출력
```PYTHON {.line-numbers}
{% extends 'chart_home.html' %}

{% block head %}
    <script src="https://cdn.jsdelivr.net/npm/vega@5"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-lite@3"></script>
    <script src="https://cdn.jsdelivr.net/npm/vega-embed@4"></script>
{% endblock %}

{% block content %}
    <div id="vis"></div>
    <script type="text/javascript">
        var spec = {{ chart_json|safe }};  /* JSON output for your chart's specification */
        var opt = {"renderer": "canvas", "actions": false};  /* Options for the embedding */
        vegaEmbed("#vis", spec, opt);
    </script>
{% endblock content %}
```

