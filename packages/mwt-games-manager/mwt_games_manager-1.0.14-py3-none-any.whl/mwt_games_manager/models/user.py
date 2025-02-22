class User:
    def __init__(self, username="", firstname="", lastname="", birth_date=None, signup_date=None, email="", password="",
                 verified=False, profile_picture_url="", role=None, **kwargs):
        # super().__init__(**kwargs)
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.birth_date = birth_date
        self.signup_date = signup_date
        self.email = email
        self.password = password
        self.verified = verified
        self.profile_picture_url = profile_picture_url
        self.role = role
