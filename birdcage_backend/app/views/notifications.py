from flask import Blueprint, request, jsonify
from app.models.notifications import NotificationService, NotificationAssignment
from app.decorators import admin_required

notifications_blueprint = Blueprint('notifications', __name__)




# Get all of the notification services and URLs from notification_services
@notifications_blueprint.route('/api/services', methods=['GET'])
def get_notification_services():
    notification_services = NotificationService.select().dicts()
    return jsonify(list(notification_services))


# Set the URL for a notification service from notification_services
@notifications_blueprint.route('/api/services/<service_name>', methods=['PUT'])
@admin_required
def set_notification_service_url(service_name):
    service_url = request.json.get('service_url', '')
    service = NotificationService.get_or_none(NotificationService.service_name == service_name)
    if service:
        service.service_url = service_url
        service.save()

    return jsonify({'result': 'success', 'message': 'Service URL updated'})


# Get all of the detection actions and associated notification services from notification_assignments
@notifications_blueprint.route('/api/assignments', methods=['GET'])
def get_detection_assignments():
    assignments = NotificationAssignment.select().dicts()
    return jsonify(list(assignments))


# Add a specified notification service for a particular detection action in notification_assignments
@notifications_blueprint.route('/api/assignments', methods=['POST'])
@admin_required
def add_detection_assignment():
    detection_action = request.json.get('detection_action')
    notification_service = request.json.get('notification_service')

    if not detection_action or not notification_service:
        return jsonify({'result': 'error', 'message': 'Missing detection_action or notification_service'})

    NotificationAssignment.replace(detectionaction=detection_action, notification_service=notification_service).execute()

    return jsonify({'result': 'success', 'message': 'Detection assignment added'})


# Remove a specified notification service for a particular detection action in notification_assignments
@notifications_blueprint.route('/api/assignments', methods=['DELETE'])
@admin_required
def remove_detection_assignment():
    detection_action = request.json.get('detection_action')
    notification_service = request.json.get('notification_service')

    if not detection_action or not notification_service:
        return jsonify({'result': 'error', 'message': 'Missing detection_action or notification_service'})

    NotificationAssignment.delete().where(NotificationAssignment.detectionaction == detection_action,
                                            NotificationAssignment.notification_service == notification_service).execute()

    return jsonify({'result': 'success', 'message': 'Detection assignment removed'})
