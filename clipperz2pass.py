#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Juhamatti Niemelä <iiska at iki.fi>. All Rights Reserved.
# Copyright (C) 2015 David A Roberts <d at vidr.cc>. All Rights Reserved.
# Copyright (C) 2016 Ashish Vijayaram <initrd at gmail.com>. All Rights Reserved.
# This file is licensed under the GPLv2+. Please see COPYING for more information.

import sys
import re

from subprocess import Popen, PIPE
import collections
import json

def space_to_camelcase(value):
    output = ""
    first_word_passed = False
    for word in value.split(" "):
        if not word:
            output += "_"
            continue
        if first_word_passed:
            output += word.capitalize()
        else:
            output += word.lower()
        first_word_passed = True
    return output

def cleanTitle(title):
    # make the title more command line friendly
    title = re.sub("(\\|\||\(|\)|/)", "-", title)
    title = re.sub("-$", "", title)
    title = re.sub("\@", "At", title)
    title = re.sub("'", "", title)
    return title

def path_for(card, path=''):
    """ Generate path name from elements title and current path """
    title_text = card.get('label')
    if title_text is None:
        title_text = ''
    title = cleanTitle(space_to_camelcase(title_text))
    return '/'.join([path, title])

def password_data(card):
    """ Return password data and additional info if available from
    password entry element. """
    fields = card['currentVersion']['fields'].values()
    notes = card['data']['notes']
    passwd = None
    for field in fields:
        if field['label'].lower() == 'password':
            passwd = field['value']
            break
    if passwd is None: # try harder
        for field in fields:
            if field['actionType'] == 'PASSWORD':
                passwd = field['value']
                break
    ret = passwd + "\n" if passwd else "\n"
    for field in fields:
        if field['value'] and field['value'] != passwd:
            label = field['label']
            if label == 'Web address':
                label = 'URL'
            if label == 'Username or email':
                label = 'Username'
            if notes:
                ret = "%s%s: %s\n\nNotes:\n%s\n" % (ret, label, field['value'], notes)
            else:
                ret = "%s%s: %s\n" % (ret, label, field['value'])
    return ret

def import_card(card, path=''):
    """ Import new password entry to password-store using pass insert
    command """
    print "Importing " + path_for(card, path)
    proc = Popen(['pass', 'insert', '--multiline', '--force',
                  path_for(card, path)],
              stdin=PIPE, stdout=PIPE)
    proc.communicate(password_data(card).encode('utf8'))
    proc.wait()


def main(json_file):
    """ Parse given Clipperz JSON file and import cards from it """
    with open(json_file,'r') as fp:
        for card in json.load(fp, object_pairs_hook=collections.OrderedDict):
            import_card(card, 'Cards')

if __name__ == '__main__':
    main(sys.argv[1])
