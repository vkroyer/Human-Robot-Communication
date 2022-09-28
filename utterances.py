
### Introduction/greetings
greeting = "Hello, I'm a receptionist robot, you can ask me for directions to a professor's office."


### Question
not_understand = "I'm sorry, I'm new to the job, so I can only help with directions to the list of professors."
not_understand_at_all = "Sorry, I didn't get that, could you repeat that again?"


### Validation
names = ["Bob", "Dirk", "Mariet", "Dennis", "Daniel", "Cristina", "Edwin"]
validations = [f"Do you want to go to {name}'s office?" for name in names]


### Directions
professor_confirmations = [f"Okay, giving directions to {name}'s office" for name in names]
professor_repeats = [f"Okay, I will repeat the directions to {name}'s office" for name in names]

# Zilverling
bob_dir = 'Exit the door closest to the projector. Walk straight forward until you reach the staircase or the elevator, and go up to the second floor. From the staircase turn left in the hallway and walk forward until you reach room 2035 on the left side. The room number is 2035'
dirk_dir = 'Exit the door closest to the projector. Walk straight forward until you reach the staircase or the elevator, and go up to the second floor. From the staircase turn right in the hallway and walk forward until you reach room 2055 on the right side. The room number is 2055'
mariet_dir = 'Exit the door closest to the projector. Walk straight forward until you reach the staircase or the elevator, and go up to the second floor. From the staircase turn right in the hallway and walk forward until you reach room 2067 on the right side. The room number is 2067'
dennis_dir = 'Exit the door closest to the projector. Walk straight forward until you reach the staircase or the elevator, and go up to the second floor. From the staircase turn right in the hallway and walk forward until you reach room 2067 on the right side. The room number is 2067'
daniel_dir ='Exit the door closest to the projector. Walk straight forward until you reach the staircase or the elevator, and go up to the second floor. From the staircase turn right in the hallway and walk forward until you reach room 2061 on the right side. The room number is 2061'

# De Horst
horst_shortcut_validation = "Do you already know how to get to De Horst?"
cristina_shortcut_dir = "When you're at De Horst enter the building on the left hand side under the bridge. Then take the staircase up to the second floor. When you're on the second floor exit the staircase and turn left. Walk down the corridor until you reach room W254 on your right side. The room number is W254"
cristina_longcut_dir = "Exit the door closest to the projector. Walk until you get to the first exit on your left. When you're outside, walk straight forwards until you reach the other building. Take a left and follow the road forwards until you're at an intersection. Turn right in the intersection. Continue on this path until the next intersection and turn right again. Follow the road under the bridge and take an immediate left. Now you're at De Horst building. Enter the building on the left hand side under the bridge. Then take the staircase up to the second floor. When you're on the second floor exit the staircase and turn left. Walk down the corridor until you reach room W254 on your right side. The room number is W254"

# Carré
# carre_shortcut_validation = "Do you already know how to get to Carré?"
edwin_longcut_dir = "Exit the door closest to the projector. Walk straight forward past the staircase, and into the large hall. Then turn left and go up the stairs. Continue straight until you see a staircase on your left, use this to go up one floor. Exit on your right through the glass door into the hallway, and turn left. Follow the hallway until the end and turn left. Follow this hallway until the end and turn left again. Continue straight until you see room C3413 on the right side. The room number is C 3413"

directions_dict = {
    "bob":bob_dir,
    "dirk":dirk_dir,
    "mariet":mariet_dir,
    "dennis":dennis_dir,
    "daniel":daniel_dir,
    "cristina_shortcut":cristina_shortcut_dir,
    "cristina_longcut":cristina_longcut_dir,
    "edwin":edwin_longcut_dir
}

### Verification/acceptance
q_understand = "Did you understand the directions?"
q_understand2 = "Did you find the directions useful?"


### Goodbye
bye = "Goodbye, have a nice day."
recommend = "I'm having trouble understanding the question, I would recommend downloading the Campus app on your smartphone."


### Dictionary with all utterances
utterance_dict = {
    "greet": greeting,
    "not_understand": not_understand,
    "not_understand_at_all": not_understand_at_all,
    "bob_validation": validations[0],
    "dirk_validation": validations[1],
    "mariet_validation": validations[2],
    "dennis_validation": validations[3],
    "daniel_validation": validations[4],
    "cristina_validation": validations[5],
    "edwin_validation": validations[6],
    "bob_confirmation": professor_confirmations[0],
    "dirk_confirmation": professor_confirmations[1],
    "mariet_confirmation": professor_confirmations[2],
    "dennis_confirmation": professor_confirmations[3],
    "daniel_confirmation": professor_confirmations[4],
    "cristina_confirmation": professor_confirmations[5],
    "edwin_confirmation": professor_confirmations[6],
    "bob_repeat": professor_repeats[0],
    "dirk_repeat": professor_repeats[1],
    "mariet_repeat": professor_repeats[2],
    "dennis_repeat": professor_repeats[3],
    "daniel_repeat": professor_repeats[4],
    "cristina_repeat": professor_repeats[5],
    "edwin_repeat": professor_repeats[6],
    "bob_direction": bob_dir,
    "dirk_direction": dirk_dir,
    "mariet_direction": mariet_dir,
    "dennis_direction": dennis_dir,
    "daniel_direction": daniel_dir,
    "cristina_shortcut_direction": cristina_shortcut_dir,
    "cristina_longcut_direction": cristina_longcut_dir,
    "edwin_direction": edwin_longcut_dir,
    "horst_validation": horst_shortcut_validation,
    "q_understand": q_understand,
    "bye": bye,
    "recommend": recommend
}


# Text-to-speech all of it
all_utterances = [
    greeting,
    not_understand, not_understand_at_all,
    bob_dir, dirk_dir, mariet_dir, dennis_dir, daniel_dir, cristina_shortcut_dir, cristina_longcut_dir, edwin_longcut_dir,
    horst_shortcut_validation,
    q_understand, q_understand2,
    bye, recommend
]



def text_to_audiofile():
    """Synthesizes speech from the input string of text or ssml.
    Make sure to be working in a virtual environment.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_inputs = [texttospeech.SynthesisInput(text=text) for text in all_utterances+validations+professor_confirmations]

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    ######## Write multiple audio files #########
    # # Perform the text-to-speech request on the text input with the selected
    # # voice parameters and audio file type
    # responses = [client.synthesize_speech(
    #     input=synthesis_input, voice=voice, audio_config=audio_config
    # ) for synthesis_input in synthesis_inputs]

    # # The response's audio_content is binary.
    # for i, response in enumerate(responses):
    #     with open(f"output{i+1}.mp3", "wb") as out:
    #         # Write the response to the output file.
    #         out.write(response.audio_content)
    #         print('Audio content written to file')


    ######## Write single audio file #########
    synthesis_input = texttospeech.SynthesisInput(text=professor_repeats[6])
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open("mp3s/edwin_repeat.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio written to file.")

# text_to_audiofile()