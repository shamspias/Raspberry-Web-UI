from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import User, EntryInfo
main = Blueprint(name='main', import_name=__name__)


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


####################

import datetime
from .lib.cors import crossdomain
from .lib.setup import rooms, settings
from .lib.appliance import Appliance


def updateStates(rooms):
    for i, room in enumerate(rooms):
        for j, appliance in enumerate(room['Appliances']):
            current_appliance = Appliance(appliance)
            rooms[i]['Appliances'][j]['State'] = current_appliance.getState()
    return rooms


@main.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)


@main.route("/controlroom")
@login_required
def controlroom():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %I:%M %p")
    templateData = {
        'time': timeString,
        'rooms': updateStates(rooms),
        'refresh_rate': settings['RefreshRate'] * 1000
    }
    return render_template('controlroom.html', **templateData)


@main.route("/grid/")
@login_required
@crossdomain(origin='*')
def grid():
    templateData = {
        'rooms': updateStates(rooms)
    }
    return render_template('grid.html', **templateData)


@main.route("/button/<int:room_index>/<int:appliance_index>/<int:statuss>")
@login_required
@crossdomain(origin='*')
def button(room_index, appliance_index, statuss):
    appliance = Appliance(rooms[room_index]['Appliances'][appliance_index])
    appliance.executeAction()
    appliance.setState(statuss)
    templateData = {
        'state': appliance.getState(),
        'room_index': room_index,
        'appliance_index': appliance_index,
        'name': appliance.name
    }
    return render_template('button.html', **templateData)


from .lib import sensors


@main.route("/sensors/")
@login_required
def sensor():
    pias = {
        'pir': sensors.pirS()
    }
    return render_template('sensors.html', **pias)


from .lib import qrcodesstem, doorSystem

@main.route("/door/")
@login_required
def door():
    datamain = qrcodesstem.doorLockSystem()
    user1 = User.query.filter_by(email=datamain).first()

    if user1:
        doorSystem.doorOpen()
        dorja = 1
        entryList = EntryInfo(door_entry_time=datetime.datetime.now(), user_name=user1.name)
        db.session.add(entryList)
        db.session.commit()
    else:
        dorja = 0
    data = {
        'dor': dorja,
        'dorinfo': "Welcome To Home"
    }
    return render_template('door.html', **data)

@main.route("/door/close")
@login_required
def doorclose():
    doorSystem.doorClose()
    return render_template('home.html')

@main.route("/door/open")
@login_required
def dooropen():
    doorSystem.doorOpen()
    return render_template('home.html')
    

@main.route("/entry/")
@login_required
def entry():
    info = EntryInfo.query.all()
    return render_template('entryinfo.html', data=info)
