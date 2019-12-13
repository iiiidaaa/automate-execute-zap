# Jenkins-ZAP
JenkinsのジョブとしてZAPの脆弱性診断を行います
結果はElasticSearchに送ります
デフォルトの設定としてサンプルのジョブが含まれています  
(サンプル実行を行う分には、スクリプトの作成や設定ファイルの変更は要りません)

## 使い方
### 0. ZAPのログインスクリプトの作成
以下のページを参考にログインスクリプトを作成して、zap_option/login.zstと置き換えてください  
https://www.coveros.com/scripting-authenticated-login-within-zap-vulnerability-scanner/

### 1. 初期設定
- volumeマウント用のディレクトリ作成
```bash
mkdir jenkins_home
chown -R 1000:1000 jenkins_home
```
- dockerの起動
```bash
$ docker build -t jenkins_zap .
$ docker run -d --name jenkins_zap -p 8080:8080 -p 50000:50000 -v $PWD/jenkins_home:/var/jenkins_home jenkins_zap
```

- Jenkinsのセットアップ
  - http://localhost:8080/ にブラウザでアクセスしてください
  - jenkinsが立ち上がったのを確認したら以下のコマンドでjobを作成してください
  - スクリプト内でjenkinsの再起動が入ります
```bash
bash setup.sh
```

### 2. JOBの実行
JENKINSにログインし直して、`SEND_ES`のジョブを実行することでZAPによるスキャンからElasticSearchに結果を送信するジョブが実行されます  
ElasticSearchに送信されるindex名も`test-日付`でベタ書きなので必要に応じて書き換えてください。

### 3. 停止
```bash
docker stop jenkins_zap
```
不要になったコンテナは手動で削除してください
