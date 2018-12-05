from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from new_database_setup import Category, Base, Game, User

engine = create_engine('sqlite:///gameshop.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until session.commit().
session = DBSession()


# Create dummy user
User1 = User(name="Jasmin Shah", email="jasmin_shah@live.com",
             picture='https://i.imgur.com/UgzvzXJ.png')
session.add(User1)
session.commit()

# Games for Action Category
category1 = Category(user_id=1, name="Action")

session.add(category1)
session.commit()

game1 = Game(user_id=1, name="Grand Theft Auto V", description="Grand Theft "
             "Auto V is an action-adventure video game developed by Rockstar "
             "North and published by Rockstar Games. It was released in "
             "September 2013 for PlayStation 3 and Xbox 360, in November "
             "2014 for PlayStation 4 and Xbox One, and in April 2015 for "
             "Microsoft Windows.", price="$19.50", category=category1)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="Dota 2", description="Dota 2 is a multiplayer"
             "online battle arena video game developed and published by Valve"
             " Corporation. The game is a sequel to Defense of the Ancients",
             price="Free", category=category1)

session.add(game2)
session.commit()

game3 = Game(user_id=1, name="Counter-Strike Global Offensive",
             description="Counter-Strike: Global Offensive is a "
             "multiplayer first-person shooter video game developed "
             "by Hidden Path Entertainment and Valve Corporation.",
             price="Free", category=category1)

session.add(game3)
session.commit()

game4 = Game(user_id=1, name="PAYDAY 2", description="Payday 2 is a "
             "cooperative first-person shooter video game developed "
             "by Overkill Software and published by 505 Games. The game "
             "is a sequel to 2011's Payday: The Heist.", price="$4.99",
             category=category1)

session.add(game4)
session.commit()

game5 = Game(user_id=1, name="PLAYERUNKNOWN'S BATTLEGROUNDS",
             description="PLAYERUNKNOWN'S BATTLEGROUNDS is a battle royale "
             "shooter that pits 100 players against each other in a "
             "struggle for survival. Gather supplies and outwit your "
             "opponents to become the last person standing.",
             price="$29.99", category=category1)

session.add(game5)
session.commit()

game6 = Game(user_id=1, name="Rocket League", description="Soccer meets"
             "driving once again in the long-awaited, physics-based "
             "multiplayer-focused sequel to Supersonic Acrobatic Rocket-"
             "Powered Battle-Cars! Choose a variety of high-flying vehicles "
             "equipped with huge rocket boosters to score amazing aerial "
             "goals and pull-off incredible game-changing saves!",
             price="$9.99", category=category1)

session.add(game6)
session.commit()

game7 = Game(user_id=1, name="Tom Clancy's Rainbow Six Siege",
             description="Tom Clancy's Rainbow Six Siege is the latest "
             "installment of the acclaimed first-person shooter franchise "
             "developed by the renowned Ubisoft Montreal studio.",
             price="$10.49", category=category1)

session.add(game7)
session.commit()

game8 = Game(user_id=1, name="MONSTER HUNTER: WORLD",
             description="In Monster Hunter: World, the latest installment "
             "in the series, one can enjoy the ultimate hunting experience, "
             "using everything at your disposal to hunt monsters in a new "
             "world teeming with surprises and excitement.", price="$3.49",
             category=category1)

session.add(game8)
session.commit()

game9 = Game(user_id=1, name="ARK: Survival Evolved",
             description="Stranded on the shores of a mysterious island, you "
             "must learn to survive. Use your cunning to kill or tame the "
             "primal creatures roaming the land, and encounter other players "
             "to survive, dominate... and escape!", price="$5.99",
             category=category1)

session.add(game9)
session.commit()


# Games under Early Access Category
category2 = Category(user_id=1, name="Early Access")

session.add(category2)
session.commit()


game1 = Game(user_id=1, name="Slay the Spire", description="We fused card "
             "games and roguelikes together to make the best single player "
             "deckbuilder we could. Craft a unique deck, encounter bizarre "
             "creatures, discover relics of immense power, and Slay the "
             "Spire!", price="$11.99", category=category2)

session.add(game1)
session.commit()

game2 = Game(user_id=1, name="7 Days to Die",
             description="7 Days to Die is an open-world game that is a "
             "unique combination of first person shooter, survival horror, "
             "tower defense, and role-playing games. Play the definitive "
             "zombie survival sandbox RPG that came first. Navezgane awaits!",
             price="$25", category=category2)

session.add(game2)
session.commit()

game3 = Game(user_id=1, name="Factorio", description="Factorio is a game "
             "about building and creating automated factories to produce "
             "items of increasing complexity, within an infinite 2D world. "
             "Use your imagination to design your factory, combine simple "
             "elements into ingenious structures, and finally protect it "
             "from the creatures who don't really like you.", price="$25",
             category=category2)

session.add(game3)
session.commit()

game4 = Game(user_id=1, name="Oxygen Not Included",
             description="Oxygen Not Included is a space-colony simulation "
             "game. Deep inside an alien space rock your industrious crew "
             "will need to master science, overcome strange new lifeforms, "
             "and harness incredible space tech to survive, and thrive.",
             price="$12.49", category=category2)

session.add(game4)
session.commit()

game5 = Game(user_id=1, name="Universim",
             description="Jump straight into managing your own planets as you"
             " guide a civilization through the ages. Become the ultimate "
             "empire in The Universim, a new breed of God Game in "
             "development by Crytivo.", price="$22.49", category=category2)

session.add(game5)
session.commit()

game6 = Game(user_id=1, name="Ring of Elysium", description="Escape an "
             "astonishing disaster in Ring of Elysium, a battle royale "
             "shooter developed by Tencent Games.", price="$12.50",
             category=category2)

session.add(game6)
session.commit()


# Games under Adventure Category
category3 = Category(user_id=1, name="Adventure")

session.add(category3)
session.commit()


game1 = Game(user_id=1, name="No Man's Sky", description="No Man's Sky is "
             "a game about exploration and survival in an infinite "
             "procedurally generated universe.", price="$14.99",
             category=category3)

session.add(game1)
session.commit()

game2 = Game(user_id=1, name="Assassin's Creed Odyssey",
             description="Choose your fate in Assassin's Creed Odyssey. From "
             "outcast to living legend, embark on an odyssey to uncover the "
             "secrets of your past and change the fate of Ancient Greece.",
             price="$39.99", category=category3)

session.add(game2)
session.commit()

game3 = Game(user_id=1, name="The Witcher 3: Wild Hunt",
             description="Experience the epic conclusion to the story of "
             "professional monster slayer, witcher Geralt of Rivia. As war "
             "rages on throughout the Northern Realms, you take on the "
             "greatest contract of your life - tracking down the Child of "
             "Prophecy, a live weapon that can alter the shape of the world.",
             price="$14.99", category=category3)

session.add(game3)
session.commit()

game4 = Game(user_id=1, name="Far Cry 5", description="Welcome to Hope "
             "County, Montana, home to a fanatical doomsday cult known as "
             "Eden's Gate. Stand up to cult leader Joseph Seed and his "
             "siblings, the Heralds, to spark the fires of resistance and "
             "liberate the besieged community.", price="$29.99",
             category=category3)

session.add(game4)
session.commit()


# Games under Casual Category
category3 = Category(user_id=1, name="Casual")

session.add(category3)
session.commit()


game1 = Game(user_id=1, name="Cities: Skylines",
             description="Cities: Skylines is a modern take on the classic "
             "city simulation. The game introduces new game play elements to "
             "realize the thrill and hardships of creating and maintaining "
             "a real city whilst expanding on some well-established tropes "
             "of the city building experience.", price="$6.99",
             category=category3)

session.add(game1)
session.commit()

game2 = Game(user_id=1, name="Stardew Valley",
             description="You've inherited your grandfather's old farm plot "
             "in Stardew Valley. Armed with hand-me-down tools and a few "
             "coins, you set out to begin your new life. Can you learn to "
             "live off the land and turn these overgrown fields into a "
             "thriving home?", price="$13.99", category=category3)

session.add(game2)
session.commit()

game3 = Game(user_id=1, name="The Sims 3", description="In The Sims 3, "
             "you can let your fantasies run wild as you design your "
             "ideal world. Start with your Sim, refining each shape, color "
             "and personality trait until you get the precise person that "
             "pleases you. Design your dream home, but don't let a grid "
             "limit you; place, rotate and stack furniture and walls freely "
             "and to your heart's content.", price="$9.99",
             category=category3)

session.add(game3)
session.commit()

game4 = Game(user_id=1, name="Overcooked 2",
             description="Overcooked returns with a brand-new helping of "
             "chaotic cooking action! Journey back to the Onion Kingdom and "
             "assemble your team of chefs in classic couch co-op or online "
             "play for up to four players. Hold onto your aprons...it's time "
             "to save the world again!", price="$15.95", category=category1)

session.add(game4)
session.commit()

game5 = Game(user_id=1, name="Slime Rancher",
             description="Slime Rancher is the tale of Beatrix LeBeau, a "
             "plucky, young rancher who sets out for a life a thousand light "
             "years away from Earth on the 'Far, Far Range' where she tries "
             "her hand at making a living wrangling slimes.", price="$9.99",
             category=category3)

session.add(game5)
session.commit()


# Games under Indie Category
category4 = Category(user_id=1, name="Indie")

session.add(category4)
session.commit()

game1 = Game(user_id=1, name="Rust", description="The only aim in Rust is "
             "to survive. To do this you will need to overcome struggles "
             "such as hunger, thirst and cold. Build a fire. Build a shelter."
             " Kill animals for meat. Protect yourself from other players, "
             "and kill them for meat. Create alliances with other players "
             "and form a town. Do whatever it takes to survive.",
             price="$14.99", category=category4)

session.add(game1)
session.commit()


game2 = Game(user_id=1, name="No Man's Sky", description="No Man's Sky is "
             "a game about exploration and survival in an infinite "
             "procedurally generated universe.", price="$14.99",
             category=category4)

session.add(game2)
session.commit()

game3 = Game(user_id=1, name="Hellblade: Senua's Sacrifice",
             description="From the makers of Heavenly Sword, Enslaved: "
             "Odyssey to the West, and DmC: Devil May Cry, comes a warrior's "
             "brutal journey into myth and madness. Set in the Viking age, "
             "a broken Celtic warrior embarks on a haunting vision quest "
             "into Viking Hell to fight for the soul of her dead lover.",
             price="$13.99", category=category4)

session.add(game3)
session.commit()

game4 = Game(user_id=1, name="Hollow Knight", description="Forge your own "
             "path in Hollow Knight! An epic action adventure through a vast "
             "ruined kingdom of insects and heroes. Explore twisting caverns,"
             " battle tainted creatures and befriend bizarre bugs, all in a "
             "classic, hand-drawn 2D style.", price="$6.50",
             category=category4)

session.add(game4)
session.commit()


# Games under Massively Multiplayer Category
category5 = Category(user_id=1, name="Massively Multiplayer")

session.add(category5)
session.commit()


game1 = Game(user_id=1, name="ARK: Survival Evolved",
             description="Stranded on the shores of a mysterious island, you "
             "must learn to survive. Use your cunning to kill or tame the "
             "primal creatures roaming the land, and encounter other players "
             "to survive, dominate... and escape!", price="$5.99",
             category=category5)

session.add(game1)
session.commit()

game2 = Game(user_id=1, name="The Elder Scrolls Online",
             description="Join over 10 million players in the award-winning "
             "online multiplayer RPG and experience limitless adventure in a "
             "persistent Elder Scrolls world. Battle, craft, steal or explore"
             "and combine different types of equipment and abilities to "
             "create your own style of play. No game subscription required.",
             price="$9.99", category=category5)

session.add(game2)
session.commit()


print "All games added!"
