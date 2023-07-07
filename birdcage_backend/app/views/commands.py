from flask import Blueprint, request, jsonify
from app.models.commands import Command
from app.decorators import admin_required

commands_blueprint = Blueprint('commands', __name__)



@commands_blueprint.route('/api/command/<command_name>', methods=['GET'])
def get_command(command_name):
    command = Command.get_or_none(Command.name == command_name)
    if command:
        return jsonify(command.to_dict())
    else:
        return jsonify({'error': 'Command not found'}), 404


@commands_blueprint.route('/api/command/<command_name>', methods=['PUT'])
@admin_required
def set_command_value(command_name):
    if 'value' not in request.json:
        return jsonify({'error': 'Value not provided'}), 400

    value = request.json['value']

    command, created = Command.get_or_create(name=command_name, defaults={'value': value})

    return jsonify({'success': True, 'name': command_name, 'value': value})
