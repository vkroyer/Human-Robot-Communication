/*  Example code for the Social Robot Interaction course
    Code Written by Sjoerd de Jong

    Connections:
    MP3 MODULE    -> D2
    LED EYES      -> D3
    SERVOS        -> D6
    TOUCH_SENSOR  -> A0
    HUSKY_LENS    -> I2C
*/

// --------------------------------------------------------------------------------- //
// ---------------------------------- EYE PATTERNS --------------------------------- //
// --------------------------------------------------------------------------------- //
// We store the different eyes as a byte array, which is both space-efficient and readable
// You can also use https://sjoerd.tech/eyes/ to quickly design your own eye patterns
byte neutral[] = {
  B0000,
  B01110,
  B011110,
  B0111110,
  B011110,
  B01110,
  B0000
};

byte blink1[] = {
  B0000,
  B00000,
  B011110,
  B0111110,
  B011110,
  B00000,
  B0000
};

byte blink2[] = {
  B0000,
  B00000,
  B000000,
  B1111111,
  B000000,
  B00000,
  B0000
};

byte blinkbig1[] = {
  B0000,
  B11111,
  B111111,
  B1111111,
  B111111,
  B11111,
  B0000
};

byte blinkbig2[] = {
  B0000,
  B00000,
  B111111,
  B1111111,
  B111111,
  B00000,
  B0000
};

byte blinkbig3[] = {
  B0000,
  B00000,
  B000000,
  B1111111,
  B000000,
  B00000,
  B0000
};

byte rubberduck[] = {
  B1111,
  B11111,
  B111111,
  B1111111,
  B111111,
  B11111,
  B1111
};

byte happy[] = {
  B1111,
  B11111,
  B111111,
  B1100011,
  B000000,
  B00000,
  B0000
};

byte angry[] = {
  B0000,
  B10000,
  B110000,
  B1111000,
  B111110,
  B11111,
  B1111
};

byte sad[] = {
  B0000,
  B00001,
  B000011,
  B0001111,
  B011111,
  B11111,
  B1111
};

byte dead[] = {
  B0000,
  B00000,
  B000000,
  B0000000,
  B000000,
  B00000,
  B0000
};

// --------------------------------------------------------------------------------- //
// ----------------------------------- VARIABLES ----------------------------------- //
// --------------------------------------------------------------------------------- //
// Let's start by including the needed libraries
#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include "HUSKYLENS.h"
#include <Servo.h> 

// Then we define global constants
#define LED_PIN       4
#define NUMPIXELS    74
#define TOUCH_PIN     A0
#define SERVO_PIN_1   6
#define SERVO_PIN_2   7

// And the rest
SoftwareSerial mp3(2, 3);                     // The MP3 module is connected on pins 2 and 3
Adafruit_NeoPixel pixels(NUMPIXELS, LED_PIN);

HUSKYLENS huskylens;
HUSKYLENSResult face;
bool face_detected = false;
bool prev_touch_value = 0;

enum Emotion {NEUTRAL, ANGRY, RUBBERDUCK, SAD, HAPPY, DEAD};
Emotion emotion = NEUTRAL;

Servo servo1, servo2;
float servo1_pos = 90, servo2_pos = 90;
float servo1_target = 90, servo2_target = 90;
float servo1_speed = 0, servo2_speed = 0;

long timer1, timer2, timer3;

bool pc_connected = false;
float servo1_target_pc = 90, servo2_target_pc = 90;

int prev_mode = 1;
int mode = 1;
long mode_timer;

bool running = true;

// --------------------------------------------------------------------------------- //
// ------------------------------------- SETUP ------------------------------------- //
// --------------------------------------------------------------------------------- //
void setup() {
  // put your setup code here, to run once:
  pinMode(TOUCH_PIN, INPUT);

  // Initialize the leds
  pixels.begin();

  // Serial communication
  Serial.begin(115200);

  // HuskyLens
  Wire.begin();
  while (!huskylens.begin(Wire)) {
      Serial.println(F("Begin failed!"));
      Serial.println(F("1.Please recheck the \"Protocol Type\" in HUSKYLENS (General Settings>>Protocol Type>>I2C)"));
      Serial.println(F("2.Please recheck the connection."));
      delay(100);
  }

  // Servos
  servo1.attach(SERVO_PIN_1);
  servo2.attach(SERVO_PIN_2);
  servo1.write(90);
  servo2.write(90);
}

// --------------------------------------------------------------------------------- //
// ----------------------------------- MAIN LOOP ----------------------------------- //
// --------------------------------------------------------------------------------- //
void loop() {
  // put your main code here, to run repeatedly:

  // Ever 20 milliseconds, update the servos
  if (millis() - timer1 >= 20){
    timer1 = millis();
    run_emotions();
    husky_lens();
    if (running) {
      move_servos();
    }
  }

  // Every 10 milliseconds, do stuff
  if (millis() - timer2 >= 10){
    timer2 = millis();
    mode = read_mode();
    if (mode != -1) {
      change_mode(mode);
    }
  }
}

// --------------------------------------------------------------------------------- //
// ------------------------------- SERIAL MODE PICKER ------------------------------ //
// --------------------------------------------------------------------------------- //
int read_mode(){
  String data = "";
  if (Serial.available() > 0) {
    data = Serial.readString();
    if (data=="" || data.toInt()>5 || data.toInt()<0){
      return -1;
    }
    else if (data.toInt()==5) {
      running = false;
    }
    else {
      running = true;
    }
    mode = data.toInt();

    Serial.print("Recieved mode: ");
    Serial.println(mode);
    return mode;
  }
}

void change_mode(int mode) {
  // Switch back to neutral mode after a specified number of seconds
  int seconds_in_mode = 5;
  if (millis()-mode_timer > 1000*seconds_in_mode && mode==prev_mode && mode!=RUBBERDUCK && mode!=DEAD) {
    emotion = NEUTRAL;
    return;
  } else if (mode == prev_mode) {
    return;
  }

  switch (mode) {
    case NEUTRAL:
      emotion = NEUTRAL;
      break;
    case ANGRY:
      emotion = ANGRY;
      mode_timer = millis();
      break;
    case RUBBERDUCK:
      emotion = RUBBERDUCK;
      break;
    case SAD:
      emotion = SAD;
      mode_timer = millis();
      break;
    case HAPPY:
      emotion = HAPPY;
      mode_timer = millis();
      break;
    case DEAD:
      emotion = DEAD;
      break;
  }
  prev_mode = mode;
}

// --------------------------------------------------------------------------------- //
// -------------------------------- DO THE EMOTION --------------------------------- //
// --------------------------------------------------------------------------------- //
void run_emotions(){
  pixels.clear();

  int neutralBrightness = 2;
  int duckyBrightness = 6;
  int attentionBrightness = 6;
  int angryBrightness = 60;

  switch (emotion) {
    case NEUTRAL:
      servo1_target = 90;
      servo2_target = 90;
      if (millis() % 5000 < 150) display_eyes(blink1, 150, neutralBrightness);
      else if (millis() % 5000 < 300) display_eyes(blink2, 150, neutralBrightness);
      else if (millis() % 5000 < 450) display_eyes(blink1, 150, neutralBrightness);
      else display_eyes(neutral, 150, neutralBrightness);
      break;
    case HAPPY:
      display_eyes(happy, 80, attentionBrightness);
      
      servo1_target = 90 + 10.0 * sin(millis() / 500.00);
      servo2_target = 80 + 15.0 * cos(millis() / 400.00);
      break;
    case SAD:
      display_eyes(sad, 125, attentionBrightness);
      
      servo1_target = 90 + 3.0 * sin(millis() / 400.00);
      servo2_target = 120 + 20.0 * cos(millis() / 500.00);
      break;
    case ANGRY:
      display_eyes(angry, 0, angryBrightness);

      servo1_target = 90 + 10.0 * sin(millis() / 250.00);
      servo2_target = 110 + 15.0 * cos(millis() / 175.00);
      break;
    case RUBBERDUCK:
      if (millis() % 5000 < 50) display_eyes(blinkbig1, 37, duckyBrightness);
      else if (millis() % 5000 < 100) display_eyes(blinkbig2, 37, duckyBrightness);
      else if (millis() % 5000 < 150) display_eyes(blinkbig3, 37, duckyBrightness);
      else if (millis() % 5000 < 200) display_eyes(blinkbig2, 37, duckyBrightness);
      else if (millis() % 5000 < 250) display_eyes(blinkbig1, 37, duckyBrightness);
      else display_eyes(rubberduck, 37, duckyBrightness);

      if (face_detected) {
        servo1_target = 90.0 + float(face.xCenter - 160) / 320.00 * -50.00;
        servo2_target = 90.0 + float(face.yCenter - 120) / 240.00 * 50.00;
      }
      break;
    case DEAD:
      display_eyes(dead, 0, 0);
      break;
  }

  pixels.show();
}

// --------------------------------------------------------------------------------- //
// -------------------------------------- EYES ------------------------------------- //
// --------------------------------------------------------------------------------- //
void display_eyes(byte arr[], int hue, int ledBrightness){
   display_eye(arr, hue, true, ledBrightness);
   display_eye(arr, hue, false, ledBrightness);
}

void display_eye(byte arr[], int hue, bool left, int ledBrightness) {
  // We will draw a circle on the display
  // It is a hexagonal matrix, which means we have to do some math to know where each pixel is on the screen

  int rows[] = {4, 5, 6, 7, 6, 5, 4};      // The matrix has 4, 5, 6, 7, 6, 5, 4 rows.
  int NUM_COLUMNS = 7;                     // There are 7 columns
  int index = (left) ? 0 : 37;             // If we draw the left eye, we have to add an offset of 37 (4+5+6+7+6=5+4)
  for (int i = 0; i < NUM_COLUMNS; i++) {
    for (int j = 0; j < rows[i]; j++) {
      int brightness = ledBrightness * bitRead(arr[i], (!left) ? rows[i] - 1 - j : j);
      pixels.setPixelColor(index, pixels.ColorHSV(hue * 256, 255, brightness));
      index ++;
    }
  }
}


// --------------------------------------------------------------------------------- //
// ----------------------------------- HUSKY LENS ---------------------------------- //
// --------------------------------------------------------------------------------- //
void husky_lens() {
  if (!huskylens.request()) {}
  else if (!huskylens.available()) {
//    Serial.println(F("No face appears on the screen!"));
    face_detected = false;
  } else {
//    Serial.println(F("###########"));

    // We loop through all faces received by the HuskyLens. If it's a face that we've learned (ID=1), we will track that face.
    // If no learned face is on the screen, we take the first face returned (which is the face closest to the center)
    face_detected = false;
    int face_index = 0;
    while (huskylens.available()) {
      HUSKYLENSResult result = huskylens.read();
      if (result.command == COMMAND_RETURN_BLOCK) {
//        Serial.println(String() + F("Block:xCenter=") + result.xCenter + F(",yCenter=") + result.yCenter + F(",width=") + result.width + F(",height=") + result.height + F(",ID=") + result.ID);
        if (face_index == 0 || result.ID == 1) face = result;
        face_index ++;
        face_detected = true;
        Serial.println("face detected");
      }
    }
//    Serial.println(String() + F("Block:xCenter=") + face.xCenter + F(",yCenter=") + face.yCenter + F(",width=") + face.width + F(",height=") + face.height + F(",ID=") + face.ID);
  }
}

// --------------------------------------------------------------------------------- //
// ---------------------------------- SERVO MOTORS --------------------------------- //
// --------------------------------------------------------------------------------- //
void move_servos(){
  // We apply some smoothing to the servos and limit the speed
  // We do this because abrubt movements cause a big spike in current draw
  // If we are connected to the PC, we use the PC angles. Otherwise we use the angles from the Arduino
//  float servo1_target_ = (pc_connected) ? servo1_target_pc : servo1_target;
//  float servo2_target_ = (pc_connected) ? servo2_target_pc : servo2_target;
  float servo1_target_ = servo1_target;
  float servo2_target_ = servo2_target;
  if (pc_connected) Serial.println("PC connected");

  if (abs(servo1_target_ - servo1_pos) < 1) {
    servo1.write(servo1_target_);
    servo1_pos = servo1_target_;
  } else {
    servo1_speed = constrain(constrain(servo1_target_ - servo1_pos, servo1_speed - 0.1, servo1_speed + 0.1), -1.0, 1.0);
    servo1_pos += servo1_speed;
    servo1.write(servo1_pos);
  }

  if (abs(servo2_target_ - servo2_pos) < 1) {
    servo2.write(servo2_target_);
    servo2_pos = servo2_target_;
  } else {
    servo2_speed = constrain(constrain(servo2_target_ - servo2_pos, servo2_speed - 0.1, servo2_speed + 0.1), -1.0, 1.0);
    servo2_pos += servo2_speed;
    servo2.write(servo2_pos);
  }
}
