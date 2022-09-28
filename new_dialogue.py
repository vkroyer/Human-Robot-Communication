import time
from voice_input_arrays import names_dict, directions_questions, variations_of_yes, variations_of_no
from utterances import utterance_dict, directions_dict

###############################
##### GLOBALS #################

LAST_ROBOT_UTTERANCE = "Hello, I'm a receptionist robot. You can ask me for directions to a professor's office"
LAST_QUESTION = ""
NAME_VOICE_INPUT = ""
REPEAT_COUNTER = 0
SLEEP_TIME = 1.5 # seconds
IGNORE_SENSITIVITY = 0.5 # between 0 and 1 (0 will ignore everything, 1 will only ignore if transcript is exactly like last robot utterance)

###############################

def handle_voice_input(transcript):
    """Based on the user input provided by Google speech-to-text,
    this function will provide answers and play the corresponding mp3 files.

    Returns True after it says goodbye in order to shut down the program.
    """

    global LAST_ROBOT_UTTERANCE
    global LAST_QUESTION
    global NAME_VOICE_INPUT
    global REPEAT_COUNTER

    transcript = transcript.lower() # ignore uppercase letters in Google's speech-to-text

    # Ignore robot's own voice
    equal_count = 0
    for word in transcript.strip(",.!?"):
        if word in LAST_ROBOT_UTTERANCE.strip(",.!?"):
            equal_count += 1
    if equal_count >= IGNORE_SENSITIVITY * len(LAST_ROBOT_UTTERANCE) and not any([answer in transcript for answer in variations_of_no+variations_of_yes]):
        print("Probably the robot's own voice. IGNORED.")
        return False

    # Handle variations of questions for directions
    if any([question in transcript for question in directions_questions]):
        for name, name_variations in names_dict.items():
            if any([name_variation in transcript for name_variation in name_variations]):
                question = utterance_dict[f"{name}_validation"]
                print(question)
                play_mp3(f"{name}_validation.mp3") # Plays the audio file with the question
                LAST_ROBOT_UTTERANCE = question
                LAST_QUESTION = question
                NAME_VOICE_INPUT = name
                break
        else:
            play_mp3("not_understand.mp3") # Plays the audio file
            print(utterance_dict["not_understand"])
            LAST_ROBOT_UTTERANCE = utterance_dict["not_understand"]

    # Handle the answer yes
    elif any([answer in transcript for answer in variations_of_yes]):
        
        # Human confirmed they want to go to said office
        if "Do you want to go to" in LAST_QUESTION:
        
            if NAME_VOICE_INPUT == "cristina":
                question = utterance_dict["horst_validation"]
                print(question)
                play_mp3("horst_shortcut_validation.mp3") # Plays the audio file
                LAST_ROBOT_UTTERANCE = question
                LAST_QUESTION = question

            # Giving directions
            if NAME_VOICE_INPUT in directions_dict.keys():
                print(utterance_dict[f"{NAME_VOICE_INPUT}_confirmation"])
                play_mp3(f"{NAME_VOICE_INPUT}_start_dir.mp3") # Plays the audio file
                print(f"{directions_dict[NAME_VOICE_INPUT]}")
                play_mp3(f"{NAME_VOICE_INPUT}_dir.mp3") # Plays the audio file

                time.sleep(SLEEP_TIME) # give the human time to think first
                question = utterance_dict["q_understand"]
                print(question)
                play_mp3("q_understand1.mp3") # Plays the audio file
                LAST_ROBOT_UTTERANCE = utterance_dict[f"{NAME_VOICE_INPUT}_confirmation"] + directions_dict[NAME_VOICE_INPUT] + question
                LAST_QUESTION = question

        # De Horst shortcut
        elif "Do you already know how to get to" in LAST_QUESTION:
            print(utterance_dict["cristina_confirmation"])
            play_mp3(f"{NAME_VOICE_INPUT}_shortcut_start_dir.mp3") # Plays the audio file
            LAST_ROBOT_UTTERANCE = directions_dict[NAME_VOICE_INPUT]
            print(directions_dict[NAME_VOICE_INPUT])
            play_mp3(f"{NAME_VOICE_INPUT}_shortcut_dir.mp3") # Plays the audio file

            time.sleep(SLEEP_TIME) # give the human time to think first
            question = utterance_dict["q_understand"]
            print(question)
            play_mp3("q_understand1.mp3") # Plays the audio file
            LAST_QUESTION = question
            LAST_ROBOT_UTTERANCE = utterance_dict["cristina_confirmation"] + directions_dict[NAME_VOICE_INPUT] + question

        # Human understood directions, shut down program
        elif LAST_QUESTION == "Did you understand the directions?":
            print(utterance_dict["bye"])
            play_mp3("bye.mp3") # Plays the audio file
            LAST_ROBOT_UTTERANCE = utterance_dict["bye"]
            return True

    # Handle the answer no
    elif any([answer in transcript for answer in variations_of_no]):
        # The robot's validation question was wrong
        if "Do you want to go to" in LAST_QUESTION:
            LAST_ROBOT_UTTERANCE = utterance_dict["not_understand"]
            print(LAST_ROBOT_UTTERANCE)
            play_mp3("not_understand.mp3")
            LAST_QUESTION = "" # Reset the variable to avoid unwanted robot dialogue later

        # De Horst longcut
        elif "Do you already know your way" in LAST_QUESTION:
            print(utterance_dict["cristina_confirmation"])
            play_mp3(f"{NAME_VOICE_INPUT}_longcut_start_dir.mp3") # Plays the audio file
            print(directions_dict[NAME_VOICE_INPUT])
            play_mp3(f"{NAME_VOICE_INPUT}_longcut_dir.mp3") # Plays the audio file

            time.sleep(SLEEP_TIME) # give the human time to think first
            question = utterance_dict["q_understand"]
            print(question)
            LAST_ROBOT_UTTERANCE = utterance_dict["cristina_confirmation"] + directions_dict[NAME_VOICE_INPUT] + question
            LAST_QUESTION = question

        # Repeat the directions if user didn't understand (three times max)
        elif LAST_QUESTION == utterance_dict["q_understand"]:
            if REPEAT_COUNTER < 2:
                REPEAT_COUNTER += 1
                print(utterance_dict[f"{NAME_VOICE_INPUT}_repeat"])
                play_mp3(f"{NAME_VOICE_INPUT}_repeat.mp3") # Plays the audio file
                print(f"{directions_dict[NAME_VOICE_INPUT]}")
                play_mp3(f"{NAME_VOICE_INPUT}_dir.mp3") # Plays the audio file
                time.sleep(SLEEP_TIME) # give the human time to think first
                question = utterance_dict["q_understand"]
                print(question)
                play_mp3("q_understand1.mp3")
                LAST_ROBOT_UTTERANCE = utterance_dict[f"{NAME_VOICE_INPUT}_repeat"] + directions_dict[NAME_VOICE_INPUT] + question
                LAST_QUESTION = question
            
            else:
                print(utterance_dict["recommend"])
                play_mp3("human_not_understand.mp3")
                print(utterance_dict["bye"])
                play_mp3("bye.mp3")
                LAST_ROBOT_UTTERANCE = utterance_dict["recommend"] + utterance_dict["bye"]
                

    else:
        LAST_ROBOT_UTTERANCE = utterance_dict["not_understand_at_all"]
        print(utterance_dict["not_understand_at_all"])
        play_mp3("not_understand_at_all.mp3")

    return False


from playsound import playsound
def play_mp3(filename):
    path = "mp3s"
    playsound(f"{path}/{filename}")