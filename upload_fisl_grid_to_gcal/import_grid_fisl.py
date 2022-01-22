#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Software em Domínio Público

import sys
import time
import atom
import re

from xml.etree import ElementTree

import gdata.calendar.service
import gdata.calendar

def time_convert(localtime):
    return time.gmtime(time.mktime(localtime + (0,0,0,-1)))

def parse_grid(filename):
    events = []

    re_day = re.compile("^<h2>([0-9]+) de Abril</h2>$")
    re_time = re.compile("^<h3>([0-9]+):([0-9]+)/([0-9]+):([0-9]+)</h3>$")
    re_title = re.compile("^<strong><em>(.*)</em></strong>$")
    re_location = re.compile("^<br/> <strong>Sala:</strong> (.*)")
    re_author = re.compile("^<br/> (.*)")

    in_grid = False
    day = 0
    timeslot = [0,0,0,0]
    event = {}
    authors = []

    page = open(filename)
    for line in page:
        striped = line.strip()
        if 'Abril' in line:
            day = int(re_day.match(striped).groups()[0])
            continue

        if striped.startswith('<h3>'):
            timeslot = [ int(x) for x in re_time.match(striped).groups() ]
            in_grid = True
            continue

        if 'Trilha' in striped and in_grid:
            continue # ignore

        if striped.startswith('<strong><em>') and in_grid:
            title = re_title.match(striped).groups()[0].strip()
            continue

        if striped.startswith('<br/> <strong>Sala:') and in_grid:
            location = re_location.match(striped).groups()[0].strip()
            continue

        if striped.startswith('<br/> ') and '</em>' not in striped and in_grid:
            try:
                authors.append(re_author.match(striped).groups()[0])
            except AttributeError:
                pass


        if striped.startswith('</div>') and in_grid:
            event['title'] = title
            event['authors'] = ', '.join(authors)
            event['location'] = location
            event['start'] = (2008, 04, day, timeslot[0], timeslot[1])
            event['end']   = (2008, 04, day, timeslot[2], timeslot[3])
            events.append(event)
            event = {}
            authors = []

    page.close()


    return events

def import_to_gcal(events):
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = 'usuario do gmail'
    calendar_service.password = 'sua_senha'
    calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
    calendar_service.ProgrammaticLogin()

    calendars_feed = calendar_service.GetAllCalendarsFeed()

    try:
        fisl_calendar = [ cal for cal in calendars_feed.entry if 'FISL' in cal.title.text ][0]
    except IndexError, e:
        print >>sys.etderr, "Nenhum calendário do FISL"
        sys.exit(1)

    url = fisl_calendar.GetAlternateLink().href

    for event in events:
        cal_event = gdata.calendar.CalendarEventEntry()
        cal_event.title = atom.Title(text=event['title'])
        cal_event.where.append(gdata.calendar.Where(value_string=event['location']))
        start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time_convert(event['start']))
        end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time_convert(event['end']))
        cal_event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))

        new_event = calendar_service.InsertEvent(cal_event, url)

if __name__ == "__main__":
    # index.html file == http://fisl.softwarelivre.org/9.0/papers/pub/programacao?print=1
    import_to_gcal(parse_grid("index.html"))

