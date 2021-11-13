# `logistex2020.pythonanywhere.com`에서 `logistex2021.pythonanywhere.com`으로 전환

1. 깃허브에 `https://github.com/logistex/pa21`라는 리모트 저장소 생성

2. 로컬에서 깃 앱 최신화  
- BELLSTONE, [Git, 설치 및 업데이트(Windows)](https://park-jongseok.github.io/git/2019/10/06/installing-and-updating-git.html), 2019-10-06. 

```bash
$ git --version                 # 최신화 전 버전 확인
git version 2.33.0.windows.2
$ git update-git-for-windows    # 최신화
$ git --version                 # 최신화 후 버전 확인
git version 2.33.1.windows.1
```

3. 기존 로컬 폴더를 Git 저장소로 만들기  
    - [Git 최초 설정](https://git-scm.com/book/ko/v2/시작하기-Git-최초-설정)
    - `.gitignore` 파일   
   
```bash
# Git 저장소 초기화 작업

$ ls            # manage.py 존재 여부 확인

# 기존 로컬 폴더를 Git 저장소로 초기화
$ git init	    # .git 폴더 생성됨

# Git 저장소에 대한 사용자 정보 전역 설정
$ git config --global user.name "<아이디>"
$ git config --global user.email "<이메일>"
$ git config --list             # 모든 설정 확인
$ git config user.email         # 지정한 키 값에 대한 설정 확인
```  

```bash {.line-numbers}
# .gitignore 파일 내용 예시

*.pyc
*~
__pycache__
*.zip
.DS_Store
.idea
# db.sqlite3    # 포함 여부에 따른 차이를 고려
```

4. add-commit-push
[GIT Push and Pull](https://www.datacamp.com/community/tutorials/git-push-pull)
```bash
git status
git add . 
git status
git commit -m "211111 altair visualizing code added"
git remote add origin "https://github.com/logistex/pa21.git"
git push -u origin master
```

















