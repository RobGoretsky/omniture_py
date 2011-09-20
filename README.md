Omniture_Py
===========
A Python Library To Simplify Accessing Omniture's SiteCatalyst Reporting API
----------------------------------------------------------------------------

This library simplifies the process of accessing the Omniture SiteCatalyst Reporting API by wrapping the REST API calls in a Python library.

First, get access configured by reading through documentation at [Omniture Developer Connection](http://developer.omniture.com/)

Then, to test authentication/access:
    import omniture_py
    ompy = OmniturePy('username:company','shared_secret')
    json_object =  ompy.run_omtr_immediate_request('Company.GetReportSuites', '')
    for suite in json_object["report_suites"]:
	  print "Report Suite ID: %s\nSite Title: %s\n" % (suite["rsid"], suite["site_title"])

To get total number of page views yesterday, just run the following.  It runs an "Overtime" report in SiteCatalyst, 
with 'pageViews' as the metric, and returns the numeric total result.
    print ompy.get_count_from_report('report_suite_name', 'pageViews') 


To get number of page views for "Homepage" and "Media Guide" combined, yesterday, run the following.  It runs a "Trended"
report in SiteCatalyst, using 'pageViews' as the metric, and 'page' as the Element, and then selecting for pages titled either
"Homepage" or "Media Guide"
    print ompy.get_count_from_report('report_suite_name', 'pageViews', 'page', ["Homepage","Media Guide"])

The get_count_from_report function currently supports requesting one dimension (called an 'element') in addition to the date, which is always implied to be included.  It also only currently supports requesting one metric at a time. 	

If you wish to have lower-level access to the Omniture API than this, you can just use the run_omtr_queue_and_wait_request, and pass it the type of request and full request body: 
    obj = ompy.run_omtr_queue_and_wait_request('Report.QueueTrended', {"reportDescription" : reportDescription})

	
	
