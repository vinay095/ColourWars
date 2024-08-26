# Colour Wars

Color Wars is a simple 2D grid-based strategy game created with Python and Pygame. Players take turns placing their color on the grid to capture cells and dominate the game board. The game can be played in two modes: Player vs. Player (human) or Player vs. Computer (AI). In AI mode, you can also choose the difficulty level.

Features
Two Game Modes:

Player vs. Player: Compete against a friend on the same computer.
Player vs. Computer: Play against an AI opponent with selectable difficulty levels (Easy, Medium, Hard).
Simple Grid-Based Gameplay: Control your color's influence over a 5x5 grid. Capture your opponent's cells and aim for total domination.

AI Difficulty Levels: In AI mode, you can select from three difficulty levels:

Easy: The AI makes random moves.
Medium: The AI starts to prioritize more strategic moves.
Hard: The AI plays with the best possible strategy.
How to Play
Grid Mechanics:

Players take turns clicking on the grid cells.
If the selected cell is empty, it becomes the starting color.
If it's already occupied by the player or a neutral cell, the value of the cell is increased.
Cells with a value of 4 "split", affecting surrounding cells.
Players can capture opponent's cells by "splitting" into neighboring cells.
Winning:

The game continues until one player dominates the board. If one player has cells remaining while the opponent has none, they win.
