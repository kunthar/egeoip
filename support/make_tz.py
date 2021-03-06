#!/usr/bin/env python
import sys

import pytz
import datetime

BASE_DATE = datetime.datetime(year=2009,month=1,day=1,
                              tzinfo=pytz.timezone('UTC'))

def main():
    cols = sys.stdin.readline().rstrip('\n').split('\t')
    rows = []
    print '%% @copyright 2010 Mochi Media, Inc.'
    print '%% @doc Autogenerated mapping of countries (and region) to'
    print '%%      standard time UTC offsets.'
    print '%%      Generated by ../support/make_tz.py'
    print '-module(egeoip_tz).'
    print '-export([utc_offset/1]).'
    print '-record(geoip, {country_code, country_code3, country_name, region,'
    print '    city, postal_code, latitude, longitude, area_code, dma_code}).'

    for line in sys.stdin:
        row = dict(zip(cols, line.rstrip('\n').split('\t')))
        try:
            tz = pytz.timezone(row['timezone'])
        except pytz.UnknownTimeZoneError:
            continue
        utcoffset = BASE_DATE.astimezone(tz).tzinfo.utcoffset(None)
        usecs = (utcoffset.days * 86400) + utcoffset.seconds
        if row['region']:
            rows.append(
                'utc_offset(#geoip{country_code = "%s", region = <<"%s">>}) -> %s' %
                (row['country'], row['region'], usecs))
        else:
            rows.append('utc_offset(#geoip{country_code = "%s"}) -> %s' %
                        (row['country'], usecs))
    rows.append('utc_offset(_) -> 0')
    print ';\n'.join(rows) + '.'

if __name__ == '__main__':
    main()
