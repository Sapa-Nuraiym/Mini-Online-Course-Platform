-- Тест пайдаланушылары
INSERT OR IGNORE INTO users (username, email, password_hash, role) VALUES
('teacher1', 'teacher1@test.com', 'hashed_password_1', 'teacher'),
('student1', 'student1@test.com', 'hashed_password_2', 'student'),
('student2', 'student2@test.com', 'hashed_password_3', 'student');

-- Тест курстары
INSERT OR IGNORE INTO courses (user_id, title, description, category) VALUES
(1, 'Python негіздері', 'Python бастаушыларға арналған курс', 'Бағдарламалау'),
(1, 'Flask арқылы Backend', 'Flask фреймворкін нөлден үйрену', 'Бағдарламалау'),
(1, 'Git және GitHub', 'Нұсқаларды басқару жүйесін үйрену', 'Құралдар'),
(1, 'Ағылшын тілі — Beginner', 'Ағылшын тілін нөлден бастап үйрену', 'Тіл үйрену'),
(1, 'Математика негіздері', 'Алгебра және геометрия негіздері', 'Математика'),
(1, 'Графикалық дизайн', 'Canva және Figma арқылы дизайн жасау', 'Дизайн');

-- Тест сабақтары (YouTube видеолармен)
INSERT OR IGNORE INTO lessons (course_id, title, content, video_url, order_num) VALUES
(1, '1-сабақ: Python орнату', 'Python орнату және баптау жолдары', 'https://www.youtube.com/embed/rfscVS0vtbw', 1),
(1, '2-сабақ: Айнымалылар', 'Python айнымалылары және деректер түрлері', 'https://www.youtube.com/embed/khKv-8q7YmY', 2),
(1, '3-сабақ: Шарттар', 'If-else шарттары', 'https://www.youtube.com/embed/DZwmZ8Usvnk', 3),
(2, '1-сабақ: Flask орнату', 'Flask орнату және Hello World', 'https://www.youtube.com/embed/Z1RJmh_OqeA', 1),
(2, '2-сабақ: Маршруттар', 'Flask routes және templates', 'https://www.youtube.com/embed/Qr4QMBUPxWo', 2),
(3, '1-сабақ: Git орнату', 'Git орнату және баптау', 'https://www.youtube.com/embed/RGOj5yH7evk', 1);