-- Disable foreign keys temporarily
SET session_replication_role = 'replica';

-- Create user table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL,
    profile VARCHAR(180) NOT NULL
);

-- Insert user data
INSERT INTO "user" (id, name, username, email, password, profile)
VALUES (1, 'Admin', 'admin', 'admin@gmail.com', '$2b$12$kRDd2FhkhkMyeQz3AACm.uAvwZZ6bT8otBRVfYfQtGJ7AxZAnxW5u', 'profile.jpg');

-- Create brand table
CREATE TABLE brand (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert brand data
INSERT INTO brand (id, name) VALUES
(1, 'Mercedes-Benz'),
(2, 'BMW'),
(3, 'Hyundai'),
(4, 'VinFast'),
(5, 'Toyota'),
(6, 'Mazda'),
(7, 'Porsche'),
(8, 'Maserati'),
(9, 'Ferrari'),
(10, 'Volvo'),
(11, 'Ford');

-- Create category table
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Insert category data
INSERT INTO category (id, name) VALUES
(1, 'SUVs & Cars'),
(2, 'Trucks & Vans'),
(3, 'Electric & Hybrid'),
(4, 'Performance Vehicles'),
(5, 'Commercial Vehicles'),
(6, 'Future Vehicles');

-- Create addproduct table
CREATE TABLE addproduct (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    price FLOAT NOT NULL,
    discount INTEGER,
    stock INTEGER NOT NULL,
    colors TEXT NOT NULL,
    "desc" TEXT NOT NULL,
    pub_date TIMESTAMP NOT NULL,
    category_id INTEGER NOT NULL REFERENCES category(id),
    brand_id INTEGER NOT NULL REFERENCES brand(id),
    image_1 VARCHAR(150) NOT NULL,
    image_2 VARCHAR(150) NOT NULL,
    image_3 VARCHAR(150) NOT NULL
);

-- Insert product data
INSERT INTO addproduct (id, name, price, discount, stock, colors, "desc", pub_date, category_id, brand_id, image_1, image_2, image_3) VALUES
(1, 'Leg Fill', 53057.68, 10, 63, 'suffer,network,western,model', 'Improve defense from face feeling cup according enough. Arrive just read. Entire final letter important wrong. Their want later fund under no.', '2025-04-16 09:55:26.939368', 3, 7, '6087936f269e938141d8.jpg', '442600ddf49cb192c2de.jpg', '231ea7f1e5d63d08ec19.jpg'),
(2, 'Yard Trip ad', 71592.62, 6, 198, 'health,happy,base,world', 'Push follow people free local. Career treatment green past. Use clear south remember every.', '2025-04-16 09:55:26.939368', 5, 6, 'cf113762b63b10f46c9d.jpg', '97803489a0c0ecbaf718.jpg', '4c5450a6d82c0d8757e7.jpg'),
(3, 'Find Experience', 35312.06, 12, 196, 'home,grow,serious,thing', 'Allow public ability nearly black feel pattern. Economic forget gun explain player authority evidence. About myself before their born so.', '2025-04-16 09:55:26.939368', 6, 8, 'a027fd5477bfc573026b.jpg', '4dc33e62c4ad05ec5c2f.jpg', 'a6c03254f5aebc2a8a5a.jpg'),
(4, 'Worker Across', 16395.98, 19, 183, 'peace,which,central,young', 'Cut event itself center serve seek politics. Speech head key sing record life do west. Whole avoid land seven catch rule.', '2025-04-16 09:55:26.939368', 6, 8, '97803489a0c0ecbaf718.jpg', '0a8ee4f03596d8c718cd.jpg', '6f564bf7019eac59624c.jpg'),
(5, 'Production Represent', 115466.87, 7, 50, 'me,easy,past,center', 'Sign case station hit task force travel mean. Page avoid discuss. Network security performance store approach rise. Their dream politics hair big card camera.', '2025-04-16 09:55:26.939368', 6, 2, 'dd68f1362bb883d5b07a.jpg', '95f19d2825ccef699c03.jpg', 'f5e6ecd7e42686c0778a.jpg'),
(6, 'Toward Year', 24135.85, 6, 95, 'look,agree,expert,throughout', 'Affect front around style body loss many institution. Store college beautiful charge wife. Technology go about I. World concern war. Student experience matter thus collection without follow.', '2025-04-16 09:55:26.939368', 4, 7, 'fb04a80207d2678dcc0b.jpg', '6f564bf7019eac59624c.jpg', '4dc33e62c4ad05ec5c2f.jpg'),
(7, 'Ford Spend Middle', 133570.97, 28, 41, 'from,computer,according,prepare', 'Answer might bit stand test. Official main my popular brother. Cell table set its. Kid drop know east their executive lot staff.', '2025-04-16 09:55:26.939368', 6, 11, '1fbe657b69ffaf8de518.jpg', '0a8ee4f03596d8c718cd.jpg', '07a607800d78dc7531d4.jpg'),
(8, 'Past Daughter', 10795.56, 4, 106, 'former,she,many,Democrat', 'Argue east involve treatment. Sound development him religious. Involve movie talk must day cover social. Letter cause conference choose talk could population. Nation security couple whole now defense clearly company.', '2025-04-16 09:55:26.939368', 3, 7, '5151330859710dd6a79d.jpg', 'f5e6ecd7e42686c0778a.jpg', '6087936f269e938141d8.jpg'),
(9, 'Network Away', 192354.65, 14, 162, 'assume,section,young,smile', 'Chance society crime you movie. Must recently follow next director. Firm Mrs administration partner society.', '2025-04-16 09:55:26.939368', 6, 11, '04082518fa5c76589af9.jpg', '7cb3adfa78ab4f8c2914.jpg', '8592f5f4c127ecf56856.jpg'),
(10, 'Place Trade', 45240.90, 9, 187, 'high,pretty,executive,forget', 'Worker air just range. Free service actually prevent agent travel air. Indicate speech scientist culture carry. Fill against race month almost they main. Bill account game should voice forget. Could open south employee write fly later.', '2025-04-16 09:55:26.939368', 5, 11, '6087936f269e938141d8.jpg', 'a6c03254f5aebc2a8a5a.jpg', '8592f5f4c127ecf56856.jpg'),
(11, 'Relate Note', 122286.44, 17, 32, 'every,government,movement,under', 'Choose coach lead surface between. Nothing term then stand model difficult expect. Tough discuss site call general. Treatment senior per off.', '2025-04-16 09:55:26.939368', 4, 11, '0a8ee4f03596d8c718cd.jpg', 'eb48e0616d9a0f746b58.jpg', '7cb3adfa78ab4f8c2914.jpg'),
(12, 'Believe Others', 178612.67, 17, 27, 'beautiful,cup,also,large', 'Crime receive medical him country show high film. Camera section activity laugh garden nor part. Possible rule sort even agency quickly fish. Here conference measure than home school behind.', '2025-04-16 09:55:26.939368', 2, 5, '231ea7f1e5d63d08ec19.jpg', 'a6c03254f5aebc2a8a5a.jpg', 'c12aa95d1323b596776d.jpg'),
(13, 'Public Meet', 36925.88, 9, 194, 'budget,consider,tree,benefit', 'Officer low decision same. International laugh similar entire hold learn. Identify whatever yard name color right improve follow. Goal next travel figure them.', '2025-04-16 09:55:26.939368', 5, 10, '95f19d2825ccef699c03.jpg', '7b4eb498899b37f49bd8.jpg', 'cf113762b63b10f46c9d.jpg'),
(14, 'Ford Rest Mrs', 190564.43, 10, 73, 'beautiful,situation,consider,challenge', 'Under small truth blue. Heart through of say play environmental discover. Network store where truth PM party general.', '2025-04-16 09:55:26.939368', 6, 11, 'cf113762b63b10f46c9d.jpg', '402c1efe2e6d9fad8122.jpg', 'adca7ce25746d4e562fc.jpg'),
(15, 'Machine Treat', 12557.70, 2, 147, 'sign,pressure,it,natural', 'Myself boy again citizen bring. Always over identify same purpose huge Mrs. Degree sign mother since buy interest.', '2025-04-16 09:55:26.939368', 4, 7, '4c5450a6d82c0d8757e7.jpg', '231ea7f1e5d63d08ec19.jpg', '442600ddf49cb192c2de.jpg'),
(16, 'Old Brother', 7627.22, 3, 194, 'entire,production,individual,back', 'Series others half write keep I effort of. Huge cost under discover. Campaign new develop result important seven near. Person international her truth bill. Its throughout according natural various.', '2025-04-16 09:55:26.939368', 6, 7, 'ced60d8e74133bf2c651.jpg', '442600ddf49cb192c2de.jpg', 'c12aa95d1323b596776d.jpg'),
(17, 'Address Sell', 57398.78, 1, 12, 'fact,white,discussion,foot', 'Design authority not eye none federal leg. Case control magazine decision. Degree put maintain door knowledge. Young staff program shoulder doctor.', '2025-04-16 09:55:26.939368', 2, 10, 'f5e6ecd7e42686c0778a.jpg', '231ea7f1e5d63d08ec19.jpg', 'dd68f1362bb883d5b07a.jpg'),
(18, 'Kid Whether', 105494.88, 13, 149, 'movement,lead,bill,language', 'Involve effort effect vote unit matter. Own eat play career key establish production quality. Article through reflect easy ball.', '2025-04-16 09:55:26.939368', 5, 7, 'ced60d8e74133bf2c651.jpg', '402c1efe2e6d9fad8122.jpg', '5151330859710dd6a79d.jpg'),
(19, 'Professor Eight', 103343.63, 19, 107, 'reduce,focus,practice,per', 'Talk require itself task prove bag. Western language require my better or body fine. Million understand firm spend consumer possible. Leave candidate four read character lay life performance.', '2025-04-16 09:55:26.939368', 4, 9, 'a027fd5477bfc573026b.jpg', '6f564bf7019eac59624c.jpg', 'sample_products'),
(20, 'Laugh Let', 104398.83, 14, 119, 'throw,while,heavy,let', 'Deal itself radio long. Glass including resource share. Pass attack air provide position hair. Certain industry road member.', '2025-04-16 09:55:26.939368', 2, 4, 'c12aa95d1323b596776d.jpg', 'eb48e0616d9a0f746b58.jpg', '97803489a0c0ecbaf718.jpg');

-- Continuing addproduct inserts due to length limitations
INSERT INTO addproduct (id, name, price, discount, stock, colors, "desc", pub_date, category_id, brand_id, image_1, image_2, image_3) VALUES
(21, 'Another Care', 7955.70, 25, 156, 'until,stuff,but,box', 'Share land plant indicate soon collection. Box ahead thought point expect detail. Maybe authority trip through hand. Serve light force real. Morning meet doctor their. Serious couple learn indeed.', '2025-04-16 09:55:26.939368', 4, 10, '7b4eb498899b37f49bd8.jpg', '6f564bf7019eac59624c.jpg', 'sample_products'),
(22, 'Man Purpose', 137969.87, 26, 95, 'threat,last,exactly,maintain', 'Person personal table. Lose she fund peace former moment manage theory. Impact price beyond fall drug even impact.', '2025-04-16 09:55:26.939368', 5, 2, 'adca7ce25746d4e562fc.jpg', 'cf113762b63b10f46c9d.jpg', 'ced60d8e74133bf2c651.jpg'),
(23, 'According Somebody', 146689.80, 15, 199, 'she,lawyer,human,everything', 'Thank open their food prevent mind. Through never page last serious hair. Fact onto mouth page leave. Raise compare follow phone student. Imagine next support family garden alone task.', '2025-04-16 09:55:26.939368', 6, 2, 'dc68ee1808d989b813c3.jpg', '442600ddf49cb192c2de.jpg', 'f5e6ecd7e42686c0778a.jpg'),
(24, 'My Agreement', 180148.21, 3, 170, 'worker,so,will,store', 'Dark whom policy recent more. Do various also more war option. Evidence family about red throughout water. Return according language leader attack. Woman fear son person.', '2025-04-16 09:55:26.939368', 6, 3, '4dc33e62c4ad05ec5c2f.jpg', '8592f5f4c127ecf56856.jpg', '402c1efe2e6d9fad8122.jpg'),
(25, 'Improve Listen', 73874.92, 27, 61, 'organization,capital,about,point', 'Administration nearly heavy treat. General matter cup weight stock. Moment born model that. Every usually event draw. So find serve age interesting.', '2025-04-16 09:55:26.939368', 6, 4, '402c1efe2e6d9fad8122.jpg', '231ea7f1e5d63d08ec19.jpg', '753f9a2c250e8ba7dc20.jpg'),
(26, 'Happy Station', 93452.25, 18, 123, 'sing,again,thought,pass', 'Like reduce staff system. Actually easy stock black debate probably. Dinner during Republican turn method.', '2025-04-16 09:55:26.939368', 3, 2, '442600ddf49cb192c2de.jpg', 'f5e6ecd7e42686c0778a.jpg', '8592f5f4c127ecf56856.jpg'),
(27, 'Risk Alone', 33296.93, 3, 131, 'Republican,bed,guess,let', 'Follow half down mind. Political any popular save. Your this trouble drive fine. Budget statement support heart themselves girl easy.', '2025-04-16 09:55:26.939368', 4, 6, '7cb3adfa78ab4f8c2914.jpg', '6f564bf7019eac59624c.jpg', '231ea7f1e5d63d08ec19.jpg'),
(28, 'Agreement Once', 188541.25, 1, 120, 'policy,it,serious,interest', 'Executive everyone organization senior meeting me. Feel man analysis study hope country. Perform door change their professional kid time.', '2025-04-16 09:55:26.939368', 2, 6, 'c4f9f96ec958a85a6bce.jpg', '4c5450a6d82c0d8757e7.jpg', '6f564bf7019eac59624c.jpg'),
(29, 'Customer Rest Ford', 34183.97, 0, 57, 'many,feel,above,box', 'Window strong young theory recent through kitchen. Simply lose have three investment. What year music themselves north would. Bank east old place action address company.', '2025-04-16 09:55:26.939368', 5, 11, '5151330859710dd6a79d.jpg', '4ca7aef7c60a8b738656.jpg', 'a6c03254f5aebc2a8a5a.jpg'),
(30, 'Situation Our', 19963.33, 28, 92, 'yeah,hope,prepare,effort', 'Use hot strategy decide right accept. Collection stuff market very hit. Them well occur international training. Organization result indeed suggest suggest hit fund.', '2025-04-16 09:55:26.939368', 2, 5, '4ca7aef7c60a8b738656.jpg', '8592f5f4c127ecf56856.jpg', '8592f5f4c127ecf56856.jpg'),
(31, 'Arm Body', 78581.70, 18, 177, 'expect,together,cell,own', 'Back pay personal help yet eye into. Career young surface cell tonight apply. Concern know something require human fast.', '2025-04-16 09:55:26.939368', 2, 4, '95f19d2825ccef699c03.jpg', 'dd68f1362bb883d5b07a.jpg', '5151330859710dd6a79d.jpg'),
(32, 'City Measure', 13427.57, 3, 45, 'successful,bit,effort,chance', 'Need such role source. Whom reflect cell how resource friend research. Forget kitchen successful court education ask teach study. Left probably almost stage sign put way simple.', '2025-04-16 09:55:26.939368', 2, 7, '753f9a2c250e8ba7dc20.jpg', '8592f5f4c127ecf56856.jpg', '4ca7aef7c60a8b738656.jpg'),
(33, 'That Third', 107453.31, 4, 125, 'perhaps,conference,when,activity', 'Finish explain girl nothing bring. Second dream capital fine mother modern history. Rise seat position experience.', '2025-04-16 09:55:26.939368', 1, 4, '753f9a2c250e8ba7dc20.jpg', '402c1efe2e6d9fad8122.jpg', '6087936f269e938141d8.jpg'),
(34, 'Activity Ball', 32555.37, 30, 39, 'sell,early,alone,position', 'Clear argue box long community central. Hear military very suggest walk place. Mean truth green none. Win member reflect first collection simple develop available. Ready fill figure crime drug wife.', '2025-04-16 09:55:26.939368', 3, 9, '4ca7aef7c60a8b738656.jpg', 'f5e6ecd7e42686c0778a.jpg', '6f564bf7019eac59624c.jpg'),
(35, 'Else Only', 22132.85, 21, 188, 'science,public,save,drop', 'Staff check energy boy. Instead team right thus. Offer right garden civil style. Mother drop professor market whose war. Down themselves culture apply. Candidate long country which know.', '2025-04-16 09:55:26.939368', 5, 9, 'cf113762b63b10f46c9d.jpg', '753f9a2c250e8ba7dc20.jpg', '6087936f269e938141d8.jpg'),
(36, 'Bank Time', 48429.82, 30, 155, 'wish,page,on,three', 'Kid similar share current. Then over film political large stock different. Give eat these little.', '2025-04-16 09:55:26.939368', 6, 8, 'fb04a80207d2678dcc0b.jpg', '0a8ee4f03596d8c718cd.jpg', '95f19d2825ccef699c03.jpg'),
(37, 'Resource Of', 40702.78, 0, 177, 'pull,executive,television,ability', 'Option why piece base week throughout fast voice. Race paper perform network clearly. Leg that father pattern. Perform church improve issue standard down north participant.', '2025-04-16 09:55:26.939368', 3, 9, '7cb3adfa78ab4f8c2914.jpg', '07a607800d78dc7531d4.jpg', '0a8ee4f03596d8c718cd.jpg'),
(38, 'Chance Decide', 195046.62, 1, 22, 'understand,see,thought,door', 'Community of end truth from husband. Whom song leader million memory attorney. Charge court capital support. Tonight left left off three blue best at. Rich think true claim drug couple positive. You challenge share.', '2025-04-16 09:55:26.939368', 4, 11, '7b4eb498899b37f49bd8.jpg', '442600ddf49cb192c2de.jpg', '4ca7aef7c60a8b738656.jpg'),
(39, 'Capital Forward', 171149.0, 6, 122, 'money,this,heart,loss', 'Investment available account first drop later forward. Husband read answer somebody maintain. Again American summer. Bit speech paper majority.', '2025-04-16 09:55:26.939368', 4, 1, '0a8ee4f03596d8c718cd.jpg', '753f9a2c250e8ba7dc20.jpg', '7cb3adfa78ab4f8c2914.jpg'),
(40, 'Event System', 28189.76, 16, 60, 'right,wonder,other,message', 'Structure whether standard operation. Pattern visit serve bar main despite. Commercial answer discussion full office less management. Wide experience owner discover.', '2025-04-16 09:55:26.939368', 4, 9, '97803489a0c0ecbaf718.jpg', '4ca7aef7c60a8b738656.jpg', 'fb04a80207d2678dcc0b.jpg');

-- Final batch of addproduct inserts
INSERT INTO addproduct (id, name, price, discount, stock, colors, "desc", pub_date, category_id, brand_id, image_1, image_2, image_3) VALUES
(41, 'Second Discuss', 174644.16, 0, 127, 'range,current,many,side', 'Cold piece cell student central soon. Door form effect news where phone. Base so threat. Add thing page know or. Rate along great range. Interest can friend today.', '2025-04-16 09:55:26.939368', 4, 10, '753f9a2c250e8ba7dc20.jpg', '0a8ee4f03596d8c718cd.jpg', '402c1efe2e6d9fad8122.jpg'),
(42, 'Home Way', 103557.36, 19, 40, 'employee,guess,instead,speech', 'Specific perform since paper sit. After visit whole base art during. Military benefit type agree condition remain. Place benefit issue former. Set important partner spend as from brother ever.', '2025-04-16 09:55:26.939368', 3, 8, '5151330859710dd6a79d.jpg', '1fbe657b69ffaf8de518.jpg', '7b4eb498899b37f49bd8.jpg'),
(43, 'Campaign Whether', 82676.35, 27, 56, 'to,mouth,task,team', 'Case shake source. Two spend next others. Matter day up. Item member science audience four culture response anyone. Suffer not cup job American affect indicate. Door chance watch thank animal another.', '2025-04-16 09:55:26.939368', 6, 2, 'a6c03254f5aebc2a8a5a.jpg', '442600ddf49cb192c2de.jpg', '7b4eb498899b37f49bd8.jpg'),
(44, 'Speech Notice', 197181.07, 9, 67, 'not,health,article,within', 'Performance me structure service. Of order think sure create. Different paper represent call attorney. There town especially popular. Enter discuss agency today realize line. Raise particular activity standard.', '2025-04-16 09:55:26.939368', 1, 7, 'dd68f1362bb883d5b07a.jpg', '4c5450a6d82c0d8757e7.jpg', 'ced60d8e74133bf2c651.jpg'),
(45, 'Million Need', 7873.60, 25, 168, 'break,sell,task,many', 'Inside medical recognize hour. Seek Mr might couple star former. Show me letter pay dinner wear itself. Which despite air.', '2025-04-16 09:55:26.939368', 6, 4, '4ca7aef7c60a8b738656.jpg', '8592f5f4c127ecf56856.jpg', 'fb04a80207d2678dcc0b.jpg'),
(46, 'Few Question', 77406.21, 12, 180, 'almost,detail,most,debate', 'Control thousand news human which capital theory. True tax data star point chance community. May happy administration natural how. Become trial two life time.', '2025-04-16 09:55:26.939368', 1, 11, 'fb04a80207d2678dcc0b.jpg', '07a607800d78dc7531d4.jpg', 'adca7ce25746d4e562fc.jpg'),
(47, 'Although Sport', 36308.83, 25, 189, 'citizen,share,argue,lead', 'Evening song front instead. None many rest quite. Attention here rate usually hard.', '2025-04-16 09:55:26.939368', 3, 3, 'c12aa95d1323b596776d.jpg', '07a607800d78dc7531d4.jpg', '753f9a2c250e8ba7dc20.jpg'),
(48, 'Early Must', 88930.08, 22, 17, 'effect,candidate,material,loss', 'Simple rock create free bag whole laugh. High sister assume half worker build production herself. Practice game way trade occur. Point man tax card successful officer stop control.', '2025-04-16 09:55:26.939368', 2, 11, 'ced60d8e74133bf2c651.jpg', '5151330859710dd6a79d.jpg', 'c12aa95d1323b596776d.jpg'),
(49, 'Finally Language', 187570.48, 29, 43, 'manager,process,same,likely', 'Special inside line tax go. Growth when choice large. Left couple weight meeting make. Process easy me card trial.', '2025-04-16 09:55:26.939368', 2, 8, 'dc68ee1808d989b813c3.jpg', 'f5e6ecd7e42686c0778a.jpg', '4ca7aef7c60a8b738656.jpg'),
(50, 'Wish Consumer', 70611.86, 25, 185, 'window,group,stock,assume', 'Series behavior production open position learn. Nation pick attorney star outside case. Culture return necessary leader want. Very stay position that computer.', '2025-04-16 09:55:26.939368', 6, 3, '8592f5f4c127ecf56856.jpg', '97803489a0c0ecbaf718.jpg', '07a607800d78dc7531d4.jpg'),
(51, 'ford xx2', 20000.0, 10, 10, 'black, white', 'dafsdfgsdfsáđà', '2025-04-17 09:28:47.676233', 2, 1, '0adad7f4024fae2aa86a.jpg', '3aa06b1b0558a2517627.jpg', '92a4f12d3e23f3b1d7eb.jpg'),
(52, 'ford xx23', 20000.0, 10, 10, 'black, white', 'dafsdfgsdfsáđà', '2025-04-17 09:28:47.676233', 2, 1, '61731eeb03600cb5d09c.jpg', 'f0f189d3bd8ed2e9d66e.jpg', '46509037cff3ec1f7bcd.jpg');

-- Create alembic_version table
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Insert alembic version
INSERT INTO alembic_version (version_num) VALUES ('9ee966d87e2c');

-- Create register table
CREATE TABLE "register" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    username VARCHAR(50) UNIQUE,
    email VARCHAR(50) UNIQUE,
    password BYTEA,
    country VARCHAR(50),
    city VARCHAR(50),
    contact VARCHAR(50),
    address VARCHAR(50),
    zipcode VARCHAR(50),
    profile VARCHAR(200),
    date_created TIMESTAMP NOT NULL
);

-- Insert register data (converting hex to bytea)
INSERT INTO register (id, name, username, email, password, country, city, contact, address, zipcode, profile, date_created)
VALUES (1, 'Hello Kitty', 'username', 'drive.nhatprox.003@gmail.com', '\x243262243132246f303037492f6235787551302e566537517a786a644f4966374f556a4f366247704d4e3970514e5737434c63484d4a6f736256374f', 'Vietnam', 'Ho Chi Minh City', '0797130840', 'Go Vap District', '700000', 'profile.ipg', '2025-04-04 10:57:26.829094');

-- Create customer_order table
CREATE TABLE customer_order (
    id SERIAL PRIMARY KEY,
    invoice VARCHAR(20) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL,
    customer_id INTEGER NOT NULL,
    date_created TIMESTAMP NOT NULL,
    orders TEXT
);

-- Create image table
CREATE TABLE image (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(100) NOT NULL,
    type VARCHAR(20)
);

-- Insert image data
INSERT INTO image (id, filename, type) VALUES
(1, 'adca7ce25746d4e562fc.jpg', 'gallery'),
(2, '231ea7f1e5d63d08ec19.jpg', 'gallery'),
(3, 'fb04a80207d2678dcc0b.jpg', 'gallery'),
(4, '753f9a2c250e8ba7dc20.jpg', 'gallery'),
(5, 'eb48e0616d9a0f746b58.jpg', 'gallery'),
(6, '4dc33e62c4ad05ec5c2f.jpg', 'gallery'),
(7, '4ca7aef7c60a8b738656.jpg', 'gallery'),
(8, '8592f5f4c127ecf56856.jpg', 'gallery'),
(9, 'dd68f1362bb883d5b07a.jpg', 'gallery'),
(10, '97803489a0c0ecbaf718.jpg', 'gallery'),
(11, '6f564bf7019eac59624c.jpg', 'gallery'),
(12, '07a607800d78dc7531d4.jpg', 'gallery'),
(13, '442600ddf49cb192c2de.jpg', 'gallery'),
(14, 'a6c03254f5aebc2a8a5a.jpg', 'gallery'),
(15, '5151330859710dd6a79d.jpg', 'gallery');

-- Re-enable foreign key constraints
SET session_replication_role = 'origin';