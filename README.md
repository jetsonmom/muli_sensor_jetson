# muli_sensor_jetson
##### 2_sensor_main.py는 Grove Dust 센서용 라이브러리, Grove Dust 센서용 라이브러리를 불러와서 센서갑을 알려주는 코드이다.
##### dual_sensor_main.py는  CM1106 센서용 라이브러리만 가져오고 미세먼지는 import 안하고, 코드에서 실행한다. 

CM1106 라이브러리 파일 생성:  1.Grove Dust 센서용 라이브러리 코드를 넣고 저장
```
gedit CM1106_lib.py
```
Grove Dust 라이브러리 파일 생성:Grove Dust 센서용 라이브러리 코드를 넣고 저장
```
gedit Grove_lib.py
```
메인 실행 파일 생성:두가지를 합친 dual_sensor_main.py 만들기.
```
gedit dual_sensor_main.py
```

1. CM1106 센서용 라이브러리 코드:
```python
import serial
import time

class CM1106:
    def __init__(self, port='/dev/ttyTHS1', baudrate=9600):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
    
    def read_co2(self):
        cmd = b'\x11\x01\x01\xED'  # CM1106 읽기 명령어
        self.serial.write(cmd)
        time.sleep(0.1)
        
        if self.serial.in_waiting:
            response = self.serial.read(8)
            if len(response) == 8:
                co2 = (response[3] << 8) + response[4]
                return co2
        return None
```

2. Grove Dust 센서용 라이브러리 코드 :
```python
import Jetson.GPIO as GPIO
import time

class GroveDustSensor:
    def __init__(self, pin=12):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.IN)
        print("Grove 먼지 센서 초기화 완료")
        
        print("\n=== 먼지 센서 연결 정보 ===")
        print("VCC → 5V (2번 핀)")
        print("GND → GND (6번 핀)")
        print(f"DATA → GPIO ({pin}번 핀)")

    def read_dust(self):
        try:
            duration = 0
            lowpulseoccupancy = 0
            starttime = time.time() * 1000
            sampletime_ms = 3000  # 3초로 변경
            
            end_time = starttime + sampletime_ms
            
            while time.time() * 1000 < end_time:
                if GPIO.input(self.pin) == GPIO.LOW:
                    duration = time.time() * 1000
                    while GPIO.input(self.pin) == GPIO.LOW:
                        time.sleep(0.0001)
                    duration = (time.time() * 1000) - duration
                    lowpulseoccupancy += duration
                time.sleep(0.001)
            
            ratio = lowpulseoccupancy / (sampletime_ms * 10.0)
            concentration = 1.1 * pow(ratio, 3) - 3.8 * pow(ratio, 2) + 520 * ratio + 0.62
            
            return concentration
                
        except Exception as e:
            print(f"먼지 센서 읽기 오류: {e}")
            return None

    def cleanup(self):
        GPIO.cleanup()
```

3. 두 센서 동시 사용 코드:
```python
from CM1106_lib import CM1106
from Grove_lib import GroveDustSensor
import threading
import time

def main():
    # 센서 객체 생성
    co2_sensor = CM1106(port='/dev/ttyTHS1')
    dust_sensor = GroveDustSensor(port='/dev/ttyTHS2')
    
    def read_co2_data():
        while True:
            co2 = co2_sensor.read_co2()
            if co2:
                print(f"CO2: {co2} ppm")
            time.sleep(2)
    
    def read_dust_data():
        while True:
            dust = dust_sensor.read_dust()
            if dust:
                print(f"PM2.5: {dust} ug/m3")
            time.sleep(2)
    
    # 스레드 생성 및 시작
    co2_thread = threading.Thread(target=read_co2_data)
    dust_thread = threading.Thread(target=read_dust_data)
    
    co2_thread.start()
    dust_thread.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("프로그램 종료")
```

설치 필요한 패키지:
```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install pyserial
```

주의사항:
1. UART 포트 활성화 필요:
```bash
sudo systemctl stop nvgetty
sudo systemctl disable nvgetty
```

2. 권한 설정:
```bash
sudo usermod -a -G dialout dli
sudo chmod 666 /dev/ttyTHS1
sudo chmod 666 /dev/ttyTHS2
```

3. 각 센서의 통신 프로토콜이 정확한지 확인 필요 (데이터시트 참조)
4. 센서 연결 시 TX/RX 크로스 연결 확인

