/*MEMBERSHIP TABLE*/
DROP TABLE IF EXISTS memberships;

CREATE TABLE memberships
(
    membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);

INSERT INTO memberships (name, price)
VALUES
    ('1 Day Pass', 15),
    ('Monthly Membership', 50),
    ('3 Month Membership', 120),
    ('6 Month Membership', 230),
    ('1 Year Membership', 450);

/*PERSONAL TRAINER TABLE*/
DROP TABLE IF EXISTS pts;

CREATE TABLE pts
(
    pt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    description TEXT
);

INSERT INTO pts (name, price, description)
VALUES
    ('Brandon', 30, 'Speacialises in fat loss and endurance training'),
    ('Mathew', 25, 'Speacialises in muscle growth and fat loss'),
    ('Abigail', 35, 'Speacialises in endurance and high intesity interval training'),
    ('Steven', 30, 'Speacialises in strength and muscle growth training'),
    ('Courtney', 25, 'Speacialises in fat loss and strength training');

/*CLASSES TABLE*/
DROP TABLE IF EXISTS classes;

CREATE TABLE classes
(
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

INSERT INTO classes (name, description)
VALUES
    ('Hot Yoga', 'A hot yoga class is a type of yoga practice performed in a heated room, typically ranging from 90°F to 105°F (32°C to 40°C). 
                During the class, participants perform a series of yoga poses and sequences, often accompanied by controlled breathing exercises, 
                in the heated environment. The heat helps to increase flexibility, promote detoxification through sweating, and enhance 
                cardiovascular endurance. Hot yoga classes can vary in intensity and style, but they generally offer a challenging yet invigorating 
                workout that promotes physical and mental well-being.'),
    ('Crazy Circuits', 'A crazy circuit class is an energetic and dynamic workout session designed to challenge the body and elevate fitness 
                levels. In this class, participants typically move through a series of high-intensity circuit exercises that target 
                different muscle groups, combining elements of strength training, cardiovascular conditioning, and functional movements. 
                The workouts often involve a variety of equipment such as dumbbells, kettlebells, resistance bands, and bodyweight 
                exercises. The circuit format keeps the workout engaging and fast-paced, with short intervals of intense exercise 
                followed by brief rest periods. Crazy circuit classes are suitable for individuals looking to improve overall strength, 
                endurance, and agility while burning calories and boosting metabolism.'),
    ('HIIT and Run', 'An HIIT (High-Intensity Interval Training) and Run class is a dynamic and intense workout session that combines elements 
                of running with high-intensity interval training exercises. Participants alternate between bursts of high-intensity 
                cardio activities, such as sprinting or running at maximum effort, and periods of active recovery or rest. The intervals 
                are typically short, ranging from 30 seconds to a few minutes, and can be adjusted to accommodate different fitness 
                levels. HIIT and Run classes are designed to maximize calorie burn, improve cardiovascular fitness, and enhance endurance. 
                They offer a challenging yet effective way to boost metabolism, increase stamina, and achieve overall fitness goals.'),
    ('Spinning', 'A spinning class is an indoor cycling workout that takes place on stationary bikes. Led by a certified instructor, 
                participants pedal through a series of simulated terrain, including hills, sprints, and flat roads, all set to motivating music. 
                The intensity of the workout can be adjusted using the bikes resistance knob, allowing participants of all fitness levels to tailor 
                the workout to their needs. Spinning classes provide a high-energy, low-impact cardiovascular workout that strengthens the legs, 
                improves endurance, and burns calories. With its dynamic and engaging format, spinning is a popular choice for individuals looking 
                to boost fitness levels while enjoying a fun and challenging workout.'),
    ('Strength and Size', 'A strength and size class is a structured workout session designed to build muscle mass and increase overall strength. 
                Typically led by a qualified instructor, the class focuses on resistance training exercises using a variety of equipment 
                such as barbells, dumbbells, and resistance machines. Participants perform a series of compound movements targeting major 
                muscle groups, including exercises like squats, deadlifts, bench presses, and rows. The workouts are designed to 
                challenge the muscles to adapt and grow, with emphasis on progressive overload and proper form. Strength and size 
                classes are suitable for individuals looking to increase muscle mass, improve muscular strength, and sculpt their 
                physique in a supportive group setting.');

/*CLASS TIME TABLE*/
DROP TABLE IF EXISTS classtimes;

CREATE TABLE classtimes
(
    class_time_id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT NOT NULL,
    time TEXT,
    time2 TEXT
);

INSERT INTO classtimes (day, time, time2)
VALUES
    ('Tuesdays', '9:00', '18:00'),
    ('Mondays', '7:00', '16:00'),
    ('Fridays', '8:00', '19:00'),
    ('Wednesdays', '9:00', '17:00'),
    ('Thursdays', '8:00', '16:00');


/*USERS TABLE*/
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

/*ADMIN TABLE*/
DROP TABLE IF EXISTS admin;

CREATE TABLE admin
(
    admin_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

INSERT INTO admin (user_id)
VALUES
    ('admin')

SELECT * FROM admin

/*CHECKOUT TABLE*/
/*USERS TABLE*/
DROP TABLE IF EXISTS checkout;

CREATE TABLE checkout
(
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);