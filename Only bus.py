import interactions
import aiohttp
import xml.etree.ElementTree as ET
import asyncio
import os
import json


DISCORD_TOKEN = f'님의 디코 봇 토큰'
BUS_API_KEY = f'버스 API 인증키'
StopID = 180750201 # 차고지(백운포) 방면 경성대학교입구 정류장
LineID_22 = 5200022000 # 22번 버스 노선 아이디
LineID_27 = 5200027000 # 27번 버스 노선 아이디
BUS_API_URL_22 = f'http://apis.data.go.kr/6260000/BusanBIMS/busStopArrByBstopidLineid?serviceKey={BUS_API_KEY}&lineid={LineID_22}&bstopid={StopID}'
BUS_API_URL_27 = f'http://apis.data.go.kr/6260000/BusanBIMS/busStopArrByBstopidLineid?serviceKey={BUS_API_KEY}&lineid={LineID_27}&bstopid={StopID}'

# 봇 초기화
bot = interactions.Client(token=DISCORD_TOKEN, intents=interactions.Intents.ALL)


# JSON 파일에서 메시지 설정 불러오기
def load_messages(filename=None):
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), "bus_car_info.json")
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# 메시지 설정 로드
bus_car_info = load_messages()

# 특정 번호판에 따른 메시지 추가
def get_bus_car_info(bus_number, bus_no):
    # bus_number와 bus_no 써서 JSON 파일에서 차량정보 찾기
    if str(bus_number) in bus_car_info:
        return bus_car_info[str(bus_number)].get(bus_no, "")
    return ""


# 버스 정보 가져오기 
async def get_bus_info(api_urls):
    buses_data = []
    async with aiohttp.ClientSession() as session:
        for api_url in api_urls:
            async with session.get(api_url) as response:
                print(f"Response status: {response.status}")
                data = await response.text()
                print(f"Response data: {data}")

                if response.status == 200:
                    buses_data.append(data)  # XML 처리
                else:
                    buses_data.append(None)
    return buses_data

# XML 데이터 처리 
def parse_bus_info(xml_data, bus_number):
    root = ET.fromstring(xml_data)
    items = root.find('.//items/item')

    if items is not None:
        buses_info = [f"🚌 {bus_number}번 버스:"]
        for i in range(1, 3):  # 첫 번째와 두 번째 버스 정보만 가져오기
            bus_no = items.find(f'carno{i}')
            min_away = items.find(f'min{i}')
            station_behind = items.find(f'station{i}')
            lowplate = items.find(f'lowplate{i}')

            if bus_no is not None and min_away is not None:
                # 특정 번호판 메시지 추가
                special_message = get_bus_car_info(bus_number, bus_no.text)
                
                buses_info.append(f"🚍 [{i}차 버스] {bus_no.text}호\n"
                                  f"    ⏳ 도착까지: {min_away.text}분\n"
                                  f"    📍 현재 위치: {station_behind.text}정거장 뒤\n"
                                  f"    📃 차량에 관하여: {special_message}")

        return "\n\n".join(buses_info)
    return f"🚌 {bus_number}번 버스 정보를 찾을 수 없습니다."

# 22번 및 27번 버스 도착 정보
@interactions.slash_command(name="버스정보", description="경성대학교입구 정류장의 버스 도착 정보를 확인합니다.")
async def 경여중(ctx: interactions.SlashContext):
    await ctx.defer()
    api_urls = [BUS_API_URL_22, BUS_API_URL_27]
    bus_numbers = ["22", "27"]
    data_list = await get_bus_info(api_urls)

    response_messages = []
    for index, data in enumerate(data_list):
        if data:
            # 버스 번호를 넘기면서 메시지 조회
            bus_info = parse_bus_info(data, bus_numbers[index])
            response_messages.append(bus_info)
        else:
            response_messages.append(f"🚌 {bus_numbers[index]}번 버스 정보를 가져오는 데 실패했습니다.")

    await ctx.send("\n\n".join(response_messages))

# 봇 실행
if __name__ == "__main__":
    print('starting bot...')
    bot.start()
