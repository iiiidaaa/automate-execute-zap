# ZAP for SPA
SPA向けのスキャンを実行します
ログイン周りをプロダクトごとにメンテナンスする必要があるので、スクリプトを読みながらログインスクリプトは作成してください
(ギルドでは、ログインスクリプトに機微な情報が含まれるので別途配布)

# Usage
ログインスクリプトを作成し、scriptsディレクトリに保存してください
```bash
docker build -t zap_spa .
docker run -d --name zap_spa -p8080:8080 zap_spa zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.key=qiiutul4utrfub1b8veqs50bk0 -addoninstall exportreport
docker exec -t zap_spa python3 zapscripts/zap.py
```

# 実施後
レポートはコンテナ内にしか作成されず、結果はElasticSearchに送るようにしていますが
もし必要であれば以下のコマンドでコンテナ内からコピーしてください
```
docker cp zap_spa:/zap/report.html:<おきたいところ>
```