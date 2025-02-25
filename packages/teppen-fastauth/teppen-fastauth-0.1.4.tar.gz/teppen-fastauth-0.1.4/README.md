# リソースアプリ API 保護ライブラリ

認証機能を提供するライブラリ。  
認証部分を別で起動しているアプリケーションで行い、リソースアプリの API の保護を実装するためのライブラリである。

## 利用方法

### 1. pip で本ライブラリをインストールする

```bash
pip install teppen-fastauth
```

### 2. 環境変数を設定する

| 環境変数名        | 説明                                                    | 必須 or 任意 | デフォルト値 | 例                           |
| ----------------- | ------------------------------------------------------- | ------------ | ------------ | ---------------------------- |
| HOST_RESOURCE_APP | リソースアプリのホスト名                                | 必須         | -            | resource-app.test.com        |
| JWKS_ENDPOINT     | 認証アプリが提供している JWKS の API エンドポイント URL | 必須         | -            | http://nginx/api/tokens/jwks |

### 3. プログラムに組み込む

保護したい API の関数の引数に`payload: AccessTokenPayload = Depends(get_bearer_access_token_decode)`を追加すれば、保護が可能。  
実際の最小のプログラムは以下の通り。

```py
from fastapi import FastAPI, Depends
from fastauth import get_bearer_access_token_decode, AccessTokenPayload

app = FastAPI()

@app.get("/")
def root(payload: AccessTokenPayload = Depends(get_bearer_access_token_decode)):
    return {"message": "Hello World"}
```

このライブラリは、HTTP ヘッダーに含まれる Bearer トークンにて認証確認を行う。  
そのため、トークンの受け渡しのために、フロントエンド側のプログラムが必要。  
これに関してもライブラリ化しているため、そちらを利用されたし。

