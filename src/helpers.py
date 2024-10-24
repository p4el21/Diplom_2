from faker import Faker

def generate_random_user():
    fake = Faker('ru_RU')
    user = {
        'email': fake.ascii_free_email(),
        'password': fake.password(),
        'name': fake.user_name()
    }
    return user