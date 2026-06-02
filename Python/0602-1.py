class Car:
    def __init__(self, make, model, color, price):
        self.make = make      # 제조사
        self.model = model    # 모델
        self.color = color    # 색상
        self.price = price    # 가격

    def setMake(self, make):      # 설정자(setter)
        self.make = make

    def getMake(self):            # 접근자(getter)
        return self.make

    def getDesc(self):            # 정보를 문자열로 요약
        return "차량 =(" + str(self.make) + "," + \
               str(self.model) + "," + \
               str(self.color) + "," + \
               str(self.price) + ")"


# 자식 클래스: Car를 상속받아 배터리 기능 추가
class ElectricCar(Car):                                  # (1) Car를 상속
    def __init__(self, make, model, color, price, batterySize):
        super().__init__(make, model, color, price)      # (2) 부모 생성자 호출
        self.batterySize = batterySize                   # (3) 내 변수 추가

    def setBatterySize(self, batterySize):
        self.batterySize = batterySize

    def getBatterySize(self):
        return self.batterySize


# 사용해보기
myCar = ElectricCar("Tisla", "Model S", "white", 10000, 0)
myCar.setMake("Tesla")          # 부모에게서 물려받은 메소드
myCar.setBatterySize(60)        # 자식이 새로 만든 메소드
print(myCar.getDesc())          # 부모 메소드 호출
print("배터리 용량:", myCar.getBatterySize())