import time
from voice_input_arrays import names_dict, directions_questions, variations_of_yes, variations_of_no
from utterances import directions_dict, not_understand, not_understand_at_all

###############################
##### GLOBALS #################

LAST_ROBOT_UTTERANCE = "Hello, I'm a receptionist robot. You can ask me for directions to a professor's office"
LAST_QUESTION = ""
NAME_VOICE_INPUT = ""
REPEAT_COUNTER = 0
SLEEP_TIME = 1.5 # seconds

###############################

def handle_voice_input(utterance):
    """Based on the user input provided by Google speech-to-text,
    this function will provide answers and play the corresponding mp3 files.
    """

    global LAST_ROBOT_UTTERANCE
    global LAST_QUESTION
    global NAME_VOICE_INPUT
    global REPEAT_COUNTER

    utterance = utterance.lower() # ignore uppercase letters in Google's speech-to-text

    # Ignore robot's own voice
    equal_count = 0
    for word in utterance.strip(",.!?"):
        if word in LAST_ROBOT_UTTERANCE.strip(",.!?"):
            equal_count += 1
    if equal_count >= 0.7 * len(LAST_ROBOT_UTTERANCE) and not any([answer in utterance for answer in variations_of_no + variations_of_yes]):
        print("Probably the robot's voice")
        return

    # Handle questions for directions
    if any([question in utterance for question in directions_questions]):
        for name, name_variations in names_dict.items():
            if any([name_variation in utterance for name_variation in name_variations]):
                question = f"Do you want to go to {name}'s office?"
                LAST_ROBOT_UTTERANCE = question
                print(f"{question}")
                play(f"{name}_validation.mp3") # Plays the audio file with the question
                LAST_QUESTION = question
                NAME_VOICE_INPUT = name
                break
        else:
            play("not_understand.mp3") # Plays the audio file
            LAST_ROBOT_UTTERANCE = not_understand
            print(f"{not_understand}")

    # Handle the answer yes
    elif any([answer in utterance for answer in variations_of_yes]):
        if "Do you want to go to" in LAST_QUESTION:

            if NAME_VOICE_INPUT == "cristina":
                question = "Do you already know how to get to De Horst?"
                LAST_ROBOT_UTTERANCE = question
                print(f"{question}")
                play("horst_shortcut_validation.mp3") # Plays the audio file
                LAST_QUESTION = question

            # Giving directions
            if NAME_VOICE_INPUT in directions_dict.keys():
                LAST_ROBOT_UTTERANCE = "Okay, giving directions to {NAME_VOICE_INPUT}'s office"
                print(f"Okay, giving directions to {NAME_VOICE_INPUT}'s office.")
                play(f"{NAME_VOICE_INPUT}_start_dir.mp3") # Plays the audio file
                LAST_ROBOT_UTTERANCE = directions_dict[NAME_VOICE_INPUT]
                print(f"{directions_dict[NAME_VOICE_INPUT]}")
                play(f"{NAME_VOICE_INPUT}_dir.mp3") # Plays the audio file
                time.sleep(SLEEP_TIME) # give the human time to think first
                question = "Did you understand the directions?"
                LAST_ROBOT_UTTERANCE = question
                print(f"{question}")
                play("q_understand1.mp3") # Plays the audio file
                LAST_QUESTION = question

        # De Horst shortcut
        elif "Do you already know how to get to" in LAST_QUESTION:
            NAME_VOICE_INPUT = "cristina_shortcut"
            LAST_ROBOT_UTTERANCE = "Okay, giving directions to {NAME_VOICE_INPUT}'s office"
            print(f"Okay, giving directions to {NAME_VOICE_INPUT}'s office.")
            play(f"{NAME_VOICE_INPUT}_start_dir.mp3") # Plays the audio file
            LAST_ROBOT_UTTERANCE = directions_dict[NAME_VOICE_INPUT]
            print(f"{directions_dict[NAME_VOICE_INPUT]}")
            play(f"{NAME_VOICE_INPUT}_dir.mp3") # Plays the audio file
            time.sleep(SLEEP_TIME) # give the human time to think first
            question = "Did you understand the directions?"
            LAST_ROBOT_UTTERANCE = question
            print(f"{question}")
            play("q_understand1.mp3") # Plays the audio file
            LAST_QUESTION = question

        # Human understood directions, shut down program
        elif LAST_QUESTION == "Did you understand the directions?":
            LAST_ROBOT_UTTERANCE = "Goodbye, have a nice day."
            print("Goodbye, have a nice day.")
            play("bye.mp3") # Plays the audio file

    # Handle the answer no
    elif any([answer in utterance for answer in variations_of_no]):
        # The robot's validation question was wrong
        if "Do you want to go to" in LAST_QUESTION:
            LAST_ROBOT_UTTERANCE = "I'm sorry, I'm new to the job, so I can only help with directions to the list of professors."
            print(LAST_ROBOT_UTTERANCE)
            play("not_understand.mp3")
            LAST_QUESTION = "" # Reset the variable to avoid unwanted robot dialogue later

        # De Horst longcut
        elif "Do you already know your way" in LAST_QUESTION:
            NAME_VOICE_INPUT = "cristina_longcut"
            LAST_ROBOT_UTTERANCE = f"Okay, giving directions to {NAME_VOICE_INPUT}'s office"
            print(f"Okay, giving directions to {NAME_VOICE_INPUT}'s office.")
            play(f"{NAME_VOICE_INPUT}_start_dir.mp3") # Plays the audio file
            LAST_ROBOT_UTTERANCE = directions_dict[NAME_VOICE_INPUT]
            print(f"{directions_dict[NAME_VOICE_INPUT]}")
            play(f"{NAME_VOICE_INPUT}_dir.mp3") # Plays the audio file
            time.sleep(SLEEP_TIME) # give the human time to think first
            question = "Did you understand the directions?"
            LAST_ROBOT_UTTERANCE = question
            print(f"{question}")
            LAST_QUESTION = question

        # Repeat the directions if user didn't understand (three times max)
        elif LAST_QUESTION == "Did you understand the directions?":
            if REPEAT_COUNTER < 2:
                REPEAT_COUNTER += 1
                LAST_ROBOT_UTTERANCE = f"Okay, giving directions to {NAME_VOICE_INPUT}'s office"
                print(f"Okay, giving directions to {NAME_VOICE_INPUT}'s office.")
                play(f"{NAME_VOICE_INPUT}_start_dir.mp3") # Plays the audio file
                LAST_ROBOT_UTTERANCE = directions_dict[NAME_VOICE_INPUT]
                print(f"{directions_dict[NAME_VOICE_INPUT]}")
                play(f"{NAME_VOICE_INPUT}_dir.mp3") # Plays the audio file
                time.sleep(SLEEP_TIME) # give the human time to think first
                question = "Did you understand the directions?"
                LAST_ROBOT_UTTERANCE = question
                print(f"{question}")
                play("q_understand1.mp3")
                LAST_QUESTION = question
            
            else:
                print("\nI'm sorry I can't be of more help, I would recommend downloading the Campus app on your smartphone.")
                play("human_not_understand.mp3")
                LAST_ROBOT_UTTERANCE = "Goodbye, have a nice day"
                print("\nGoodbye, have a nice day.")
                play("bye.mp3")
                

    else:
        LAST_ROBOT_UTTERANCE = not_understand_at_all
        print(f"{not_understand_at_all}")
        play("not_understand_at_all.mp3")


from playsound import playsound
def play(filename):
    path = "mp3s"
    playsound(f"{path}/{filename}")