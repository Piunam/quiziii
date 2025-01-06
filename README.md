# quiziii
A dynamic Django-based quiz app for creating, managing, and attempting quizzes. Features include categories, scoring, user stats, real-time results, and a responsive design for educational or fun purposes. and many more features to come..........


difference in admin and custom_admin
Default Admin (/admin/):

Standard Django admin interface
Basic CRUD operations for your models
Default styling and layout
Basic filtering and search capabilities
No custom dashboard

Custom Admin (/quiz-admin/):

All features of default admin PLUS:
Custom dashboard with statistics:

Total quizzes count
Total questions count
Recent quizzes list
Most popular quizzes
Quiz difficulty distribution


Custom badges for difficulty levels
Customized headers and titles
Special route for dashboard view (/quiz-admin/dashboard/)