from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Brand, Guitar, User

engine = create_engine('postgresql+psycopg2://catalog:test123@localhost:5432/guitars')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#default user
User1 = User(name="Default Dan", email="defaultDan@udacity.com")
session.add(User1)
session.commit()

#ESP
brand1 = Brand(user_id=1, name="ESP")
session.add(brand1)
session.commit()

#ESP Andromeda
Guitar1 = Guitar(user_id=1,
                 name="Arrow",
                 brand=brand1,
                 body_material="Alder",
                 neck_material="3Pc Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Seymour Duncan AHB-1",
                 bridge="Floyd Rose Original")

session.add(Guitar1)
session.commit()

#ESP Horizon-I
Guitar2 = Guitar(user_id=1,
                 name="Horizon-I",
                 brand=brand1,
                 body_material="Alder",
                 neck_material="3Pc maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Seymour Duncan Hot Rails/Distortion",
                 bridge="Floyd Rose Original")

session.add(Guitar2)
session.commit()

#ESP E-II HRF NT-8 Baritone
#8 string
Guitar3 = Guitar(user_id=1,
                 name="E-II HRF NT-8 Baritone",
                 brand=brand1,
                 body_material="Alder",
                 neck_material="3Pc Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="8",
                 scale_length="27",
                 pickups="EMG 81-8H",
                 bridge="Hipshot w/String Thru")

session.add(Guitar3)
session.commit()

#ESP E-II Stream G
Guitar4 = Guitar(user_id=1,
                 name="E-II Stream G",
                 brand=brand1,
                 body_material="Mahogany",
                 neck_material="3Pc Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="EMG 66/57 Brushed Black Chrome",
                 bridge="Tonepros Locking TOM& Gotoh Tailpiece")

session.add(Guitar4)
session.commit()

#ESP E-II Viper Bariton
Guitar5 = Guitar(user_id=1,
                 name="E-II Viper Baritone",
                 brand=brand1,
                 body_material="Mahogany",
                 neck_material="3Pc Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="27",
                 pickups="EMG 80/81",
                 bridge="Gotoh TOM & Tailpiece")

session.add(Guitar5)
session.commit()

#ESP E-II FRX
Guitar6 = Guitar(user_id=1,
                 name="FRX",
                 brand=brand1,
                 body_material="Mahogany",
                 neck_material="3Pc Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="EMG 89R/89",
                 bridge="Floyd Rose Original")

session.add(Guitar6)
session.commit()

brand2 = Brand(user_id=1, name="Gibson")
session.add(brand2)
session.commit()

#Gibson SG Dark 7
Guitar1 = Guitar(user_id=1,
                 name="SG Dark 7",
                 brand=brand2,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Richlite",
                 frets="24",
                 strings="7",
                 scale_length="24.75",
                 pickups="Seymour Duncan SH-1n/SH-4",
                 bridge="Tune-o-matic")

session.add(Guitar1)
session.commit()

#Gibson Explorer Faded 2016 Limited
Guitar2 = Guitar(user_id=1,
                 name="Explorer Faded 2016 Limited",
                 brand=brand2,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.75",
                 pickups="Dirty Fingers+",
                 bridge="Tune-o-matic")

session.add(Guitar2)
session.commit()

#Gibson Flying V Faded 2016 Limited
Guitar3 = Guitar(user_id=1,
                 name="Flying V Faded 2016 Limited",
                 brand=brand2,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.75",
                 pickups="Dirty Fingers+",
                 bridge="Tune-o-matic")

session.add(Guitar3)
session.commit()

#Gibson SG Supreme 2016 Limited
Guitar4 = Guitar(user_id=1,
                 name="SG Supreme 2016 Limited",
                 brand=brand2,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Composite",
                 frets="24",
                 strings="6",
                 scale_length="24.75",
                 pickups="Burstbucker Pro",
                 bridge="Tune-o-matic")

session.add(Guitar4)
session.commit()

#Gibson Firebird V 2016 T
Guitar5 = Guitar(user_id=1,
                 name="Firebird V 2016 T",
                 brand=brand2,
                 body_material="Mahogany",
                 neck_material="Mahogany/Walnut",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.75",
                 pickups="Traditional Firebird mini-humbuckers",
                 bridge="Tune-o-matic")

session.add(Guitar5)
session.commit()

#Gibson Les Paul '60s Tribute 2016 T
Guitar6 = Guitar(user_id=1,
                 name="Les Paul Studio Faded 2016 T",
                 brand=brand2,
                 body_material="Maple/Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.75",
                 pickups="BB Pro",
                 bridge="Tune-o-matic")

session.add(Guitar6)
session.commit()

brand3 = Brand(user_id=1, name="Jackson")
session.add(brand3)
session.commit()

#Jackson Pro Series Soloist SL7
Guitar1 = Guitar(user_id=1,
                 name="Pro Series Soloist SL7",
                 brand=brand3,
                 body_material="Mahogany",
                 neck_material="Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="7",
                 scale_length="25.5",
                 pickups="Seymour Duncan SH-6 7",
                 bridge="Floyd Rose FRT-SSO 2000 Double-Locking Tremolo")

session.add(Guitar1)
session.commit()

#Jackson Pro Series Rhoads RRT
Guitar2 = Guitar(user_id=1,
                 name="Pro Series Rhoads RRT",
                 brand=brand3,
                 body_material="Mahogany",
                 neck_material="Maple",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="7",
                 scale_length="25.5",
                 pickups="Seymour Duncan JB SH-4/SH2N",
                 bridge="Compensated and Adjustable Strings-Through")

session.add(Guitar2)
session.commit()

#Jackson Pro Series King V KV
Guitar3 = Guitar(user_id=1,
                 name="Pro Series King V KV",
                 brand=brand3,
                 body_material="Nato",
                 neck_material="Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Seymour Duncan SH6b/SH6n",
                 bridge="Floyd Rose FRT-o5000 Double Locking Tremolo")

session.add(Guitar3)
session.commit()

#X Series Kelly KEXM
Guitar4 = Guitar(user_id=1,
                 name="X Series Kelly KEXM",
                 brand=brand3,
                 body_material="Basswood",
                 neck_material="Maple",
                 fingerboard_material="Maple",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Jackson High Output Humbucking",
                 bridge="Floyd Rose Special Double-Locking Tremolo")

session.add(Guitar4)
session.commit()

#JS Series Warrior JS32T
Guitar5 = Guitar(user_id=1,
                 name="JS Series Warrior JS32T",
                 brand=brand3,
                 body_material="Basswood",
                 neck_material="Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Jackson High Output Humbucking",
                 bridge="Complensated and Adjustable Strings-Through")

session.add(Guitar5)
session.commit()

#USA Select B7MG
Guitar6 = Guitar(user_id=1,
                 name="USA Select B7MG",
                 brand=brand3,
                 body_material="Alder",
                 neck_material="Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="7",
                 scale_length="27",
                 pickups="EMG 81-7/707 Humbucking",
                 bridge="Jackson HT7 7-String Hardtail")

session.add(Guitar6)
session.commit()


brand4 = Brand(user_id=1, name="BCRich")
session.add(brand4)
session.commit()

#mk9 Warlock
Guitar1 = Guitar(user_id=1,
                 name="Mk9 Warlock",
                 brand=brand4,
                 body_material="Mahogany",
                 neck_material="Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="24.75",
                 pickups="High Output Humbuckers",
                 bridge="Quadramatic")

session.add(Guitar1)
session.commit()

#Mk7 Mockingbird
Guitar2 = Guitar(user_id=1,
                 name="Mk7 Mockingbird",
                 brand=brand4,
                 body_material="Mahogany",
                 neck_material="3Pc Mahogany",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="High Output Humbucker",
                 bridge="Floyd Rose Special")

session.add(Guitar2)
session.commit()

#Mk3 Villain
Guitar3 = Guitar(user_id=1,
                 name="Mk3 Villain",
                 brand=brand4,
                 body_material="Basswood",
                 neck_material="Hard Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="High Output Humbuckers",
                 bridge="BC Rich Double Locking Tremolo")

session.add(Guitar3)
session.commit()

#Mk3 Warbeast
Guitar4 = Guitar(user_id=1,
                 name="Mk3 Warbeast",
                 brand=brand4,
                 body_material="Basswood",
                 neck_material="Hard Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="High Output Pickups",
                 bridge="TOM Style, String Through")

session.add(Guitar4)
session.commit()

#Wk3 Jr. V
Guitar5 = Guitar(user_id=1,
                 name="Mk3 Jr V",
                 brand=brand4,
                 body_material="Basswood",
                 neck_material="Hard Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="24.75",
                 pickups="High Output Humbuckers",
                 bridge="BC Rich Double Locking Tremolo")

session.add(Guitar5)
session.commit()

#Mk1 Warlock 7 String
Guitar6 = Guitar(user_id=1,
                 name="Mk1 Warlock 7 String",
                 brand=brand4,
                 body_material="Basswood",
                 neck_material="Hard Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="7",
                 scale_length="25.5",
                 pickups="High Output Humbuckers",
                 bridge="Fixed Bridge")

session.add(Guitar6)
session.commit()

brand5 = Brand(user_id=1, name="Ibanez")
session.add(brand5)
session.commit()

#Ibanez RGIR38BFE
Guitar1 = Guitar(user_id=1,
                 name="RGIR38BFE",
                 brand=brand5,
                 body_material="Mahogany",
                 neck_material="Walnut",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="8",
                 scale_length="27",
                 pickups="EMG 808",
                 bridge="Gibraltar Standard II-8 Bridge")

session.add(Guitar1)
session.commit()

#Ibanez RGDIX6PB
Guitar2 = Guitar(user_id=1,
                 name="RGDIX6PB",
                 brand=brand5,
                 body_material="Poplar/Ash/Mahogany",
                 neck_material="Maple/Bubinga",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="26.5",
                 pickups="DiMarzio Fusion Edge",
                 bridge="Gibraltar Standard II")

session.add(Guitar2)
session.commit()

#Ibanez FTM33 WK
Guitar3 = Guitar(user_id=1,
                 name="FTM33 WK",
                 brand=brand5,
                 body_material="Ash",
                 neck_material="Maple/Walnut",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="8",
                 scale_length="27",
                 pickups="Lundgren Model M8P",
                 bridge="FX Edge-III-8 Bridge")

session.add(Guitar3)
session.commit()

#Ibanez AR2619
Guitar4 = Guitar(user_id=1,
                 name="AR2619",
                 brand=brand5,
                 body_material="Maple/Mahogany",
                 neck_material="3Pc Maple",
                 fingerboard_material="Ebony",
                 frets="24",
                 strings="6",
                 scale_length="24.7",
                 pickups="Super 80 Flying Finger",
                 bridge="Gibraltar bridge w/Sustain block")

session.add(Guitar4)
session.commit()

#TM1702M
Guitar5 = Guitar(user_id=1,
                 name="TM1702M",
                 brand=brand5,
                 body_material="Alder",
                 neck_material="Maple",
                 fingerboard_material="Maple",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Seymour Duncan Alnico II Pro",
                 bridge="IFX-PRO")

session.add(Guitar5)
session.commit()

#RC1320
Guitar6 = Guitar(user_id=1,
                 name="RC1320",
                 brand=brand5,
                 body_material="Mahogany",
                 neck_material="Maple",
                 fingerboard_material="Rosewood",
                 frets="24",
                 strings="6",
                 scale_length="25.5",
                 pickups="Seymour Duncan 59/JB",
                 bridge="Tight-Tune")

session.add(Guitar6)
session.commit()

brand6 = Brand(user_id=1, name="Dean")
session.add(brand6)
session.commit()

#Dean Cadillac 1980 3 Pickup
Guitar1 = Guitar(user_id=1,
                 name="Cadillac 1980 3 Pickup",
                 brand=brand6,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.75",
                 pickups="DMT Design",
                 bridge="Tune-o-matic")

session.add(Guitar1)
session.commit()

#Dean ML79 Floyd
Guitar2 = Guitar(user_id=1,
                 name="ML79 Floyd",
                 brand=brand6,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.75",
                 pickups="DMT Design",
                 bridge="Floyd Rose Special")

session.add(Guitar2)
session.commit()

#Dean V
Guitar3 = Guitar(user_id=1,
                 name="V",
                 brand=brand6,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Ebony",
                 frets="22",
                 strings="6",
                 scale_length="24.625",
                 pickups="USA DMT Time Capsule",
                 bridge="Tune-o-matic (String-thru)")

session.add(Guitar3)
session.commit()

#Dean USA Z
Guitar4 = Guitar(user_id=1,
                 name="USA Z",
                 brand=brand6,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Ebony",
                 frets="22",
                 strings="6",
                 scale_length="23.625",
                 pickups="DiMarzio Super Distortion CRCR",
                 bridge="Tune-o-matic")

session.add(Guitar4)
session.commit()

#Dean Gran Sport
Guitar5 = Guitar(user_id=1,
                 name="Gran Sport",
                 brand=brand6,
                 body_material="Mahogany",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.625",
                 pickups="DMT Series Nostalgia/Equalizer",
                 bridge="Tune-o-matic (hardtail)")

session.add(Guitar5)
session.commit()

#Dean Icon
Guitar6 = Guitar(user_id=1,
                 name="Icon",
                 brand=brand6,
                 body_material="Maple",
                 neck_material="Mahogany",
                 fingerboard_material="Rosewood",
                 frets="22",
                 strings="6",
                 scale_length="24.625",
                 pickups="DMT Series Nostalgia",
                 bridge="Tune-o-matic (hardtail)")

session.add(Guitar6)
session.commit()

print "Added Guitars and Brands!"
