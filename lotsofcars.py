from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Make, Base, Model, User

engine = create_engine('sqlite:///carmake.db')
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

# Create original user
User1 = User(name="Zecl", email="zeclarcheage@gmail.com",
             picture='https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e2390bfa-7403-4119-bdcf-35a3e9fe9734/dd4m3if-c0582c7d-2920-4a1d-b831-f0c15500563e.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2UyMzkwYmZhLTc0MDMtNDExOS1iZGNmLTM1YTNlOWZlOTczNFwvZGQ0bTNpZi1jMDU4MmM3ZC0yOTIwLTRhMWQtYjgzMS1mMGMxNTUwMDU2M2UucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.dbYMbxkWzUTdswv0FnBx4SdhcNajCony-Rp5kJtMXmQ')
session.add(User1)
session.commit()

#Acura Car Make

make1 = Make(user_id=1, name='Acura', description='Acura is the American luxury vehicle marque of Japanese automaker Honda. The brand was launched in the United States and Canada on 27 March 1986, marketing luxury, performance, and high-performance vehicles.', image='https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/acura-logo-eva-sartiyem.jpg')

session.add(make1)
session.commit()

modelCar1 = Model(user_id=1, name='ILX', description='Meticulously-crafted with a stunning new A-Spec variant, this powerfully-styled premium sport sedan features an aggressive exterior re-design, along with a beautiful interior wrapped in Milano Leather and Ultrasuede trim. Inside and out, the ILX was tailor made for you.', price='$25,900',
                image='https://www.acura.com/-/media/Acura-Platform/Vehicle-Pages/ILX/2019/overview-page/Hero-and-Parallax/03-showroom/ILX_2019_Quick_On_Its_Feet_M.jpg', make=make1)

session.add(modelCar1)
session.commit()

modelCar2 = Model(user_id=1, name='TLX', description='With so many premium features, the 2020 Acura TLX is the best sport sedan for those who like to have it all.',
                price='33,000', image='https://www.acura.com/-/media/Acura-Platform/Vehicle-Pages/TLX/2020/overview-page-b/07-packages/2020_TLX_packages_A-Spec-Package_M.jpg', make=make1)

session.add(modelCar2)
session.commit()

modelCar3 = Model(user_id=1, name='RLX', description='Engineered to thrill in more ways than one, the 2019 RLX is performance personified. Available in 377-HP66 Sport Hybrid SH-AWD with 7-Speed DCT, or discover the 310-HP83 Precision All-Wheel Steer with 10-Speed Automatic Transmission.',
                price='$54,900', image='https://www.acura.com/-/media/Acura-Platform/Vehicle-Pages/RLX/2019/gallery-page/05-2019-acura-rlx-gallery-exterior-sport-hybrid-m.jpg', make=make1)

session.add(modelCar3)
session.commit()

modelCar4 = Model(user_id=1, name='RDX', description='The all new Acura RDX is redesigned, more luxurious, and even more thrilling to drive. Everything we ever imagined and then some.',
                price='$37,400', image='https://www.acura.com/-/media/Acura-Platform/Vehicle-Pages/RDX/2019/gallery-page/exterior/05-gallery-rdx-2019-aspec-white-diamond-pearl-showing-agressive-rear-led-taillights-M.jpg', make=make1)

session.add(modelCar4)
session.commit()

modelCar5 = Model(user_id=1, name='MDX', description='The 2019 Acura MDX is ready for the challenge. We designed the MDX around your lifestyle, no wonder it is the best-selling third-row luxury SUV of all time.',
                price='$44,300', image='https://www.acura.com/-/media/Acura-Platform/Vehicle-Pages/MDX/2019/overview-page/03_Gallery/02-gallery-MDX-2019-Advance-M.jpg', make=make1)

session.add(modelCar5)
session.commit()

modelCar6 = Model(user_id=1, name='NSX', description='THAT FEELING OF EMOTIONAL CONNECTEDNESS reflects both the power of dreams and driven creativity that fuels the craft of engineering. Reignited in a new generation of engineers, that connection brought forth a new vision, to honor the lineage by creating a boldly evolved NSX for a new century.',
                price='$157,500', image='https://de3mk53z3elpo.cloudfront.net/explorer/assets/desktop/chapters/1-NSX/01_Ratings-Section/2019-Acura-NSX-Ratings-Thermal-Orange-Pearl-ocean-background-Medium2x.jpg', make=make1)

session.add(modelCar6)
session.commit()


#Lexus Car Make

make2 = Make(user_id=1, name='Lexus', description="Lexus is the luxury vehicle division of the Japanese automaker Toyota. The Lexus brand is marketed in more than 70 countries and territories worldwide and has become Japan's largest-selling make of premium cars. It has ranked among the 10 largest Japanese global brands in market value.", image="https://i.pinimg.com/originals/b2/fd/61/b2fd615300a58b51d019203625e99c26.jpg")
session.add(make2)
session.commit()

modelCar1 = Model(user_id=1, name='IS', description='Bold design is just one way the IS 300 stands apart. With a turbocharger designed in-house, it provides robust power, low-end torque and responsive performance you can feel the moment you accelerate.',
                price="$38,310", image="https://www.lexus.com/cm-img/shared/gallery/2017/IS/Lexus-IS-atomic-silver-exterior-gallery-overlay-1204x677-LEX-ISG-MY17-0063.jpg", make=make2)
session.add(modelCar1)
session.commit()

modelCar2 = Model(user_id=1, name='ES', description="Entirely new from the ground up, the ES 350 features a longer, wider stance and a sleek, coupe-like silhouette inherited from the flagship LS. With first-of-its-kind technology and a more powerful engine, this is the most advanced ES ever.", 
                price="$39,600", image="https://www.lexus.com/cm-img/gallery/2019/ES/Lexus-ES-eshshowninnebulagraypearl-gallery-overlay-1204x677-LEX-ESH-MY19-0033-05_M75.jpg", make=make2)
session.add(modelCar2)
session.commit()

modelCar3 = Model(user_id=1, name='UX', description='From its smart size to its agile performance and best-in-class turning radius,* every aspect of the first-ever Lexus compact crossover was crafted for exploration.',
                price="$32,000", image="https://www.lexus.com/cm-img/gallery/2019/UX/Lexus-UXH-cadmium-orange-gallery-overlay-1204x677-LEX-UXH-MY19-0022-03_M75.jpg", make=make2)
session.add(modelCar3)
session.commit()

modelCar4 = Model(user_id=1, name='RC F', description='Pushing design and performance to new extremes, the RC F now features bolder styling and the most powerful Lexus V8 to date, as well as a new Launch Control* system for lightning-fast acceleration off the line.',
                price="$64,750", image="https://www.lexus.com/cm-img/gallery/2020/RCF/base/Lexus-RCF-gallery-overlay-1204x677-LEX-RCF-MY20-0016_M75.jpg", make=make2)
session.add(modelCar4)
session.commit()

modelCar5 = Model(user_id=1, name='LC HYBRID', description='Experience a profound shift in hybrid performance. A breakthrough Lexus Multistage Hybrid Drive, a 4.7- second 0-to-60 time* and a multistage transmission deliver the instant torque and response to put the entire category on notice.',
                price="$96,810", image="https://www.lexus.com/cm-img/shared/gallery/2018/LC/Lexus-LC-caviar-gallery-overlay-1204x677-LEX-LC5-MY18-0009.jpg", make=make2)
session.add(modelCar5)
session.commit()

#Honda Car Make

make3 = Make(user_id=1, name='Honda', description="Honda Motor Company, Ltd. is a Japanese public multinational conglomerate corporation primarily known as a manufacturer of automobiles, aircraft, motorcycles, and power equipment.", image="https://wallpapercave.com/wp/71LhuCZ.jpg")
session.add(make3)
session.commit()

modelCar1 = Model(user_id=1, name='Civic', description='Settle in and relax. The spacious interior seats five, offers plenty of cargo space and is designed with your comfort in mind. Plus, intuitive instrument displays and an available 60/40 split fold-down rear seatback make your life easier on the go.',
                price="$19,450", image="https://automobiles.honda.com/-/media/Honda-Automobiles/Vehicles/2019/Civic-Sedan/00-NEW-VLP/Exterior/0-Ext-Overview/MY19-CIVIC-SEDAN-transfer-EXTERIOR-Overview-1400-2x.jpg", make=make3)
session.add(modelCar1)
session.commit()

modelCar2 = Model(user_id=1, name='Accord', description='For nine generations, the fun-to-drive Accord has consistently brought the automotive mainstream unforeseen levels of technology, fuel-efficiency, safety and reliability.',
                price="23,720", image="https://blogmedia.dealerfire.com/wp-content/uploads/sites/680/2018/11/What-Colors-Does-the-2019-Honda-Accord-Come-in-a_o.jpg", make=make3)
session.add(modelCar2)
session.commit()

modelCar3 = Model(user_id=1, name='Fit', description='A small car with big attitude, the Honda Fit is the right mix of modern sport styling and aerodynamic efficiency.',
                price="$16,190", image="https://automobiles.honda.com/-/media/Honda-Automobiles/Vehicles/2019/Fit/00-NEW-VLP/Exterior/Overview/MY19-fit-transfer-ext-blade-overview-1400-2x.jpg", make=make3)
session.add(modelCar3)
session.commit()

modelCar4 = Model(user_id=1, name='Pilot', description='The eight-passenger 2019 Honda Pilot is a midsize SUV that is offered in five primary trim levels: LX, EX, EX-L, Touring and Elite. All models are powered by a 3.5-liter V6 (280 horsepower, 262 pound-feet of torque).',
                price="$31,450", image="https://st.motortrend.com/uploads/sites/5/2018/08/2019-Honda-Pilot-front-three-quarter-in-motion-2.jpg", make=make3)
session.add(modelCar4)
session.commit()

#Mercdes-Benz Car Make

make4 = Make(user_id=1, name='Mercedes-Benz', description="Mercdes-Benz is a German global automobile marque and a division of Daimler AG. The brand is known for luxury vehicles, buses, coaches, and trucks.", image="https://www.hdwallpaper.nu/wp-content/uploads/2015/12/Mercedes_Logo_10-995x498.jpg")
session.add(make4)
session.commit()

modelCar1 = Model(user_id=1, name='A-Class', description='A is for advanced. With the new Mercedes-Benz User Experience (MBUX), the A-Class drives a new generation of user-friendly tech. Quite possibly the most capable, natural and intuitive speech interface from any automaker, it is easy to learn because it learns you.',
                price="$32,500", image="https://www.mbusa.com/content/dam/mb-nafta/us/myco/my19/a/sedan/class-page/2019-A-SEDAN-CATEGORY-HERO-2-1-DR.jpg", make=make4)
session.add(modelCar1)
session.commit()

modelCar2 = Model(user_id=1, name='C-Class', description='The C-Class wraps countless technological advances in even more seductive style for 2019. New lower body styling, wheel choices,and all-LED lighting highlight its athletically elegant shape. Its acclaimed cabin brings new dimensions of enjoyment.',
                price="$41,400", image="https://www.mbusa.com/content/dam/mb-nafta/us/myco/my19/c/sedan/class-page/non-amg/2019-C-SEDAN-CATEGORY-HERO-2-1-DR.jpg", make=make4)
session.add(modelCar2)
session.commit()

modelCar3 = Model(user_id=1, name='GLE SUV', description='The luxury SUV that started the segment once again leads the way. Roomier, with a 3-inch-longer wheelbase, it is also more agile and aerodynamic. And from LED headlamps to a bold yet elegant cabin, it wraps first-in-class tech in finely tailored style.',
                price="$56,200", image="https://www.mbusa.com/content/dam/mb-nafta/us/myco/my20/gle/suv/class-page/non-amg/2020-GLE-SUV-CATEGORY-HERO-3-1-DR.jpg", make=make4)
session.add(modelCar3)
session.commit()

modelCar4 = Model(user_id=1, name='AMG GT', description='If the Mercedes-AMG GT is a reinvention of the pure sports car, there is only one way to make it even purer, open it up. With the new GT roadsters, the handcrafted AMG performance that is born on the track has been unleashed into an open sky.',
                price="$124,700", image="https://assets.mbusa.com/vcm/MB/DigitalAssets/Vehicles/ClassLanding/2018/GT/RDS/CATEGORY/HEADER/2018-AMG-GT-ROADSTER-CATEGORY-HERO-4-1-DR.jpg", make=make4)
session.add(modelCar4)
session.commit()

print ("added makes and models!!!")