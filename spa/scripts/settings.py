from pprint import pprint
from zapv2 import ZAPv2

class ZapConfig :
    def __init__(self):
        # ZAPのAPIにアクセスするためのホスト名とポート
        # デフォルトの動作から変更する必要がなければそのままで
        proxy_host = "127.0.0.1"
        proxy_port = "8080"

        # 診断対象に含めるURLを正規表現で
        # 複数のドメインが存在している場合には、カンマ区切りのリストにしてください
        self.contextIncludeURL = ['http://localhost:8000.*']

        # 診断対象から除外するURLを正規表現で
        # 上の診断対象に含めるURL以外に攻撃リクエストは送信されないので空リストでも問題ありません
        self.globalExcludeUrl = ['^(?:(?!http://localhost:8000).*).$']

        # スパイダーの起点とするURL
        self.target = 'http://localhost:8000/'

        # 上以外にも起点にしたいURLがあれば ZAPが見つけられなさそうなURLを
        self.applicationURL = []

        # ログインなどが存在するため、ユーザー情報が必要ならばTrueにしてください
        self.createUser = True
        # 診断時に使用するユーザーを設定します
        self.userList = [
            {'name': 'guest1', 'credentials': 'Username=guest1&Password=guest1'}
            ]

        # ログイン状態を判断するためにしよう
        # indicatorRegexにログインしている時に見える文字列を設定できる場合はTrue、ログアウト時に見える文字列を設定できる場合はFalse
        self.isLoggedInIndicator = False
        # ログインしている時orログインしていない時に常に見えている文字列を設定
        # この文字列が見えている(上がFalse)/見えていない(上がTrue)ときにログインマクロを実行します
        self.indicatorRegex = '\QLocation: /login\E'

        # 認証用スクリプトの設定 なければ適当で
        self.authMethod = 'scriptBasedAuthentication'
        # TODO script関係はクラス化してロードなどもそこでやるほうがいい
        self.scripts = [{
                # スクリプトの名前
                'authScriptName' : 'login.zst',
                # スクリプトのタイプ
                'authScriptType' : 'authentication',
                # スクリプトのエンジン ここら辺は有識者が書いたほうがいい
                #authScriptEngine = 'Oracle Nashorn'
                'authScriptEngine' : 'Mozilla Zest',
                # スクリプトのパス
                'authScriptFileName' : '/zap/zapscripts/login.zst',
                'authScriptDescription' : 'This is a description',

                # スクリプトのパラメータ
                'authParams' : ('scriptName=plogin.zst&'
                            'Submission Form URL='
                            'Username field=username&'
                            'Password field=password&')}
                        ]

        # サイトでCSRFトークンを使用している場合以下に記載
        self.csrfTokens=[
            "token",
            "csrftoken"
        ]

        # Elastic Searchのindexの接頭辞
        self.esIndex = "pigg"

        ### ここから下は基本的に修正の必要はないです ###

        # スキャン結果の保存場所
        self.resultDir='/zap/'
        self.resultNameExportReport='exreport.json'
        # MANDATORY. Define the API key generated by ZAP and used to verify actions.
        self.apiKey='qiiutul4utrfub1b8veqs50bk0'

        # MANDATORY. Define the listening address of ZAP instance
        self.proxyAddr = "{}:{}".format(proxy_host,proxy_port)
        self.localProxy = {"http": self.proxyAddr, "http": self.proxyAddr}

        # MANDATORY. True to create another ZAP session (overwritte the former if the
        # same name already exists), False to use an existing one
        self.isNewSession = True
        # MANDATORY. ZAP Session name
        self.sessionName = 'zap_session'

        # MANDATORY only if defineNewContext is True. Ignored otherwise
        self.contextName = 'zap_ajax_scan'
        # MANDATORY only if defineNewContext is False. Disregarded otherwise.
        # Corresponds to the ID of the context to use
        self.contextId = 0

        # Define Context Exclude URL regular expressions. Ignored if useContextForScan
        # is False. List can be empty.
        self.contextExcludeURL = []

        # MANDATORY only if useContextForScan is True. Ignored otherwise. Define the
        # session management method for the context. Possible values are:
        # "cookieBasedSessionManagement"; "httpAuthSessionManagement"
        self.sessionManagement = 'cookieBasedSessionManagement'

        # MANDATORY only if useContextForScan is True. Ignored otherwise. List can be
        # empty. Define the userid list. Created users will be added to this list later
        self.userIdList = []

        # MANDATORY. Set value to True if you want to customize and use a scan policy
        self.useScanPolicy = False
        # MANDATORY only if useScanPolicy is True. Ignored otherwise. Set a policy name
        self.scanPolicyName = 'SQL Injection and XSS'
        # MANDATORY only if useScanPolicy is True. Ignored otherwise.
        # Set value to True to disable all scan types except the ones set in ascanIds,
        # False to enable all scan types except the ones set in ascanIds..
        self.isWhiteListPolicy = True
        # MANDATORY only if useScanPolicy is True. Ignored otherwise. Set the scan IDs
        # to use with the policy. Other scan types will be disabled if
        # isWhiteListPolicy is True, enabled if isWhiteListPolicy is False.
        # Use zap.ascan.scanners() to list all ascan IDs.
        ## In the example bellow, the first line corresponds to SQL Injection scan IDs,
        ## the second line corresponds to some XSS scan IDs
        self.ascanIds = [40018, 40019, 40020, 40021, 40022, 40024, 90018,
                    40012, 40014, 40016, 40017]
        # MANDATORY only if useScanPolicy is True. Ignored otherwise. Set the alert
        # Threshold and the attack strength of enabled active scans.
        # Currently, possible values are:
        # Low, Medium and High for alert Threshold
        # Low, Medium, High and Insane for attack strength
        self.alertThreshold = 'Medium'
        self.attackStrength = 'Low'

        # MANDATORY. Set True to use Ajax Spider, False otherwise.
        self.useAjaxSpider = True

        # MANDATORY. Set True to shutdown ZAP once finished, False otherwise
        self.shutdownOnceFinished = False

    def setupCSRFToken(self,zap):
        acsrf = zap.acsrf
        for csrft in self.csrfTokens:
            pprint('Add CSRF Token:: ' + csrft + ' -> ' +
            acsrf.add_option_token(csrft))
        pass

    def setupScript(self,zap,contextId):
        script = zap.script
        auth = zap.authentication
        for authScript in self.scripts:
            script.remove(scriptname=authScript['authScriptName'])
            pprint('Load script: ' + authScript['authScriptName'] + ' -> ' +
                    script.load(scriptname=authScript['authScriptName'],
                                scripttype=authScript['authScriptType'],
                                scriptengine=authScript['authScriptEngine'],
                                filename=authScript['authScriptFileName'],
                                scriptdescription=authScript['authScriptDescription']))
            if authScript['authScriptType'] == 'authentication':
                # Define an authentication method with parameters for the context
                pprint('Set authentication method: ' + self.authMethod + ' -> ' +
                        auth.set_authentication_method(contextid=contextId,
                                                    authmethodname=self.authMethod,
                                                    authmethodconfigparams=authScript['authParams']))
