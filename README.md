<h1 align="center">MPIA </h>

# Блатная бригада". 
### Этот репозиторий содержит код и инструкции для создания управляемого беспилотного автомобиля на Python и Arduino. Вы можете использовать его для своих собственных экспериментов или разработки, а также изучения того, как работает управление автономным транспортом.


<p align="center">
<img  src="blob:https://web.telegram.org/93f3d0b3-36d7-4bb3-bb47-c654554ad5fd"  width="600"> </p>


# Python код
- ## Функия для определения USB порта Arduino
~~~ Python
def find_arduino_port():
    arduino_ports = [
        p.device  
        for p in serial.tools.list_ports.comports()
        if 'Serial' in p.description
    ]
    if arduino_ports:
        return arduino_ports[0] # Вернуть первый найденный Arduino порт
    
    return None
~~~ 
- ## Основная часть для отправки комманд на Arduino
~~~Python
arduino_port = find_arduino_port()

with serial.Serial(arduino_port, 9600) as ser:
    time.sleep(2)

    while True:
        command = input()
        ser.write(f'{command}'.encode())
    
~~~
<p align="left">
<img  src="https://git.kruzhok28.ydns.eu/Cr4zyden/Black-Car/raw/branch/main/images/QY5yiHBXle0.png"  width="240"> </p>

# Arduino код
- ## Функция для управления моторами
  ### На вход подаётся целочисленное значение скорости от -255 до 255 (если значение < 0, то моторы будут двигаться в обратном направлении)
    ~~~ C
    void drive(int Speed){
        analogWrite(PIN_ENA, abs(Speed)); // Устанавливаем скорость 1-го мотора
        analogWrite(PIN_ENB, abs(Speed)); // Устанавливаем скорость 2-го мотора

        if(Speed > 0){
            digitalWrite(PIN_IN1, LOW);
            digitalWrite(PIN_IN2, HIGH);
            digitalWrite(PIN_IN3, LOW);
            digitalWrite(PIN_IN4, HIGH);
        }else{
            digitalWrite(PIN_IN1, HIGH);
            digitalWrite(PIN_IN2, LOW);
            digitalWrite(PIN_IN3, HIGH);
            digitalWrit(PIN_IN4, LOW);
        }
    
    }
    ~~~
- ## Функция для поворота
  ### На вход подаётся целочисленный угол, после чего он нормируется до значений сервопривода (от 0 до 180)
  ~~~C
  void turn(int angle){
    if (angle > 180){
        angle = 180;
    }
    if (angle < 0){
        angle = 0;
    }

    servo.write(angle);
    
  }
  ~~~
- ## Функция для остановки моторов
  ~~~C
  void driver_stop(){
    digitalWrite(PIN_IN1, LOW);
    digitalWrite(PIN_IN2, LOW);
    digitalWrite(PIN_IN3, LOW);
    digitalWrite(PIN_IN4, LOW);

    servo.write(90);

  }
  ~~~
- ## Основная часть кода для обработки сигналов, отправленных с Raspberry PI
  ~~~C
  void loop() {
    // Вращаем моторы в одну сторону с разной скоростью

    if(Serial.available() > 0)
        {
            String data = Serial.readStringUntil('\n');
        
        
        if(data.startsWith("SPEED"))
        {
            String speed_str = data.substring(6);
            int Speed = speed_str.toInt();
            drive(Speed);

        }
        else if (data.startsWith("ANGLE"))
        {
            String angle_str = data.substring(6);
            int angle = angle_str.toInt();
            turn(angle);
            }
        else if(data.startsWith("STOP")){
            driver_stop();
        }
        }
  
  }
  ~~~
<p align="center">
<img  src="https://git.kruzhok28.ydns.eu/Cr4zyden/Black-Car/raw/branch/main/images/W5T2H90NbPU.png"  width="340"> </p>
