from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


# POST /api/auth/register — тіркелу
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON деректер жіберілмеді'}), 400

    errors = []
    if not data.get('username') or len(data.get('username', '').strip()) == 0:
        errors.append('Username міндетті')
    if not data.get('email') or '@' not in data.get('email', ''):
        errors.append('Email дұрыс форматта болуы керек')
    if not data.get('password') or len(data.get('password', '')) < 6:
        errors.append('Құпия сөз кемінде 6 символ болуы керек')
    if data.get('role') and data.get('role') not in ['teacher', 'student']:
        errors.append('Role тек teacher немесе student болуы керек')
    if errors:
        return jsonify({'errors': errors}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Бұл email бұрын тіркелген'}), 409

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Бұл username бұрын алынған'}), 409

    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = User(
        username=data['username'].strip(),
        email=data['email'].strip(),
        password_hash=password_hash,
        role=data.get('role', 'student')
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Тіркелу сәтті',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201


# POST /api/auth/login — кіру
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON деректер жіберілмеді'}), 400

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


# POST /api/auth/logout — шығу
@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Шығу сәтті'}), 200


# GET /api/auth/me — кім кірген
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