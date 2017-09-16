
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database import Category, Base, Item
 
#engine = create_engine('postgresql+psycopg2://catalog:udacity@localhost/catalog')
engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

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

category1 = Category(name="Snowboarding", picture="https://static.pexels.com/photos/376697/pexels-photo-376697.jpeg")
session.add(category1)
session.commit()

item1 = Item(name="Goggles", description="High performance anti-fog and UV400 protection - The X4 ski goggles featured with double lens made of solid PC material which came with unique lagopus anti-fogging treatment and 100% UV400 protection that cuts the glare.", category_id=category1.id)
session.add(item1)
session.commit()
item2 = Item(name="Snowboard", description="The Timeless is a snowboard guaranteed to live up to it's name! Built around the strongest core System has, the 3D Core with Edgelock is full tip to tail poplar with high density stringers running just outside the center of the board as well as down each rail, easily driving and holding your edge in to any snow conditions! Then an artisan grade heartwood stringer is set in the center of the board creating explosive power and response from the park to big mountain carves!", category_id=category1.id)
session.add(item2)
session.commit()
item3 = Item(name="Helmet", description="Hybrid design with molded EPS foam, generous ventilation and highly adjustable suspension system", category_id=category1.id)
session.add(item3)
session.commit()
item4 = Item(name="Boots", description="Leather-and-nubuck. Traditional lacing. Foundation Unilite outsole", category_id=category1.id)
session.add(item4)
session.commit()
item5 = Item(name="Snow Board Bags", description="Waterproof - It is waterproof and keep your stuff dry even when the bag fell in the water. Ultra Light - Its ultra light weight makes it very convenient to carry on while camping, hiking or fishing. Durable - Made of high density PVC laminated fabric, tough and health. Easy to use - Just roll the top down a few times and snap the side release buckles together", category_id=category1.id)
session.add(item5)
session.commit()


category2 = Category(name="Soccer", picture="https://static.pexels.com/photos/47730/the-ball-stadion-football-the-pitch-47730.jpeg")
session.add(category2)
session.commit()


item6 = Item(name="Soccer Ball", description="Machine stitched construction and internal nylon wound carcass for maximum durability and long-lasting performance", category_id=category2.id)
session.add(item6)
session.commit()
item7 = Item(name="Rebounder", description="Practice different soccer techniques like trapping, heading, volleying, ground ball and pass accuracy", category_id=category2.id)
session.add(item7)
session.commit()
item8 = Item(name="Agility Ladder", description="Enhance your overall endurance, speed and stamina with this Ohuhu? Agility Ladder before or after your next workout. ", category_id=category2.id)
session.add(item8)
session.commit()
item9 = Item(name="Goalkeeper Gloves", description="PLAY LIKE THE PROS: The KixGK goalkeeper gloves have been available in the UK under the 1GK name for over a decade. Worn by many pros, now available in the U.S.", category_id=category2.id)
session.add(item9)
session.commit()



category3 = Category(name="Basketball", picture="https://static.pexels.com/photos/264258/pexels-photo-264258.jpeg")
session.add(category3)
session.commit()

item10 = Item(name="Basket Ball", description="Pro Game Ball with environmental rubber middle type, which is the dedicated high-end tire for Wilson. Used for NCAA League training as for its good impact resistance (up to 13,000 times) & flexibility & high quality standards", category_id=category3.id)
session.add(item10)
session.commit()
item11 = Item(name="Sneakers", description="High-style hi tops with a hoops history. These girls' kicks are inspired by basketball shoes. Shiny metallic details and leopard-print underlays add modern glam.", category_id=category3.id)
session.add(item11)
session.commit()


category4 = Category(name="Baseball", picture="https://static.pexels.com/photos/257970/pexels-photo-257970.jpeg")
session.add(category4)
session.commit()

item12 = Item(name="Baseball", description="Practice and play like the pros with a high-performing baseball made to the exact specifications of Major League Baseball. Hone your pitching, batting, catching, and throwing skills comfortably and effectively. The composite cork and rubber center is designed for ultimate durability and rigidity for optimal performance. The inner windings maximize shape retention, shock absorption, and provide for great flight control.", category_id=category4.id)
session.add(item12)
session.commit()
item13 = Item(name="Strike Zone Target", description="The strike zone target makes this an ideal throwing, pitching and fielding trainer for youth baseball and softball players, but especially for pitchers.", category_id=category4.id)
session.add(item13)
session.commit()
item14 = Item(name="Agility Ladder", description="Enhance your overall endurance, speed and stamina with this Ohuhu? Agility Ladder before or after your next workout. ", category_id=category4.id)
session.add(item14)
session.commit()


category5 = Category(name="Golf", picture="https://static.pexels.com/photos/54123/pexels-photo-54123.jpeg")
session.add(category5)
session.commit()


category6 = Category(name="Skateboarding", picture="https://static.pexels.com/photos/469970/pexels-photo-469970.jpeg")
session.add(category6)
session.commit()
item15 = Item(name="Pads", description="This protective gear set is specially designed to offer you perfect protection for skateboard, roller blading, riding a scooter, bicycle and many other outdoor sports.", category_id=category6.id)
session.add(item15)
session.commit()


category7 = Category(name="Football", picture="https://static.pexels.com/photos/4198/field-sport-ball-america.jpg")
session.add(category7)
session.commit()

item16 = Item(name="Tackling Dummy", description="Designed to take the toughest abuse and provide better control during contact drills. It features three reinforced heavy-duty handles for long-lasting performance and a secure hold. Perfect for football, soccer, basketball, kickboxing, mixed martial arts and military training, this tackling dummy can help increase athlete strength and stamina.", category_id=category7.id)
session.add(item16)
session.commit()
item17 = Item(name="Football", description="Wilson is the Official Football of the NFL. The Wilson NFL MVP ball features exclusive Wilson tackified PVC material with deeper pebble and firmer texture and a multi-layered lining for better shape and durability. The 3-ply bladder also provides better air retention and moisture control.", category_id=category7.id)
session.add(item17)
session.commit()

