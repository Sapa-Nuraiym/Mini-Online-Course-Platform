from flask import Blueprint, request, jsonify
from app import db
from app.models import Course

courses_bp = Blueprint('courses', __name__)

# GET — барлық курстарды алу (іздеу және сүзгілеу)
@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    query = Course.query

    if search:
        query = query.filter(Course.title.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)

    courses = query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'description': c.description,
        'category': c.category,
        'user_id': c.user_id
    } for c in courses])

# GET — бір курсты алу
@courses_bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс табылмады'}), 404
    return jsonify({
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'category': course.category,
        'user_id': course.user_id
    })

# POST — жаңа курс жасау
@courses_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()

    # Валидация
    if not data.get('title'):
        return jsonify({'error': 'Курс атауы міндетті'}), 400
    if not data.get('user_id'):
        return jsonify({'error': 'user_id міндетті'}), 400

    course = Course(
        title=data['title'],
        description=data.get('description', ''),
        category=data.get('category', ''),
        user_id=data['user_id']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Курс жасалды', 'id': course.id}), 201

# PUT — курсты жаңарту
@courses_bp.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс табылмады'}), 404

    data = request.get_json()

    if not data.get('title'):
        return jsonify({'error': 'Курс атауы міндетті'}), 400

    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    course.category = data.get('category', course.category)

    db.session.commit()
    return jsonify({'message': 'Курс жаңартылды'})

# DELETE — курсты өшіру
@courses_bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс табылмады'}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Курс өшірілді'})