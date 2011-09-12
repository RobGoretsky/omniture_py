import urllib2, time, binascii, sha, json

USER_NAME = 'username:company'
SHARED_SECRET = 'sharedsecret'

def get_header():
    nonce = str(time.time())
    base64nonce = binascii.b2a_base64(binascii.a2b_qp(nonce))
    created_date = time.strftime("%Y-%m-%dT%H:%M:%SZ",  time.localtime())
    sha_object = sha.new(nonce + created_date + SHARED_SECRET)
    password_64 = binascii.b2a_base64(sha_object.digest())
    return 'UsernameToken Username="%s", PasswordDigest="%s", Nonce="%s", Created="%s"' % (USER_NAME, password_64.strip(), base64nonce.strip(), created_date)

def run_omtr_immediate_request(method, request_data):
    request = urllib2.Request('https://api.omniture.com/admin/1.2/rest/?method=%s' % method, json.dumps(request_data))
    request.add_header('X-WSSE', get_header())
    return  json.loads(urllib2.urlopen(request).read())

def run_omtr_queue_and_wait_request(method, request_data):
    status_resp = run_omtr_immediate_request(method, request_data)
    report_id = status_resp['reportID']
    status = status_resp['status']
    print "Status for Report ID %s is %s" % (report_id, status)
    while status != 'done':
        time.sleep(5)
        status_resp = run_omtr_immediate_request('Report.GetStatus', {"reportID" : report_id})
        status = status_resp['status']
        print "Status for Report ID %s is %s" % (report_id, status)        
    return run_omtr_immediate_request('Report.GetReport', {'reportID' : report_id})
    

#Just for testing, this will ensure that you can connect to your report suite
if __name__ == '__main__':
    json_object =  run_omtr_immediate_request('Company.GetReportSuites', '')
    for suite in json_object["report_suites"]:
        print "Report Suite ID: %s\nSite Title: %s\n" % (suite["rsid"], suite["site_title"])
     
    
