import os
import os.path as op
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import RenderTemplateWidget


# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


# Create models
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))


# Create submodel A
class SubLocationA(db.Model):
    __tablename__ = 'sublocations_a'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    main_location = db.relationship('Location', backref='sub_locations_a')
    main_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))


# Create submodel B
class SubLocationB(db.Model):
    __tablename__ = 'sublocations_b'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    main_location = db.relationship('Location', backref='sub_locations_b')
    main_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location_a = db.relationship('SubLocationA', backref='sub_sub_locations_b')
    location_a_id = db.Column(db.Integer, db.ForeignKey('sublocations_a.id'))


# This widget uses custom template for inline field list
class CustomInlineFieldListWidget(RenderTemplateWidget):
    def __init__(self):
        super(CustomInlineFieldListWidget, self).__init__('field_list.html')


# Customized admin interface
class CustomView(ModelView):
    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'


# Customized admin interface
class CustomViewA(ModelView):
    list_template = 'list.html'
    create_template = 'create_a.html'
    edit_template = 'edit.html'


class UserAdmin(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name', 'email')


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


@app.route('/api/look_up_b_locations_connected_to_a_locations', methods=['POST'])
def look_up_b_locations_connected_to_a_locations():
    # use a set in case the same b location is in multiple a locations to prevent duplicates
    b_location_list = set()
    a_location_list = json.loads(request.form['selected_a_locations'])
    for a_location_id in a_location_list:
        a_location = SubLocationA.query.get_or_404(a_location_id)
        for b_location in a_location.sub_sub_locations_b:
            b_location_list.add(str(b_location.id))
    return jsonify(list(b_location_list))



# Create admin with custom base template
admin = admin.Admin(app, 'Example: Layout-BS3', base_template='layout.html', template_mode='bootstrap3')

# Add views
admin.add_view(CustomViewA(Location, db.session))
admin.add_view(CustomView(SubLocationA, db.session))
admin.add_view(CustomView(SubLocationB, db.session))


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    db.drop_all()
    db.create_all()

    a = Location(name='name_main_1')
    b1 = SubLocationA(name='name_a_1', main_location=a)
    b2 = SubLocationA(name='name_a_2', main_location=a)
    c1 = SubLocationB(name='name_b_1', main_location=a, location_a=b1)
    c2 = SubLocationB(name='name_b_2', main_location=a, location_a=b1)
    c3 = SubLocationB(name='name_b_3', location_a=b2)

    for location in [a, b1, b2, c1, c2, c3]:
        db.session.add(location)

    db.session.commit()


app_dir = op.realpath(os.path.dirname(__file__))
database_path = op.join(app_dir, app.config['DATABASE_FILE'])

build_sample_db()

app.run(debug=True)
