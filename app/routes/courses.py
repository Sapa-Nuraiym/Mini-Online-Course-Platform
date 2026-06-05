from flask import Blueprint, request, jsonify
from app import db
from app.models import Course

courses_bp = Blueprint('courses', __name__)

def validate_course_data(data):
    errors = []
    if not data.get('title') or len(data.get('title', '').strip()) == 0:
        errors.append('Курс атауы міндетті')
    if len(data.get('title', '')) > 200:
        errors.append('Курс атауы 200 символдан аспауы керек')
    if not data.get('user_id'):
        errors.append('user_id міндетті')
    if data.get('category') and len(data.get('category', '')) > 100:
        errors.append('Санат 100 символдан аспауы керек')
    return errors

@courses_bp.route('/courses', methods=['GET'])
def get_courses():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

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

@courses_bp.route('/courses', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON деректер жіберілмеді'}), 400

    errors = validate_course_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    course = Course(
        title=data['title'].strip(),
        description=data.get('description', '').strip(),
        category=data.get('category', '').strip(),
        user_id=data['user_id']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Курс жасалды', 'id': course.id}), 201

@courses_bp.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс табылмады'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON деректер жіберілмеді'}), 400

    errors = validate_course_data(data)
    if errors:
        return jsonify({'errors': errors}), 400

    course.title = data.get('title', course.title).strip()
    course.description = data.get('description', course.description)
    course.category = data.get('category', course.category)

    db.session.commit()
    return jsonify({'message': 'Курс жаңартылды'})

@courses_bp.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс табылмады'}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Курс өшірілді'})
from app.models import Lesson

@courses_bp.route('/courses/<int:id>/lessons', methods=['GET'])
def get_lessons(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': 'Курс табылмады'}), 404
    lessons = Lesson.query.filter_by(course_id=id).order_by(Lesson.order_num).all()
    return jsonify([{
        'id': l.id,
        'title': l.title,
        'content': l.content,
        'video_url': l.video_url,
        'order_num': l.order_num
    } for l in lessons])