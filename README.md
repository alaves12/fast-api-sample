# AWS Lambda for FastAPI

## 課題

pythonのfastapiを使い、postした画像をAWSのs3に保存し、保存先のurlをreturnするAPIをlambdaのfunctionとして書く。


## セットアップ

1. クレデンシャル情報を設置

    ```bash
    cp -a .env.example .env
    vim .env

    以下を書き換える
    AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXX
    AWS_SECRET_ACCESS_KEY=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
    ```
2. サービス名を書き換える

    ```bash
    vim apps/app/serverless.yml 

    service: サービス名
    ```

    ```bash
    vim apps/app/main.py
    
    def create_file(file: UploadFile = File(...)):
      service_name = サービス名 
    ```

3. Dockerイメージの作成

    ```bash
    docker-compose build
    ```

4. パッケージのインストール

    ```bash
    docker-compose run --rm app yarn install
    ```

## デプロイ

### ステージング環境

```bash
docker-compose run --rm app yarn run deploy -s dev
```

### 本番環境

```bash
docker-compose run --rm app yarn run deploy -s prod
```

## 確認方法

### ローカルでのテスト

```bash
docker-compose up -d
```

```bash
curl -X POST "localhost:8000/files/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@img1.jpg;type=image/jpeg"
```

### 本番環境でのテスト
```bash
curl -X POST "エンドポイントURL/files/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@img1.jpg;type=image/jpeg"
```

## 結果
ローカルで画像をPOSTした際はリターンされたurlから画像をダウンロードし表示することができた。
しかしデプロイ後 apigatewayのエンドポイントにPOSTした際は、urlは一応リターンされダウンロードもできたが画像が表示されなかった。


## ライセンス

[MIT license](https://en.wikipedia.org/wiki/MIT_License).