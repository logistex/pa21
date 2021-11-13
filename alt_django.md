# 알테어 시각화 결과를 장고로 배포하기 


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

