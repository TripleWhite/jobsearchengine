from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # 检查管理员用户是否已存在
    admin = User.query.filter_by(email='admin@example.com').first()
    if not admin:
        admin = User(
            email='admin@example.com',
            name='Admin User',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
    else:
        print("Admin user already exists")

    # 创建测试用户
    test_user = User.query.filter_by(email='user@example.com').first()
    if not test_user:
        test_user = User(
            email='user@example.com',
            name='Test User',
            is_admin=False
        )
        test_user.set_password('user123')
        db.session.add(test_user)
        db.session.commit()
        print("Test user created successfully")
    else:
        print("Test user already exists")
