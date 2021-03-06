# 시각장애인을 위한 스마트 지팡이 개발
최근 4차 산업혁명으로 IoT 혹은 인공지능과 같은 기술들은 많이 발전하고 있는 추세이다. 하지만 이 기술들은 주로 스마트 홈이나 인공지능 스피커 등 생활 속에서 상업적인 수단으로 적용되는 경우가 대다수이다. 정보화 시대에서 이러한 기술들의 적용은 상업적인 용도 뿐 아니라 이동약자 혹은 정보약자들과 같은 사회배려계층에게도 필수적으로 도움을 줘야 한다고 생각하여 해당 프로젝트를 수행하게 되었다.

# 결과물
![output](https://user-images.githubusercontent.com/33053367/41817634-e3961d5a-77d9-11e8-93c1-5b9a56ad46ef.png)

# 기능
### 전방 객체 인식 
딥러닝의 콘볼루션 신경망 (CNN)을 이용한 YOLO 알고리즘을 통해 서버에서 전방의 객체를 인식하고, 인식 결과를 사용자에게 음성으로 전달한다.
![default](https://user-images.githubusercontent.com/33053367/41817594-2b27a496-77d9-11e8-988b-95c0b25b19c5.png)

### 횡단보도 방향 안내
촬영한 사진에서 HSV변환을 통해 횡단보도의 꼭짓점을 인식하고, 선형회귀를 적용해 횡단보도가 어느 방향으로 기울어 있는지 확인한다. 인식 결과를 사용자에게 음성으로 전달해 올바른 방향으로 인도한다.
![1](https://user-images.githubusercontent.com/33053367/41817596-2b7c64a4-77d9-11e8-8449-4e4c6b90ab83.jpg) ![2](https://user-images.githubusercontent.com/33053367/41817597-2bae3f92-77d9-11e8-9077-f130a1b738ac.jpg)

### 블랙박스
라즈베리파이의 전원이 켜진 순간부터 전원이 꺼질 때까지 블랙박스 촬영을 유지한다. 
![default](https://user-images.githubusercontent.com/33053367/41817595-2b50e1f8-77d9-11e8-9ae1-806fa05a2aa3.gif)

### SOS 요청
STT를 이용하여 보호자의 전화번호를 음성으로 입력받는다. 사용자가 SOS 버튼을 누르면 그 순간의 전방 사진과 사용자의 위치를 안내하는 Google map URL을 보호자에게 MMS로 전송한다.

### 장애물 인식
지속적으로 전방의 장애물까지의 거리를 측정하고, 이동평균필터를 통해 이상값을 제거한다. 상단의 초음파 센서 1개는 빠르게 다가오는 물체를 인식하고, 하단의 초음파 센서 3개는 일정 거리 이하의 장애물을 인식하여 진동 모터로 사용자에게 알림을 전달한다.
![obstacledetection](https://user-images.githubusercontent.com/33053367/41817608-7fb8c512-77d9-11e8-892b-2763eb55721b.JPG)

# 시연 영상
[![Video Label](https://img.youtube.com/vi/k6lEb8ufqBo/0.jpg)](https://youtu.be/k6lEb8ufqBo)

# smartcane
smartcane
