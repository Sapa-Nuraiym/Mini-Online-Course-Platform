from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
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

    password_hash = bcrypt.hashpw(
        data['password'].encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash,
        role=data.get('role', 'student')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Тіркелу сәтті', 'id': user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Деректер жіберілмеді'}), 400

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email және құпия сөз міндетті'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Пайдаланушы табылмады'}), 404

    if not bcrypt.checkpw(data['password'].encode('utf-8'),
                          user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Құпия сөз қате'}), 401

    return jsonify({
        'message': 'Кіру сәтті',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })