#!/usr/bin/python

#get information from logfile
#example file: apache2.log

import re
import urlparse


def get_all_success_links(path):
    """Get all link with success tatus(status code is 200)"""
    # sample log:
    #(domain:port)  (ip)           (date_access)                (method url            http_version)    (status_code)   (total)     (referer)       'user-agent'
    #cnweb:80       127.0.0.1 - - [10/Jun/2013:08:53:37 +0700] "GET /js/cab.youtube.js HTTP/1.1"        304             211         "http://cnweb/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22"
    #cnweb:80 127.0.0.1 - - [10/Jun/2013:08:53:37 +0700] "GET /js/cab.youtube.js HTTP/1.1" 304 211 "http://cnweb/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22"
    pat ='(?P<domain>\w+):(?P<port>\d+) (?P<ip>\S+) - - \[(?P<date>[^\]]+)\] "(?P<method>\w+)\s+(?P<url>\S+)\s+(?P<http_version>[^"]+)" (?P<status_code>\d+) (?P<Content_length>\d+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)"'
    #pat
    #yield 1
    pat = re.compile(pat)
    f = open(path)
    for line in f:
        #print line
        #print line
        k = pat.match(line.strip())
        if k:
            yield k.groupdict()


def get_count(tup):
    return tup[1]


def save_to_file(my_dict, file_name):
    items = my_dict.items()
    sorted_items = sorted(items, key=get_count, reverse=True)
    f = open(file_name, 'w')
    f.write('[visited]  [url]\n')
    for key, val in sorted_items:
        f.write('[%s] %s\n' % (str(val).rjust(7), key))

    f.close()


def rank_by_visit(log_file='apache2.log', out_file='ranked.out'):
    """Rank site by visited"""

    passed_url = {}  # map contain all passed link
    for parsed_line in get_all_success_links(log_file):
        #print parsed_line['domain'], parsed_line['url']
        link = urlparse.urljoin('http://' + parsed_line['domain'],
                                parsed_line['url'])  # get url
        #rank only page success status_code == 200
        #or status_code == 304 ('not modified')
        status_code = int(parsed_line['status_code'])
        if status_code == '200' or status_code == 304:
            if not link in passed_url:
                passed_url[link] = 1
            else:
                passed_url[link] += 1

    save_to_file(passed_url, out_file)


def main():
    rank_by_visit()

if __name__ == '__main__':
    main()
