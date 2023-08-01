# Guess-the-object
This is a two-player game, in which one player is going to think of an object and the other one is going to try to guess the object by asking a specific number of questions. Before starting the game, both players need to choose between 5 different categories, each of them with a difficulty level, i.e., a different number of possible questions.

The game begins with Player #1, which is going to write in a “secret box” the object which he/she is thinking about. During the game, the word inside the secret box will only be visible to Player #1. Once the word is set up, Player #2 can start doing the questions, each question must be able to be answered with a simple “yes”, “no” or “sometimes” by Player #1, it is not allowed to give any additional information beyond these three responses, so it is important for Player #2 to ask questions that can be answered with a single word. The number of possible questions Player #2 can make, depends on the chosen category at the beginning of the game.

The game ends when Player #2 guesses the object inside the secret box, or when he/she reaches the maximum number of possible questions. Player #2 wins if they guess the object correctly within the specified number of questions. Player #1 wins if player #2 is unable to guess the object. Players can switch roles after each game if desired

The game is developed in Python using sockets and a Database to store each of the questions and answers
