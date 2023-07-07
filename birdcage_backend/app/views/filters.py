from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.filters import FilterThresholds, SpeciessOverides
from app.models.preferences import UserPreferences
import requests
from app.decorators import admin_required

filters_blueprint = Blueprint('filters', __name__)


@filters_blueprint.route('/api/filters/birdsoftheweek', methods=['GET'])
def get_birds_of_the_week():

    #get the predicted birds of the week from BirdNET Analyzer and return to client
    url = 'http://birdcage_analyzer:8080/predictedspecies'

    preferences = UserPreferences.get_all_user_preferences(0)
    now = datetime.now()
    year, week_number, weekday = now.isocalendar()

    response = requests.get(url, params={
        'latitude': preferences['latitude'],
        'longitude': preferences['longitude'],
        'week_number': week_number,
        'locale': preferences['locale'],
        'sf_thresh': preferences['sf_thresh']
    })

    return response.json()


@filters_blueprint.route('/api/filters/thresholds/<int:user_id>', methods=['GET'])
def get_thresholds(user_id):
    
    thresholds = FilterThresholds.select().where(FilterThresholds.user_id == user_id).dicts()

    if len(thresholds):
        return jsonify(thresholds[0])
    else:
        return jsonify({"error": "User not found"}), 404


@filters_blueprint.route('/api/filters/thresholds/<int:user_id>', methods=['POST'])
@admin_required
def set_thresholds(user_id):
    try:
        ignore_threshold = float(request.form['ignore_threshold'])
        log_threshold = float(request.form['log_threshold'])
        recordalert_threshold = float(request.form['recordalert_threshold'])
    except ValueError:
        return jsonify({"error": "Invalid input"}), 400

    if not (0 <= ignore_threshold >= log_threshold >= recordalert_threshold >= 0 and ignore_threshold <= 1):
        return jsonify({"error": "Invalid threshold values"}), 400

    FilterThresholds.replace(user_id=user_id, ignore_threshold=ignore_threshold, log_threshold=log_threshold, recordalert_threshold=recordalert_threshold).execute()

    return jsonify({"success": "Thresholds updated"})


@filters_blueprint.route('/api/filters/overrides/<int:user_id>', methods=['GET'])
def get_overrides(user_id):
    overrides = SpeciessOverides.select().where(SpeciessOverides.user_id == user_id).dicts()

    return jsonify(list(overrides))


@filters_blueprint.route('/api/filters/overrides/<int:user_id>', methods=['POST', 'DELETE'])
@admin_required
def add_remove_override(user_id):
    species_name = request.form['species_name']


    if request.method == 'POST':
        override_type = request.form['override_type']
        if override_type not in ["ignore", "log", "record", "alert"]:
            return jsonify({"error": "Invalid override type"}), 400

        try:
            SpeciessOverides.create(user_id=user_id, species_name=species_name, override_type=override_type).save()
            return jsonify({"success": "Override added"})
        except SpeciessOverides.IntegrityError:
            return jsonify({"error": "Override already exists"}), 400

    elif request.method == 'DELETE':
        deleted = SpeciessOverides.delete().where(SpeciessOverides.user_id == user_id, SpeciessOverides.species_name == species_name).execute()

        if deleted > 0:
            return jsonify({"success": "Override removed"})
        else:
            return jsonify({"error": "Override not found"}), 404
