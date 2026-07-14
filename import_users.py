import pandas as pd

from werkzeug.security import generate_password_hash

from app import app
from models import db, User

with app.app_context():

    df = pd.read_excel("users.xlsx")

    for _, row in df.iterrows():

        # اگر قبلاً وجود داشت ردش کن
        if User.query.filter_by(username=row["username"]).first():
            continue

        user = User(
            username=row["username"],
            password=generate_password_hash(str(row["password"])),
            marketer=row["full_name"]
        )

        db.session.add(user)

    db.session.commit()

print("همه کاربران ثبت شدند.")