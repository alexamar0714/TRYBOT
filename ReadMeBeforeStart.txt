General Rules:

- Try to keep github up-to-date. ie push before end of session.
	//just so others can check progress etc. etc.

- Coding conventions:
	 - names/variables --> underscore and non-Alpha
		example: du_er_homo

	 - Comment more than you think is necessary

	 - Use british english
		ie Behaviour NOT behavior
		ie Optimisation NOT optimization
	

- After completion of a module/class
	- write test-code for it + Document this test-code.
	//Test every case thinkable, both the simple and advanced one
	//Documentaion. What is tested, what is the expected output, what was outputted	
	
	- write documentation.
		- all Methods and its input/outputs.(arguments, returns)
	  	- Short description of what the methods do.
	


Sprint 0:

---------------
Database
---------------

//Do not make it possible to delete tables/rows/columns. If necessary, only remove
//its access possiblity, ie its still in the database but not accesable

-- 3 Modules
	1 - Database (SQL tables)
	2 - Input/Modifying Module (Python)
	3 - Output/Fetch Module (Python)


(1) Database 

create tables with:
		- comments (@ - link ---- primary key)
		- Keywords (ID, Keyword, priority, foreign key *comments*)

(2) Input/Modifying Module

Bot -> Database

- Input: List of tuples, with keyword + priority
	//Last element in list is ALWAYS link to answer/question
	example: [(ball, 5), (homo, 10), @link]		

- "output" --> towards Database
	create code that translates the List into keywords and priority and adds them
	to the database.
	//Shivam + Daniel, you choose how.
	example: insert ball, 5 into keywords(table)

(3) Output/Fetch Module

- Input: List of keywords
	example: [ball, homo, fin, rar]
	Create code that uses these keywords to find the appropriate answer in the database

- output: List of @links
	example: [@161, @123] / []  / [@23]
	Create code that converts the answer(s) received from the database and add them to a LIST
	and return this LIST



----------------------------------- 	
SCRAPING. ALEX + DUONG LEARN IT AND DO IT.