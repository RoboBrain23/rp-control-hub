
char input;
int mode, temp, spo2, hr;


void setup()
{
  pinMode(3, OUTPUT);
  digitalWrite(3, LOW);
  Serial.begin(9600);
}

void loop()
{
//  mode = random(1, 4);
//  temp = random(20, 30);
//  spo2 = random(80, 100);
//  hr   = random(55, 80);

//  String Message = create_Formatted_Msg();

//  Serial.write(Message.c_str());

  if (Serial.available())
  {
    input = Serial.read();
    Serial.print(input);
    switch (input)
    {
      case'F':
        digitalWrite(3, HIGH);
        break;

      case 'S':
        digitalWrite(3, LOW);
        break;
    }
  }
}


String create_Formatted_Msg()
{
  String Current_Mode_String = String(mode);
  String Temperature_String = String(temp);
  String HeartRate_String = String(spo2);
  String SPO2_String = String(hr);
  String input_String = String(input);
  
  // Format Message: #ID#Current_Mode#Temperature#Heartrate#SPO2#
  String FormattedMessage = '#' + Current_Mode_String + '#' + Temperature_String + '#' + HeartRate_String + '#' + SPO2_String + '#' + input_String+ '#' + '\n' ;

  return FormattedMessage;
}
