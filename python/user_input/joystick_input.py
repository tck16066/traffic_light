import pygame


button_idxs = {}

def init_joystick(red_button_index=-1, yellow_button_index=-1, green_button_index=-1):
    pygame.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()

    global button_idxs
    button_idxs[red_button_index] = "r"
    button_idxs[yellow_button_index] = "y"
    button_idxs[green_button_index] = "g"

    KICK_GAME = pygame.USEREVENT+1
    pygame.time.set_timer(KICK_GAME, 50)

    return pygame.joystick.get_count() > 0

class joystick_input:
    def __init__(self):
        self.joystick = None

    def joystick_button(self, event):
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        press = None
        for joystick in joysticks:
            buttons = joystick.get_numbuttons()
            print("    JOYSTICK:")
            for i in range(buttons):
                button = joystick.get_button(i)
                print("    Button {:>2} value: {}".format(i, "DOWN" if button == 1 else "UP"))
                if press == None and button == 1:
                    press = i
            print("    END")
        if press in button_idxs:
            global button_idxs
            return button_idxs[press]
        return None
    
    
    def get_user_input(self, timeout_sec):
        e = pygame.event.wait()
        events = pygame.event.get()
        events.insert(0, e)
        ret_val = None
        for event in events:
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                ret_val = self.joystick_button(event)
        return ret_val

