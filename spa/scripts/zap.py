import time
from pprint import pprint
from zapv2 import ZAPv2
from settings import ZapConfig
from report import CreateReport
from sendJson import sendJson

c = ZapConfig()
# Connect ZAP API client to the listening address of ZAP instance
zap = ZAPv2(proxies=c.localProxy, apikey=c.apiKey)

# Start the ZAP session
core = zap.core
pprint('Create ZAP session: ' + c.sessionName + ' -> ' +
        core.new_session(name=c.sessionName, overwrite=True))

# Configure ZAP global Exclude URL option
print('Add Global Exclude URL regular expressions:')
for regex in c.globalExcludeUrl:
    pprint(regex + ' ->' + core.exclude_from_proxy(regex=regex))

# Define the ZAP context
context = zap.context
contextId = context.new_context(contextname=c.contextName)
pprint('Use context ID: ' + contextId)

# Include URL in the context
print('Include URL in context:')
for url in c.contextIncludeURL:
    pprint(url + ' -> ' +
            context.include_in_context(contextname=c.contextName,
                                        regex=url))

# Exclude URL in the context
print('Exclude URL from context:')
for url in c.contextExcludeURL:
    pprint(url + ' -> ' +
            context.exclude_from_context(contextname=c.contextName,
                                            regex=url))

# Setup session management for the context.
# There is no methodconfigparams to provide for both current methods
pprint('Set session management method: ' + c.sessionManagement + ' -> ' +
        zap.sessionManagement.set_session_management_method(
            contextid=contextId, methodname=c.sessionManagement,
            methodconfigparams=None))

## In case we use the scriptBasedAuthentication method, load the script
auth = zap.authentication
c.setupCSRFToken(zap)
c.setupScript(zap,contextId)

# Define either a loggedin indicator or a loggedout indicator regexp
# It allows ZAP to see if the user is always authenticated during scans
if c.isLoggedInIndicator:
    pprint('Define Loggedin indicator: ' + c.indicatorRegex + ' -> ' +
            auth.set_logged_in_indicator(contextid=contextId,
                                    loggedinindicatorregex=c.indicatorRegex))
else:
    pprint('Define Loggedout indicator: ' + c.indicatorRegex + ' -> ' +
            auth.set_logged_out_indicator(contextid=contextId,
                                    loggedoutindicatorregex=c.indicatorRegex))

# Define the users
users = zap.users
if c.createUser:
    for user in c.userList:
        userName = user.get('name')
        print('Create user ' + userName + ':')
        userId = users.new_user(contextid=contextId, name=userName)
        c.userIdList.append(userId)
        pprint('User ID: ' + userId + '; username -> ' +
                users.set_user_name(contextid=contextId, userid=userId,
                                    name=userName) +
                '; credentials -> ' +
                users.set_authentication_credentials(contextid=contextId,
                    userid=userId,
                    authcredentialsconfigparams=user.get('credentials')) +
                '; enabled -> ' +
                users.set_user_enabled(contextid=contextId, userid=userId,
                                        enabled=True))

# Enable all passive scanners (it's possible to do a more specific policy by
# setting needed scan ID: Use zap.pscan.scanners() to list all passive scanner
# IDs, then use zap.scan.enable_scanners(ids) to enable what you want
pprint('Enable all passive scanners -> ' +
        zap.pscan.enable_all_scanners())

ascan = zap.ascan
# Define if a new scan policy is used
if c.useScanPolicy:
    ascan.remove_scan_policy(scanpolicyname=c.scanPolicyName)
    pprint('Add scan policy ' + c.scanPolicyName + ' -> ' +
            ascan.add_scan_policy(scanpolicyname=c.scanPolicyName))
    for policyId in range(0, 5):
        # Set alert Threshold for all scans
        ascan.set_policy_alert_threshold(id=policyId,
                                         alertthreshold=c.alertThreshold,
                                         scanpolicyname=c.scanPolicyName)
        # Set attack strength for all scans
        ascan.set_policy_attack_strength(id=policyId,
                                         attackstrength=c.attackStrength,
                                         scanpolicyname=c.scanPolicyName)
    if c.isWhiteListPolicy:
        # Disable all active scanners in order to enable only what you need
        pprint('Disable all scanners -> ' +
                ascan.disable_all_scanners(scanpolicyname=c.scanPolicyName))
        # Enable some active scanners
        pprint('Enable given scan IDs -> ' +
                ascan.enable_scanners(ids=c.ascanIds,
                                      scanpolicyname=c.scanPolicyName))
    else:
        # Enable all active scanners
        pprint('Enable all scanners -> ' +
                ascan.enable_all_scanners(scanpolicyname=c.scanPolicyName))
        # Disable some active scanners
        pprint('Disable given scan IDs -> ' +
                ascan.disable_scanners(ids=c.ascanIds,
                                       scanpolicyname=c.scanPolicyName))
else:
    print('No custom policy used for scan')
    scanPolicyName = None

# Open URL inside ZAP
pprint('Access target URL ' + c.target)
core.access_url(url=c.target, followredirects=True)
for url in c.applicationURL:
    pprint('Access URL ' + url)
    core.access_url(url=url, followredirects=True)
# Give the sites tree a chance to get updated
time.sleep(2)

# Launch Spider, Ajax Spider (if useAjaxSpider is set to true) and
# Active scans, with a context and users or not
forcedUser = zap.forcedUser
spider = zap.spider
ajax = zap.ajaxSpider

# 希望する時間があれば記載
#ajax.set_option_max_duration(1)

scanId = 0
print('Starting Scans on target: ' + c.target)

for userId in c.userIdList:
    print('Starting scans with User ID: ' + userId)
    if c.useAjaxSpider:
        # Prepare Ajax Spider scan
        pprint('Set forced user mode enabled -> ' +
                forcedUser.set_forced_user_mode_enabled(boolean=True))
        pprint('Set user ID: ' + userId + ' for forced user mode -> ' +
                    forcedUser.set_forced_user(contextid=contextId,
                        userid=userId))
        # Ajax Spider the target URL
        pprint('Ajax Spider the target with user ID: ' + userId + ' -> ' +
                    ajax.scan(url=c.target, inscope=None))
        # Give the Ajax spider a chance to start
        time.sleep(10)
        while (ajax.status != 'stopped'):
            print('Ajax Spider is ' + ajax.status)
            time.sleep(5)
        for url in c.applicationURL:
            # Ajax Spider every url configured
            pprint('Ajax Spider the URL: ' + url + ' with user ID: ' +
                    userId + ' -> ' +
                    ajax.scan(url=url, inscope=None))
            # Give the Ajax spider a chance to start
            time.sleep(10)
            while (ajax.status != 'stopped'):
                print('Ajax Spider is ' + ajax.status)
                time.sleep(5)
        pprint('Set forced user mode disabled -> ' +
                forcedUser.set_forced_user_mode_enabled(boolean=False))
        print('Ajax Spider scan for user ID ' + userId + ' completed')

    # Launch Active Scan with the configured policy on the target url
    # and recursively scan every site node
    scanId = ascan.scan_as_user(url=c.target, contextid=contextId,
            userid=userId, recurse=True, scanpolicyname=scanPolicyName,
            method=None, postdata=True)
    print('Start Active Scan with user ID: ' + userId +
            '. Scan ID equals: ' + scanId)
    # Give the scanner a chance to start
    time.sleep(2)
    while (int(ascan.status(scanId)) < 100):
        print('Active Scan progress: ' + ascan.status(scanId) + '%')
        time.sleep(2)
    print('Active Scan for user ID ' + userId + ' completed')

# Give the passive scanner a chance to finish
time.sleep(5)

# If you want to retrieve alerts:
## pprint(zap.core.alerts(baseurl=target, start=None, count=None))

# To retrieve ZAP report in JSON and HTML format
print('JSON report create')
jsonPath = c.resultDir + 'report.json'
fileJson = open(jsonPath, 'w')
fileJson.write(core.jsonreport())
fileJson.close()
print('HTML report create')
htmlPath = c.resultDir + 'report.html'
fileHtml = open(htmlPath, 'w')
fileHtml.write(core.htmlreport())
fileHtml.close()

# To retrieve ZAP exportreport in JSON format
print('JSON exportreport create')
pathExportReport = c.resultDir + c.resultNameExportReport
if CreateReport(c,pathExportReport):
    sendJson(pathExportReport,c.esIndex)
print('scan finished')
if c.shutdownOnceFinished:
    # Shutdown ZAP once finished
    pprint('Shutdown ZAP -> ' + core.shutdown())
