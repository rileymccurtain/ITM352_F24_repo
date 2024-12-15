Flashcard App: This is a Flask-based web application that enables users to create, manage, and practice flashcards. The app integrates user authentication, deck management, and flashcard practice sessions with instant feedback along with score tracking.

Features 
- Create Decks: Add decks with custom titles to organize flashcards by topics. 
- Edit Decks: Modify deck names to ensure they remain pertinent. 
- Delete Decks: Discard decks that are no longer needed. 
- Add Flashcards: Create flashcards with questions and answers within a deck. 
- Edit Flashcards: Revise the content of currently available flashcards. 
- Delete Flashcards: Remove specific flashcards from a deck. 
- Quiz Mode: Attempt randomized quizzes with flashcards in sequential difficulty order, including easy, medium, and hard, and receive prompt feedback.
- Result Display: Access quiz results, including accuracy, time spent, and progress by difficulty level.

Technical Specifications: This application is reliant on Python 3.8+, Flask 2.0+, and pip.

Applied Instrumentation 
- Backend: Flask
- Database: SQLite 
- Frontend: CSS, HTML
- Security: Werkzeug for password hashing

A Manual to Operating the Application

Adding a Deck 
1. Navigate to the home page. 
2. Choose a title for the deck under “Deck Name:” and click “Create Deck.”
3. On the home page, it can be found under “Your Decks.”

Maintaining Flashcards 
1. Click on a deck to open it. 
2. Add a new card with a question, answer, and difficulty rating, and then select “Add Card.” 
3. Edit or delete existing cards through the corresponding buttons next to each flashcard. 

Utilizing Flashcards 
1. Open a deck and click “Start Quiz.”
2. Flashcards will be shown in a sequence based on difficulty. In any case, questions are shuffled and randomized within each category.
3. Answer the question and receive immediate feedback. 

Viewing Results 
After completing a quiz, the results page displays: 
- Time spent in minutes. 
- Percentage accuracy. 
- The number of incorrect answers. 
- An overview of card difficulty ratings. 