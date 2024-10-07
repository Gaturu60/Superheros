from app import app, db, Hero, Power, HeroPower

def seed_data():
    with app.app_context():
        # Drop all tables if needed
        db.drop_all()  # Uncomment if you want to reset the database

        # Create all tables
        db.create_all()

        # Seed Heroes
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        db.session.bulk_save_objects(heroes)

        # Seed Powers
        powers = [
            Power(name="super strength", description="gives the wielder super-human strengths"),
            Power(name="flight", description="gives the wielder the ability to fly through the skies at supersonic speed"),
            Power(name="super human senses", description="allows the wielder to use her senses at a super-human level"),
            Power(name="elasticity", description="can stretch the human body to extreme lengths"),
        ]
        db.session.bulk_save_objects(powers)

        # Commit changes
        db.session.commit()

        # Seed HeroPowers (associating Heroes with Powers)
        hero_powers = [
            HeroPower(hero_id=1, power_id=2, strength="Strong"),  # Kamala Khan with flight
            HeroPower(hero_id=2, power_id=1, strength="Average"),  # Squirrel Girl with super strength
            HeroPower(hero_id=3, power_id=3, strength="Weak"),     # Spider-Gwen with super human senses
            HeroPower(hero_id=4, power_id=4, strength="Strong"),   # The Wasp with elasticity
            # Add more associations as needed
        ]
        db.session.bulk_save_objects(hero_powers)
        db.session.commit()

if __name__ == "__main__":
    seed_data()
