This is my Final Project in DI. It's a card game based on Heroes of Might and Magic series.

How to run:

1. Install Python 3
2. Install pygame (type 'pip install pygame' in the command line)
3. Type 'python mp.py' in the command line

How to win:

When any player runs out of hitpoints at the end of turn, the game ends. The player who still has hitpoints becomes a winner.
If both players' hitpoints are less or equal to 0 at the end of the turn, the game results in a draw.

How to play:

Choose your faction (one of four images in the right part of the screen) and press 'Start game'. Your opponent should do the same.

There are 28 cards in your deck in total. (7+6+5+4+3+2+1): 7 units of first tier, 6 units of second tier and so on
At the beginning of the game you receive 3 random cards from your faction deck. 
Please note that some card effects allow you to draw/generate additional cards.
Important: after your deck is empty, it DOES NOT reshuffle! If you have no cards to play, deal with it:). Deck management is a part of this game.

Every turn you draw a new card from your deck and receive certain amount of gold. This amount increases every 3 turns.
You can play any number of cards during your turn, provided that you have enough gold to spend. You can also pass and save your cards and gold for future.
There is a hard cap of gold you can have at the beginning of your turn. This cap also increases as the game advances.

Card has 3 basic parameters:

1. Attack. This is the damage that it deals on attack or being attacked. This is the LEFT of two values which are displayed on the top of each card.
2. Health. This is the amount of damage a card can survive. This is the RIGHT of two values which are displayed on the top of each card.
3. Cost. This is the amount of gold you have to spend to play this card.
Many cards have their unique abilities. You can read about them in the 'docs/factions' folder. 

Every turn one player is the attacker, another one is the defender. The turn has 3 phases.

1. Attacker plays his cards.
2. Defender plays his cards.
3. Attacker cards deal their damage (the order is from rear to front and from left to right)

If your attacking card has an opponent card placed in front of it, it will attack this opponent card.
Otherwise, it will attack your opponent directly, causing him lose hitpoints.

After the attacking phase, turn ends. Attacker and defender change their places. New turn begins.

Now I recommend you to read about game factions. To do it, go to the 'docs/factions' folder.






