#! /usr/bin/python

import sched
import threading

class simon():

    def __init__(self, hw_interface, seq_generator):
        """
        Simon game constructor. Takes a ref to the hw interface class as well as the sequence
        generator.
        """
        #
        # The hardware interface for lights and sound
        #
        self.hw_interface = hw_interface

        #
        # This is the thing we use to request a new item to put on to the sequence list.
        #
        self.seq_generator = seq_generator

        #
        # The sequence we've generated so far, that we compare against
        #
        self.running_sequence = []

        #
        # Milliseconds before we start the game.
        #
        self.start_game_millisecods = 2000 * .001

        #
        # Milliseconds for final light to remain up at game loss
        #
        self.game_loss_light_msec = 2000 * 0.001

        #
        # Milliseconds between button presses before user must give input, else loses.
        #
        self.timeout_msec = 1500 * 0.001

        #
        # Seconds a light is off between flashes
        #
        self.replay_flash_off_msec = 300 * 0.001

        #
        # Seconds a light is on during flash sequence
        #
        self.replay_flash_on_msec = 300 * 0.001

        #
        # Milliseconds for delay before playback begins.
        #
        self.replay_start_msec = 1500 * 0.001

        #
        # Milliseconds to light light when user presses
        #
        self.user_press_msec = 100 * 0.001

        #
        # The current index of the simon game list during playback.
        #
        self.current_index = 0

        #
        # Input handler to be called when we're handling input. Reduces mode-tracking.
        # Should return False if input was ignored.
        #
        self.input_handler = self.input_filter_all

        #
        # A thread used as a timeout to lose the game!
        #
        self.user_play_timer = None

        #
        # Poll this to determine if the game is running
        #
        self.game_running = False

    def start_game(self):
        """
        Start the game!!
        """
        #
        # We kick off a playback after a short time of user preparation.
        #
        self.game_running = True
        self.running_sequence = []
        self.hw_interface.hw_all_off()
        t = threading.Timer(self.start_game_millisecods, self.append_new_item_and_play_back)
        t.start() 

    def append_new_item_and_play_back(self):
        """
        Create a new item, put it on the end of the list, and initiate playback.
        """
        self.running_sequence.append(self.seq_generator.sequence_generate_entry())
        self.start_seq_flash_funct()

    def set_sequence(self, sequence):
        """
        Currently only for testing.
        """
        self.running_sequence = sequence

    def lose_game(self):
        """
        Game loss handler. Can be called from a timer or from input mismatch.
        """
        #
        # Closure to provide something to call back to finish the game loss sequence.
        #
        def finish_lose_game():
            self.hw_interface.hw_all_off()
            self.game_running = False

        self.input_handler = self.input_filter_all
        self.hw_interface.hw_all_off()
        self.hw_interface.hw_light_on(self.current_playback_item().color_abbrev)
        t = threading.Timer(self.game_loss_light_msec, finish_lose_game)
        t.start()
        print "LOSER!!!!"

    #
    # Filter all input while we're in the playback loop.
    #
    def input_filter_all(self, input_data):
        return False

    #
    # Filter only input that corresponds to a non-button press.
    #
    def gameplay_input_filter(self, input_data):
        vals = ['r', 'y', 'g']
        if input_data not in vals:
            return True
        else:
            self.user_play_timer.cancel()
            self.input_handler = self.input_filter_all

            #
            # Closure so we have something to call later.
            #
            def end_button_press():
                self.hw_interface.hw_light_off(input_data)
                self.advance_current_index()
                self.input_handler = self.gameplay_input_filter
                if input_data == self.current_playback_item().color_abbrev:
                    if self.current_index == len(self.running_sequence) - 1:
                        self.append_new_item_and_play_back()
                else:
                    self.lose_game()

            self.hw_interface.hw_light_on(input_data)
            t = threading.Timer(self.user_press_msec, end_button_press)
            t.start()

    #
    # Reset the current index state
    #
    def reset_current_index(self):
        self.current_index = -1

    #
    # Go to the next index in the seq list
    #
    def advance_current_index(self):
        self.current_index += 1

    def handle_input(self, input_data):
        """
        Handles user input :). We expect the caller to filter out any
        input that he's interested in, and we can handle the rest.
        """
        self.input_handler(input_data)

    def current_playback_item(self):
       """
       Returns the current item in the sequence.
       """
       return self.running_sequence[self.current_index]

    def start_seq_flash_funct(self):
        """
        Plays back the sequence to the user.
        """
        self.input_handler = self.input_filter_all
        self.reset_current_index()
        self.advance_current_index()
        t = threading.Timer(self.replay_start_msec, self.seq_playback_turn_on)
        t.start()

    def seq_playback_turn_off(self):
        """
        Turns off light, then sleeps until we need to awake. If we're at the
        end of the sequence, we resert current index so user input is used for
        comparison, turn off the light, and listen for input, and
        set the "you're a loser" timer.
        """
        self.hw_interface.hw_light_off(self.current_playback_item().color_abbrev)
        if self.current_index != len(self.running_sequence) - 1:
            self.advance_current_index()
            t = threading.Timer(self.replay_flash_off_msec, self.seq_playback_turn_on)
            t.start()
        else:
            self.reset_current_index()
            self.input_handler = self.gameplay_input_filter
            self.user_play_timer = threading.Timer(self.timeout_msec, self.lose_game)
            self.user_play_timer.start()

    def seq_playback_turn_on(self):
        self.hw_interface.hw_light_on(self.current_playback_item().color_abbrev)
        t = threading.Timer(self.replay_flash_on_msec, self.seq_playback_turn_off)
        t.start()

    def sequence_play_input_handler(self, input_data):
        return False
