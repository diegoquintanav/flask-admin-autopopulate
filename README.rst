This example shows how to implement a button that assists the creation of relationships, and is based on `this example  <https://github.com/flask-admin/flask-admin/tree/master/examples/layout_bootstrap3>`_.

The problem that attempts to solve is reviewed in https://stackoverflow.com/questions/50661791/add-buttons-that-populate-other-fields-in-built-in-templates-of-flask-admin?noredirect=1#comment88342923_50661791

This is done by overriding some of the built-in templates.

To run this example:

1. Clone the repository::

    git clone https://github.com/diegoquintanav/flask-admin-autopopulate
    cd flask-admin-autopopulate

2. Create and activate a virtual environment::

    virtualenv env
    source env/bin/activate

3. Install requirements::

    pip install -r requirements.txt

4. Run the application::

    python app.py

