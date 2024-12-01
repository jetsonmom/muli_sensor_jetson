import Jetson.GPIO as GPIO
import time
from CM1106_lib import CM1106
# import CM1106 라이브러리만 가져오는 코드로 미세먼지값은 이곳에서 
# GPIO 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
DUST_PIN = 12

def setup():
    GPIO.setup(DUST_PIN, GPIO.IN)
    print("GPIO 초기화 완료")

def main():
    # CO2 센서 초기화
    co2_sensor = CM1106(port='/dev/ttyTHS1')
    
    # 미세먼지 센서 변수
    duration = 0
    lowpulseoccupancy = 0
    starttime = time.time() * 1000
    sampletime_ms = 3000  # 3초
    
    print("\n=== 센서 모니터링 시작 ===")
    
    try:
        while True:
            # CO2 측정
            co2_value = co2_sensor.read_co2()
            
            # 미세먼지 측정
            if GPIO.input(DUST_PIN) == GPIO.LOW:
                duration = time.time() * 1000
                while GPIO.input(DUST_PIN) == GPIO.LOW:
                    time.sleep(0.0001)
                duration = (time.time() * 1000) - duration
                lowpulseoccupancy += duration
            
            current_time = time.time() * 1000
            if (current_time - starttime) > sampletime_ms:
                # 미세먼지 농도 계산
                ratio = lowpulseoccupancy / (sampletime_ms * 10.0)
                dust_concentration = 1.1 * pow(ratio, 3) - 3.8 * pow(ratio, 2) + 520 * ratio + 0.62
                
                # 결과 출력
                print("\n=== 측정 결과 ===")
                print(f"시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"CO2 농도: {co2_value} ppm")
                print(f"미세먼지 농도: {dust_concentration:.2f} pcs/L")
                
                # 변수 초기화
                lowpulseoccupancy = 0
                starttime = current_time
            
            time.sleep(0.001)
            
    except KeyboardInterrupt:
        print("\n프로그램 종료")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    setup()
    main()
