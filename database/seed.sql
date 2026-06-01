-- Тест пайдаланушылары
INSERT INTO users (username, email, password_hash, role) VALUES
('teacher1', 'teacher1@test.com', 'hashed_password_1', 'teacher'),
('student1', 'student1@test.com', 'hashed_password_2', 'student'),
('student2', 'student2@test.com', 'hashed_password_3', 'student');

-- Тест курстары
INSERT INTO courses (user_id, title, description, category) VALUES
(1, 'Python негіздері', 'Python бастаушыларға арналған курс', 'Бағдарламалау'),
(1, 'Flask арқылы Backend', 'Flask фреймворкін үйрену', 'Бағдарламалау'),
(1, 'Дерекқор негіздері', 'SQL және SQLite үйрену', 'Дерекқор');

-- Тест сабақтары
INSERT INTO lessons (course_id, title, content, order_num) VALUES
(1, '1-сабақ: Python орнату', 'Python орнату жолдары...', 1),
(1, '2-сабақ: Айнымалылар', 'Python айнымалылары...', 2),
(2, '1-сабақ: Flask орнату', 'Flask орнату жолдары...', 1);

-- Тест тіркелулері
INSERT INTO enrollments (user_id, course_id) VALUES
(2, 1),
(2, 2),
(3, 1);