import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from bot.db.models.user import User
from bot.db.models.item import Toy, WeaponMod, ArmourMod
from bot.db.models.inventory import UserToy, UserWeaponMod, UserArmourMod
from bot.db.connection import get_db, initialise_db_connection


class TestInventoryModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialise_db_connection(':memory:')
        cls.db = get_db()

    def setUp(self):
        self.db.execute('BEGIN')

    def tearDown(self):
        self.db.execute('ROLLBACK')

    def test_user_toy_creation(self):
        user = User(twitch_username='testuser')
        user.save()

        toy = Toy(name='Test Toy', cost=100)
        toy.save()

        user_toy = UserToy(
            user_id=user.id,
            toy_id=toy.id,
            date_acquired=datetime.now().isoformat()
        )
        user_toy.save()

        retrieved_user_toy = UserToy.get_by_id(user_toy.id)
        self.assertEqual(retrieved_user_toy.user_id, user.id)
        self.assertEqual(retrieved_user_toy.toy_id, toy.id)

    def test_weapon_mod_creation(self):
        user = User(twitch_username='testuser')
        user.save()

        weapon_mod = WeaponMod(name='Sharp Mod', cost=50, adjective='Sharp')
        weapon_mod.save()

        user_weapon_mod = UserWeaponMod(
            user_id=user.id,
            mod_id=weapon_mod.id,
            date_applied=datetime.now().isoformat()
        )
        user_weapon_mod.save()

        retrieved_weapon_mod = UserWeaponMod.get_by_id(user_weapon_mod.id)
        self.assertEqual(retrieved_weapon_mod.user_id, user.id)
        self.assertEqual(retrieved_weapon_mod.mod_id, weapon_mod.id)

    def test_armour_mod_creation(self):
        user = User(twitch_username='testuser')
        user.save()

        armour_mod = ArmourMod(name='Padded Mod', cost=50, adjective='Padded')
        armour_mod.save()

        user_armour_mod = UserArmourMod(
            user_id=user.id,
            mod_id=armour_mod.id,
            date_applied=datetime.now().isoformat()
        )
        user_armour_mod.save()

        retrieved_armour_mod = UserArmourMod.get_by_id(user_armour_mod.id)
        self.assertEqual(retrieved_armour_mod.user_id, user.id)
        self.assertEqual(retrieved_armour_mod.mod_id, armour_mod.id)

    def test_unique_constraint(self):
        user = User(twitch_username='testuser')
        user.save()

        weapon_mod = WeaponMod(name='Unique Mod', cost=50, adjective='Unique')
        weapon_mod.save()

        user_weapon_mod = UserWeaponMod(
            user_id=user.id,
            mod_id=weapon_mod.id,
            date_applied=datetime.now().isoformat()
        )
        user_weapon_mod.save()

        with self.assertRaises(Exception):
            duplicate_user_weapon_mod = UserWeaponMod(
                user_id=user.id,
                mod_id=weapon_mod.id,
                date_applied=datetime.now().isoformat()
            )
            duplicate_user_weapon_mod.save()

    def test_relationships(self):
        user = User(twitch_username='testuser')
        user.save()

        toy = Toy(name='Test Toy', cost=100)
        toy.save()

        user_toy = UserToy(
            user_id=user.id,
            toy_id=toy.id,
            date_acquired=datetime.now().isoformat()
        )
        user_toy.save()

        user_toys = user.toys
        self.assertTrue(any(ut.toy_id == toy.id for ut in user_toys))

    def test_deletion(self):
        user = User(twitch_username='testuser')
        user.save()

        toy = Toy(name='Deletable Toy', cost=100)
        toy.save()

        user_toy = UserToy(
            user_id=user.id,
            toy_id=toy.id,
            date_acquired=datetime.now().isoformat()
        )
        user_toy.save()

        user_toy.delete()

        with self.assertRaises(Exception):
            UserToy.get_by_id(user_toy.id)


if __name__ == '__main__':
    unittest.main()