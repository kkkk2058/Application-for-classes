# Application-for-classes Notation
# v1 : 로그인 시 서버에서 사용자 정보를 검증할 수 있도록 바꿈.
## 1. 로그인 html form을 post method를 사용 하도록 수정.
## 2. 로그인 form의 post요청 검증 결과에 따라 home 또는 현재 페이지로 redirection.
## 3. 검증은 sql logintable에 정보가 없으면 실패로 간주. -> alert창 표시 후 다시 로그인 페이지로.
### 추가해야 하는 사항 : 회원가입을 구현할 경우, jsonify를 사용해야함. html post로 온 정보를 서버(flask)에서 가공하여 logintable(mysql)에 추가해야함.
### 웹브라우저(html) -> json전환 -> flask -> mysql 형태일 듯.
### 추가해야 하는 사항2 : 각 user에 맞게 페이지를 보여줘야함. 이는 html 추가 작성 및 redirection을 통해서 가능할 듯.