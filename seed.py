from random import randint, choice as rc
from faker import Faker
from models import db, Hero, Power, hero_powers
from app import app

fake = Faker()

with app.app_context():
    Hero.query.delete()
    Power.query.delete()

    heroes = []
    for i in range(50):
        hero = Hero(
          name= fake.name(),
          super_name = fake.first_name(),  
        )
        heroes.append(hero)
    db.session.add_all(heroes)

    powers = []
    for i in range(50):
        power = Power(
            name = fake.name(),
            description = fake.paragraph()
        )
        powers.append(power)
    db.session.add_all(powers)

    combinations = set()
    strengths = ["Strong", "Weak", "Average"]
    for _ in range(50):
        hero_id = randint(1, 50)
        power_id = randint(1, 50)
        strength = rc(strengths)

        if (hero_id, power_id, strength) in combinations:
            continue
        combinations.add((hero_id, power_id, strength))
        hero_power_data = {"hero_id": hero_id, "power_id": power_id, "strength": strength}
        statement = db.insert(hero_powers).values(hero_power_data)
        db.session.execute(statement)
        db.session.commit()
    db.session.commit()