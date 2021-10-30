## 목적 / 개요

- Wanted 프리온 보딩 백엔딩 코스 과제 수행
- 게시글 목록/상세 확인 API, 유저 회원가입과 인증/인가를 통한 게시글 수정/삭제/작성 접근 제한기능 구현

<br>

## EndPoint

- 회원가입    : POST/users/signup 
- 로그인      : POST/users/signin
- 게시물 목록 : GET/bulletin-board/post
- 게시물 작성 : POST/bulletin-board/post
- 게시물 수정 : PATCH/bulletin-board/post/<int:post_id>
- 게시물 삭세 : DELETE/bulletin-board/post/<int:post_id>
- 게시물 상세 : GET/bulletin-board/post-detail/<int:post_id>

<br>

## API 명세서

- 회원가입 API
> METHOD : POST
> URL : /users/signup 

> Request
```
{
    "name" : "kakarot",
    "email" : "abcde1@google.com",
    "password" : "123abc!@"
}
```

> Response
```
SUCCESS : {'message': 'SUCCESS'}, status=201

FAIL-1  : {'message': 'EXIST_EMAIL'}, status=400
FAIL-2  : {'message': 'INVALID_EMAIL_FORM'}, status=400
FAIL-3  : {'message': 'INVALID_PASSWORD_FORM'}, status=400
FAIL-4  : {'message': 'KEY_ERROR'}, status=400
```
특정 조건에 따른 입력값 제어를 위해 REGX를 이용하여 유효성검사를 하였으며
유저 비밀번호 저장 시 bcrypt 라이브러리를 통해 암호화하여 개인정보를 보호하였습니다.

<br>

- 로그인 API
> METHOD : POST
> URL : /users/signin

> Request
{
    "email" : "abcde1@google.com",
    "password" : "123abc!@"
}

> Response
```
SUCCESS : {'access_token' : access_token}, status = 201

FAIL-1  : {"message" : "INVALID_USER"}, status = 401
FAIL-2  : {"message" : "KEY_ERROR"}, status = 400
```
로그인시 입력된 암호와 DB에 암호화되어 저장된 값을 비교하는데 bcrypt 라이브러리를 사용하였고
jwt 라이브러리를 통해 로그인하는 유저의 id가 포함된 암호화 token을 발행하였습니다.

<br>

- 게시물 목록 API
> METHOD : GET
> URL : /bulletin-board/post?offset=0&limit=10

> Response
```
SUCCESS : {'results' : results}, status = 200
{
    "results": [
        {
            "author": "사라진 회원입니다.",
            "title": "Update success",
            "created_at": "2021-10-26T16:57:05.114Z"
        },
        {
            "author": "kakarot",
            "title": "거위의 꿈",
            "created_at": "2021-10-26T16:57:53.050Z"
        },
        ... ...
]
}
```
회원정보를 반환해줄 때 탈퇴 등으로 DB에서 삭제된 회원일 경우
"사라진 회원입니다."라는 구문으로 대체되도록 하였습니다.

<br>

- 특정 게시물 상세 API
> METHOD : GET
> URL : /bulletin-board/post-detail/<int:post_id>

> Response
```
SUCCESS : {'results' : results}, status = 200
{
    "results": {
        "author": "kakarot",
        "title": "Update success",
        "description": "Update success",
        "created_at": "2021-10-26T16:58:10.926Z",
        "updated_at": "2021-10-26T19:01:18.863Z"
    }
}
```
상세 페이지에서는 게시물과 관련된 대부분의 정보를 보여주는 방향으로 설정했습니다.

<br>

- 게시물 작성 API
> METHOD : POST
> URL : /bulletin-board/post

> Request
```
{
    "title": "거위의 꿈3",
    "description": "난 난꿈을꾸어쬬~",
    "created_at": "2021-10-26 14:29:41.217186"
}
```

> Response
```
SUCCESS : {'message' : 'SUCCESS'}, status = 201

FAIL-1  : {'message' : 'INVALID_USER'}, status=404
FAIL-2  : {'message': 'KEY_ERROR'}, status=400
```
게시글 작성은 토큰을 통한 인증을 거쳐야 가능하며, 토큰으로부터 가져온 유저 id를 통해
게시물의 저자가 자동으로 지정됩니다.
time.sleep(1) 으로 클라이언트 측의 연속입력 방지를 흉내 내어 보았습니다.

<br>

- 게시물 수정
> METHOD : PATCH
> URL : /bulletin-board/post/<int:post_id>

> Request
```
    "title"       : "Update success",
    "description" : "Update success"
```

> Response
```
SUCCESS : {'message' : 'SUCCESS'}, status=200

FAIL-1  : {'message' : 'INVALID_USER'}, status=404
FAIL-2  : {'message': 'KEY_ERROR'}, status=400
FAIL-3  : {'message' : 'INVALID_POST'}, status=404
```
토근을 통해 인증된 사용자와 해당 글의 작성자가 일치하는지 확인한 후 수정 가능하게 하였습니다.
datetime.datetime.now()으로 글 수정 시점의 시간이 저장되게 하였습니다.

<br>

- 게시물 삭세
> METHOD : DELETE
> URL : /bulletin-board/post/<int:post_id>

> Response
```
SUCCESS : {'message' : 'SUCCESS'}, status=200

FAIL-1  : {'message' : 'INVALID_USER'}, status=404
FAIL-2  : {'message' : 'INVALID_POST'}, status=404
```
토근을 통해 인증된 사용자와 해당 글의 작성자가 일치하는지 확인한 후 삭제 가능하게 하였습니다.