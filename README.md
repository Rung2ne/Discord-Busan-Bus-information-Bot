# (부산) 버스 정보 디스코드 봇
> 부산버스 API를 활용하여 interactions.py로 만든 디스코드 봇

![image](https://github.com/user-attachments/assets/43d29c5a-c7c0-4e91-8a92-db5fb21e85e9)


# 실행하는 데에 필요한 API, 노선 ID와 정류소 ID를 알아내는 법

> ## 1. API 발급받기
>
> https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15092750

> ## 2. 노선 ID와 정류소 ID 공통사항
>
>> 1. 마이페이지에 들어간다.
>>
>> ![image](https://github.com/user-attachments/assets/d56c62b4-04a6-4c93-9d57-e3b8657b70fb)
>>
>> 2. 마이페이지의 API 신청을 누르면 이게 뜰 것이다.
>>
>> ![image](https://github.com/user-attachments/assets/592703da-2016-4f6a-8dcf-0bdf6fba36bb)
>>
>> 3. 들어가면 활용신청 상세기능정보가 보일 것이다.
>>
>> ![image](https://github.com/user-attachments/assets/574ead09-b807-4777-a002-fe35d11ad3d1)
>> 
>> 4. 그 중에 정류소 도착정보 조회(ARS 번호)의 확인을 누르고 정보를 입력한다.
>>
>> ![image](https://github.com/user-attachments/assets/59e42464-7581-4809-a390-5281a1f55328)
>> 
>> 네이버지도로 경성대학교입구의 정류장을 검색해본 결과 ARS번호는 07010이다.
>>
>> ![image](https://github.com/user-attachments/assets/745fa29b-b2ba-4b68-a060-1bc4e2e62651)
>>
>> 5. 정보를 입력하고 미리보기를 누르면 XML파일이 나타날 것이다.
>> 뭐가 많이 뜨는데 우리가 필요한 부분은 `<bstopid>`와 `<lineid>`다.
>> ![image](https://github.com/user-attachments/assets/adff8878-6ad5-45b0-9d80-30b6bbc8795b)
>>
>> `<bstopid>180750201</bstopid>`에서 알아낸 정류장 ID는 180750201 이다.
>>
>> `<lineid>5200022000</lineid>` 에서 알아낸 노선 ID는 5200022000 이다.
>> 
>> 이것을 코드의 `StopID`와 `lineid`부분에 적으면 된다.
 #### 이런 식으로 자신이 원하는 노선 ID와 정류장 ID를 설정하면 된다.


# 차량 설명 바꾸는 법

> ## bus_car_info.json을 열고 아래의 양식으로 수정한다.
> 
> ![image](https://github.com/user-attachments/assets/d917cb78-4b8b-428e-9af6-c86102061e1c)
