__author__ = 'icoz'

from app import app
from forms import RequestForm
from app.db import db, get_applications, get_hosts
from app.auth import login_required

from flask import request, render_template, session


@app.route('/')
def home():
    print(session)
    return render_template('home.html')


# test get info on flask-wtf forms
@app.route('/get_info2', methods=['GET', 'POST'])
@login_required
def get_info2():
    data = None
    form = RequestForm()
    if form.validate_on_submit():
        print('Form submitted')
        print('get-info: post', form.data)

        req = dict()
        sk = 0

        # HOST
        if form.host.data:
            if form.host_ie.data == 0:
                req['h'] = {'$in': form.host.data}
            else:
                req['h'] = {'$nin': form.host.data}

        # APPLICATION
        if form.application.data:
            if form.application_ie.data == 0:
                req['a'] = {'$in': form.application.data}
            else:
                req['a'] = {'$nin': form.application.data}

        # FACILITY
        if form.facility.data:
            if form.facility_ie.data == 0:
                req['f'] = {'$in': form.facility.data}
            else:
                req['f'] = {'$nin': form.facility.data}

        # PRIORITY
        if form.priority.data:
            if form.priority_ie.data == 0:
                req['p'] = {'$in': [i for i in form.priority.data]}
            else:
                req['p'] = {'$nin': [i for i in form.priority.data]}

        # DATEFROM
        if form.date_from.data:
            req['d'] = {'$gte': form.date_from.data}

        # DATETO
        if form.date_to.data:
            if 'd' in req:
                req['d']['$lte'] = form.date_to.data
            else:
                req['d'] = {'$lte': form.date_to.data}

        # RECORD PER PAGE - in find()

        # SORT - in find()

        # SEARCH STR
        if form.search_str.data:
            req['m'] = {'$regex': form.search_str.data}

        print(req)

        # multiple choice find or - db.messages.find( { $or: [{"h": 'serv 0'}, {"h":'serv 1'}] } )
        # multiple choice find in - db.messages.find( { h: { $in: ['serv 0','serv 1']}, p: {$in: [0,1]} })
        #info = db.messages.find(req).limit(form.records_per_page.data + sk).skip(sk).sort('d', form.sort_direction.data)
        info = db.messages.find(spec=req,
                                skip=sk,
                                limit=form.records_per_page.data,
                                sort=[('d', form.sort_direction.data)])

        data = [i for i in info]

    else:
        print('Form NO submitted')

    return render_template('request_form2.html', form=form, data=data)

@app.route('/get_info', methods=['GET', 'POST'])
@login_required
def get_info():
    hosts = get_hosts()
    apps = get_applications()
    data = None
    # app = None
    # host = None
    act = dict()
    if request.method == 'GET':
        print('get-info: get')
    else:
        if request.args.get('skip'):
            sk = request.args.get('skip')
        else:
            sk = 0
        print('get-info: post', request.form)
        host = request.form.get('host')
        app = request.form.get('app')
        prio = request.form.get('prio')
        regex = request.form.get('msg_regex')
        req = dict()
        if host:
            act['host'] = host
            req['h'] = host
        if app:
            act['app'] = app
            req['a'] = app
        if prio != '':
            prio = int(prio)
            act['prio'] = prio
            req['p'] = prio
        if regex:
            act['regex'] = regex
            req['m'] = {'$regex': regex}
        print(req)
        # if regex:
        #     info = db.messages.find({'h': host, 'a': app, 'm':{'$regex': regex}}).limit(100+sk).skip(sk)
        # else:
        #     info = db.messages.find({'h': host, 'a': app}).limit(100+sk).skip(sk)
        info = db.messages.find(req).limit(100 + sk).skip(sk)
        data = [i for i in info]
    return render_template('request_form.html', hosts=hosts, apps=apps, data=data, active=act)


@app.route('/json/servers/', methods=['GET', 'POST'])
def json_servers():
    if request.method == 'GET':
        return str(get_hosts())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return str([])
        # date_from = request.json['date_from']
        # date_to = request.json['date_to']
        # collections = db.dates.find({'date': {'$ge': date_from, '$le': date_to}}, {'coll_name': 1})


@app.route('/json/apps/', methods=['GET', 'POST'])
def json_apps():
    if request.method == 'GET':
        return str(get_applications())
        # info = db.messages.aggregate({'$distinct': {'d': 0}})
        # info = db['dates'].aggregate({'$match': {'d': {'$and': [{'$gte':1}, {'$lte': 1}]}}},
        #                              {'$group': {"_id": 'servers', 'servers': {'$addToSet': '$servers'}}})
    else:
        return str([])