import splunklib.client as client
from splunklib import results

from xbase_util.common_util import date2s


def get_splunk_pa(start_time, end_time, splunk_host,
                  splunk_port,
                  splunk_username,
                  splunk_password,
                  splunk_scheme="https",
                  splunk_filter="THREAT AND NOT informational",
                  count=10000):
    """
    获取PA威胁信息
    :param splunk_filter:
    :param start_time:
    :param end_time:
    :param splunk_host:
    :param splunk_port:
    :param splunk_username:
    :param splunk_password:
    :param splunk_scheme:
    :return:
    """
    service = client.connect(
        host=splunk_host,
        port=splunk_port,
        scheme=splunk_scheme,
        username=splunk_username,
        password=splunk_password
    )
    job = service.jobs.oneshot(
        '''search index=idx_pa
FILTER_TEXT
| eval values = split(_raw, ",")
| eval THREAT_TIME = strftime(_time, "%Y-%m-%d %H:%M:%S")
| eval SIP = mvindex(values, 7) 
| eval DIP = mvindex(values, 8) 
| eval S_PORT = mvindex(values, 24) 
| eval D_PORT = mvindex(values, 25) 
| eval XFF_IP = mvindex(values, 79) 
| eval PROTOCOL = mvindex(values, 29) 
| eval DENY_METHOD = mvindex(values, 30) 
| eval THREAT_SUMMARY =  mvindex(values, 32)
| eval SEVERITY =  mvindex(values, 34)
| search SEVERITY IN ("medium", "high", "critical", "low")
| search NOT THREAT_SUMMARY="*HTTP Unauthorized Brute Force Attack*"
| search NOT THREAT_SUMMARY="*SSH User Authentication Brute Force Attempt*"
| table THREAT_TIME,SIP,S_PORT, DIP, D_PORT,XFF_IP,PROTOCOL, DENY_METHOD, THREAT_SUMMARY, SEVERITY
| dedup THREAT_TIME,SIP,S_PORT, DIP, D_PORT,XFF_IP,PROTOCOL'''.replace("FILTER_TEXT", splunk_filter).replace('"', '\"'),
        **{
            "earliest_time": date2s(start_time, pattern='%Y-%m-%dT%H:%M:%S'),
            "latest_time": date2s(end_time, pattern='%Y-%m-%dT%H:%M:%S'),
            "output_mode": "json",
            "count": count
        })
    return [item for item in results.JSONResultsReader(job) if isinstance(item, dict)]


def get_splunk_waf(start_time,
                   end_time,
                   splunk_host,
                   splunk_port,
                   splunk_username,
                   splunk_password,
                   splunk_scheme="https",count=10000):
    service = client.connect(
        host=splunk_host,
        port=splunk_port,
        scheme=splunk_scheme,
        username=splunk_username,
        password=splunk_password)
    exp = '''search sourcetype=changting:waf
| rex field=_raw "(?<json_data>{.*})"
| spath input=json_data
| eval THREAT_TIME=strftime(_time,"%Y-%m-%d %H:%M:%S")
| eval SIP=src_ip
| eval S_PORT=src_port
| eval DIP=dest_ip
| eval D_PORT=dest_port
| eval XFF_IP=x_forwarded_for
| eval PROTOCOL=protocol
| eval DENY_METHOD=action
| eval THREAT_SUMMARY=reason
| eval SEVERITY=risk_level
| table THREAT_TIME,SIP,S_PORT,DIP,D_PORT,XFF_IP,PROTOCOL,DENY_METHOD,THREAT_SUMMARY,SEVERITY
| dedup THREAT_TIME,SIP,S_PORT,DIP,D_PORT,XFF_IP,PROTOCOL'''.replace('"', '\"')
    job = service.jobs.oneshot(
        exp, **{
            # "earliest_time": date2s(start_time, pattern='%Y-%m-%dT%H:%M:%S')+'.000+08:00',
            # "latest_time": date2s(end_time, pattern='%Y-%m-%dT%H:%M:%S')+'.000+08:00',
            "earliest_time": date2s(start_time, pattern='%Y-%m-%dT%H:%M:%S'),
            "latest_time": date2s(end_time, pattern='%Y-%m-%dT%H:%M:%S'),
            "output_mode": "json",
            "count": count
        })
    return [item for item in results.JSONResultsReader(job) if isinstance(item, dict)]
