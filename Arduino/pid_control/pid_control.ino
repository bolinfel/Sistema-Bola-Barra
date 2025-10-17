#include <Servo.h> //include library

#define sensor A0 //define sensor port
#define servo 9 // define servo port
Servo myServo;

#define maxAngle 90
#define minAngle 0

#define k1 0.07080913
#define k2 -1.06757971

float volts;
float distancia;     // posição da bola (cm ou mm)
float setpoint = 20; // posição desejada da bola
float erro, erro_anterior = 0;
float integral = 0;
float derivada;
float saida;
float deltaT;
float tempoAnterior;

#define botaoStart 8  // Botão pra iniciar o teste no pino 2
#define tempoTeste 30000//30000(30s)
 
unsigned long tempoInicio = 0;  // Tempo inicial (millis()) quando o botão é pressionado

float Kp = 3.8;
float Ki = 1;
float Kd = 2;


bool pause = true;
void setup() {
  // put your setup code here, to run once:

  pinMode(botaoStart, INPUT_PULLUP);
  pinMode(13,OUTPUT);
  Serial.begin(9600);
  myServo.write(20);
  myServo.attach(servo);
  myServo.write(maxAngle);
  delay(100);
  myServo.write(0);
  delay(100);
  myServo.write(20);
  delay(1000);

  tempoAnterior = millis();
  

}

void loop() {

  if(!digitalRead(botaoStart) == true){
    pause = false;
    tempoInicio = millis();
  }
  else{
    pause = true;
  }
  
  while(pause == false){
    //only start if sensor sees the ball

    digitalWrite(13, HIGH);
    volts = analogRead(sensor) * 5.0/1024;  // 5/1024
    
    distancia = pow((volts*k1),(1/k2)); // relação sensor -> distância
    
    unsigned long tempoAtual = millis();
    deltaT = (tempoAtual - tempoAnterior) / 1000.0; // em segundos
    tempoAnterior = tempoAtual;
    
    erro = setpoint - distancia;
    derivada = (erro - erro_anterior) / deltaT; // termo derivativo
    integral += erro * deltaT;

    saida = erro * Kp + integral * Ki + derivada * Kd;
    erro_anterior = erro;

    float angulo = constrain(map(saida, -30, 14, maxAngle, 0), 0, maxAngle);

    if (distancia > 60 || (tempoAtual-tempoInicio) >= tempoTeste){
      pause = true;
      digitalWrite(13, LOW);
    }
    else{
      pause = false;
      digitalWrite(13, HIGH);
    }
    
    myServo.write(angulo);
    Serial.print(50);
    Serial.print(",");
    Serial.print(4);
    Serial.print(",");
    Serial.println(distancia);
    delay(20);
  }
}
