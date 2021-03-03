from django.shortcuts import render
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':  # 회원 가입 정보가 서버로 전달된 상태이면
        user_form = RegisterForm(request.POST)                # 유효성 검사 수행
        if user_form.is_valid():                              # 유효성 검사 문제가 없다면 2 단계 절차 수행
            new_user = user_form.save(commit=False)                    # DB 저장 없이 메모리 객체만 생성
            new_user.set_password(user_form.cleaned_data['password'])  # 암호화된 비밀번호 지정
            new_user.save()                                            # DB에 객체 저장
            return render(request,
                'registration/register_done.html',                     # register_done 페이지 출력
                {'new_user': new_user})                                # 맥락변수 전달
    else:  # 회원 가입 정보가 서버로 전달되지 않은 상태이면
        user_form = RegisterForm()

    return render(request, 'registration/register.html',{'form': user_form})