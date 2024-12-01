from CM1106_lib import CM1106
from Grove_lib import GroveDustSensor
import time

def main():
    # 센서 초기화
    co2_sensor = CM1106(port='/dev/ttyTHS1')
    dust_sensor = GroveDustSensor(pin=12)
    
    print("\n=== 센서 모니터링 시작 ===")
    print("측정 간격: 3초")
    
    try:
        while True:
            # CO2 측정
            co2_value = co2_sensor.read_co2()
            
            # 미세먼지 측정
            dust_value = dust_sensor.read_dust()
            
            # 결과 출력
            print("\n=== 측정 결과 ===")
            print(f"시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"CO2 농도: {co2_value} ppm")
            if dust_value is not None:
                print(f"미세먼지 농도: {dust_value:.2f} pcs/L")
            else:
                print("미세먼지 측정 실패")
            
            time.sleep(300)
            
    except KeyboardInterrupt:
        print("\n프로그램 종료")
        dust_sensor.cleanup()

if __name__ == "__main__":
    main()
