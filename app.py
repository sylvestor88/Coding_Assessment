#!flask/bin/python
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

groups = [];
users = [];


@app.route('/users', methods=['GET'])
def get_users():

    """ returns the list of users that exists,
        returns an empty list if no users exist"""

    return jsonify({'users': users})


@app.route('/users', methods=['POST'])
def create_user():

    """ creates a new user after validating the request body,
        an invalid request body results in an appropriate error code,
        throws 422 error if user with userid already exists """

    if not request.json or not 'userid' in request.json or not 'groups' in request.json:
        abort(400, {'errors': "Bad request from the client"});

    new_user = {
        'first_name': request.json.get('first_name', ""),
        'last_name': request.json.get('last_name', ""),
        'userid': request.json['userid'],
        'groups': request.json['groups']
    }

    for user in users:
        if user['userid'] == request.json['userid']:
            abort(422, {'errors': "User already exists"})

    if len(request.json['groups']) == 0:
        abort(400, {'errors': "No groups defined for the user"});

    user_groups = [group for group in request.json['groups']];
    for group in user_groups:
        if group not in groups:
            abort(400, {'errors': "Group in groups attribute does not exist"});

    users.append(new_user);
    return jsonify({'user': new_user}), 201


@app.route('/users/<string:id>', methods=['GET'])
def get_user(id):

    """ returns user details from the users list or
        results in 404 error if user does not exist"""

    user = [user for user in users if user['userid'] == id]
    if len(user) == 0:
        abort(404);
    return jsonify({'user': user[0]});


@app.route('/users/<string:id>', methods=['DELETE'])
def delete_user(id):

    """ deletes the given user from the users list or
        results in 404 error if user does not exist"""

    user = [user for user in users if user['userid'] == id]
    if len(user) == 0:
        abort(404, {'errors': "User does not exist"});
    users.remove(user[0])
    return jsonify({'result': 'User Deleted'})


@app.route('/users/<string:id>', methods=['PUT'])
def update_task(id):

    """ updates user details for the user in users lists or
        results in 404 error if user does not exist"""

    user = [user for user in users if user['userid'] == id]
    if len(user) == 0:
        abort(404, {'errors': "User does not exist"})
    if not request.json:
        abort(400, {'errors': "Bad request format from client"})
    if 'first_name' in request.json and type(request.json['first_name']) is not unicode:
        abort(400, {'errors': "Bad request format from client(first_name)"})
    if 'last_name' in request.json and type(request.json['last_name']) is not unicode:
        abort(400, {'errors': "Bad request format from client(last_name)"})
    if 'groups' in request.json and type(request.json['groups']) is not list:
        abort(400, {'errors': "Bad request format from client(groups)"})
    user[0]['first_name'] = request.json.get('first_name', user[0]['first_name'])
    user[0]['last_name'] = request.json.get('last_name', user[0]['last_name'])
    user[0]['groups'] = request.json.get('groups', user[0]['groups'])
    return jsonify({'user': user[0]})


@app.route('/groups', methods=['POST'])
def create_group():

    """ creates a group with valid the request body and adds it to the groups list,
        an invalid request body results in an appropriate error code,
        throws 422 error if group already exists """

    if not request.json:
        abort(400, {'errors': "Bad request format from client"});
    if not 'name' in request.json:
        abort(400, {'errors': "Request does not contain name attribute"});
    if request.json.get('name') == "":
        abort(400, {'errors': "Group name empty"});
    if request.json.get('name') in groups:
        abort(422, {'errors': "Group Already Exists"});
    else:
        groups.append(request.json.get('name'));
        return jsonify({'result': 'New Group named \"' + request.json.get('name') + '\" Created.'}), 201


@app.route('/groups', methods=['GET'])
def view_groups():

    """ returns the list of groups that exists,
        returns an empty list if no groups exist """

    return jsonify({'groups': groups});


@app.route('/groups/<string:gname>', methods=['GET'])
def get_groups(gname):

    """ returns list of userid's associated with a given group,
        results in 404 error if group does not exist """

    if gname not in groups:
        abort(404, {'errors': "Group with name " + gname + " does not exist"});
    group_users = [user['userid'] for user in users if gname in user['groups']]
    return jsonify({'users': group_users});


@app.route('/groups/<string:gname>', methods=['PUT'])
def update_group(gname):

    """ updates membership for list of users in the request body by adding
        the given group to the users groups attribute if not exists already, or
        results in 404 error if group does not exist"""

    if gname not in groups:
        abort(404, {'errors': "Group with name " + gname + " does not exist"});
    if not request.json:
        abort(400, {'errors': "Bad request format from client"});
    if 'members' not in request.json:
        abort(400, {'errors': "Request does not contain members attribute"});
    if not request.json.get('members'):
        abort(400, {'errors': "Users list is empty"});
    for userid in request.json.get('members'):
        user = [user for user in users if user['userid'] == userid]
        if len(user) != 0:
            if gname not in user[0]['groups']:
                user[0]['groups'].append(gname);
    return jsonify({'user': 'Users added to \"' + gname + '\" group'})


@app.route('/groups/<string:gname>', methods=['Delete'])
def delete_group(gname):

    """ deletes the given group from the groups list along
        with its reference in any of the users,
        results in 404 error if groups does not exist"""

    if gname not in groups:
        abort(404);
    for user in users:
        if gname in user['groups']:
            user['groups'].remove(gname);
    groups.remove(gname);
    return jsonify({'result': 'Group \"' + gname + '\" Deleted'})


if __name__ == '__main__':
    app.run(debug=True)