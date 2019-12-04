import time
import board
import displayio
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

# Set the background color
BACKGROUND_COLOR = 0x443355
 
# Set the NeoPixel brightness
BRIGHTNESS = 0.3
# Setup PyPortal without networking
pyportal = PyPortal(default_bg=BACKGROUND_COLOR)

# Button colors
RED = (255, 0, 0)
ORANGE = (255, 34, 0)
YELLOW = (255, 170, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
VIOLET = (153, 0, 255)
MAGENTA = (255, 0, 51)
PINK = (255, 51, 119)
AQUA = (85, 125, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

#set up the font
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
large_font = cwd+"/fonts/Anton-Regular-104.bdf"
large_font2 = bitmap_font.load_font(large_font)
glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
large_font2.load_glyphs(glyphs)

#set up the scoreboard
HEALTH = 20
PLAYER_COUNTER = 0

#create the buttons
spots = [
    {'label': "1", 'pos': (10, 150), 'size': (60, 60), 'color': RED},
    {'label': "2", 'pos': (90, 150), 'size': (60, 60), 'color': GREEN},
    {'label': "3", 'pos': (170, 150), 'size': (60, 60), 'color': RED},
    {'label': "4", 'pos': (250, 150), 'size': (60, 60), 'color': GREEN}	
	]

#initialize list of texts
texts= displayio.Group(max_size=3)
pyportal.splash.append(texts)	
	
#function for updating the display
def update_display():
	counters = [{'font':large_font2, 'max_glyphs': 3, 'text' : "%d"  % HEALTH     , 'pos': (30,60) ,'color': 0xFFFFFF},
			{'font':large_font2, 'max_glyphs': 3, 'text' : "%d"  % PLAYER_COUNTER , 'pos': (190,60),'color': 0xFFFFFF}]
	for counter in counters:
		texty = Label(counter['font'],
					max_glyphs=counter['max_glyphs'],
					x=counter['pos'][0],y=counter['pos'][1],
					color=counter['color'],
					text=counter['text'])
		texts.append(texty)
		if len(texts) >2:
			texts.pop(0)
			
#create the buttons on the screen
buttons = []
for spot in spots:
    button = Button(x=spot['pos'][0], y=spot['pos'][1],
                    width=spot['size'][0], height=spot['size'][1],
                    style=Button.SHADOWROUNDRECT,
                    fill_color=spot['color'], outline_color=0x222222,
                    name=spot['label'])
    pyportal.splash.append(button.group)
    buttons.append(button)			
	
#initial display without popping the list
update_display()

while True:
	touch = pyportal.touchscreen.touch_point
	if touch:
		if buttons[0].contains(touch):
			HEALTH-=1
		if buttons[1].contains(touch):
			HEALTH+=1
		if buttons[2].contains(touch):
			PLAYER_COUNTER-=1
		if buttons[3].contains(touch):
			PLAYER_COUNTER+=1
		print(touch)
		update_display()
	time.sleep(0.05)