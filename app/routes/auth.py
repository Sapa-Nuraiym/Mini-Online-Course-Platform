from flask import Blueprint, request, jsonify, session
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Деректер жіберілмеді'}), 400

    errors = []
    if not data.get('username'):
        errors.append('Пайдаланушы аты міндетті')
    if not data.get('email') or '@' not in data.get('email', ''):
        errors.append('Email дұрыс емес')
    if not data.get('password') or len(data.get('password', '')) < 6:
        errors.append('Құпия сөз кемінде 6 символ болуы керек')
    if errors:
        return jsonify({'errors': errors}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Бұл email тіркелген'}), 400

    password_hash = bcrypt.generate_password_hash(
        data['password']
    ).decode('utf-8')

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role=data.get('role', 'student')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Тіркелу сәтті өтті',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Деректер жіберілмеді'}), 400

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email және құпия сөз міндетті'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Пайдаланушы табылмады'}), 404

    if not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Құпия сөз қате'}), 401

    session['user_id'] = user.id
    session['role'] = user.role

    return jsonify({
        'message': 'Кіру сәтті',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 200


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Шығу сәтті'}), 200


@auth_bp.route('/auth/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Авторизация жоқ'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Пайдаланушы табылмады'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200