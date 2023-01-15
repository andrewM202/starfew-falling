from pygame.math import Vector2
# screen
Screen_Width = 1280
Screen_Height = 720
Tile_Size = 64

# overlay positions 
Overlay_Positions = {
	'tool' : (40, Screen_Height - 15), 
	'seed': (70, Screen_Height - 5)}

Player_Tool_Offset = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

Layers = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

Apple_Pos = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

Grow_Speed = {
	'corn': 1,
	'tomato': 0.7
}

Sale_Prices = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}

Purchase_Prices = {
	'corn': 4,
	'tomato': 5
}
