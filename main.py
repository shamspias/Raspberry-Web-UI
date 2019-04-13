from flask import Blueprint, render_template, Flask
from flask_login import login_required, current_user

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

