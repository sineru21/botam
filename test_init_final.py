# -*- coding: utf-8 -*- 


import asyncio
import discord
import datetime
import random
from discord.ext import commands
from gtts import gTTS
#from discord.ext.commands import Bot
#from discord.voice_client import VoiceClient
'''
import sys 
reload(sys) 
sys.setdefaultencoding('cp949')
'''

if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')

	
basicSetting = []
bossData = []

bossNum = 0
chkvoicechannel = 0
chkrelogin = 0
chflg = 0

bossTime = []
tmp_bossTime = []

bossTimeString = []
bossDateString = []
tmp_bossTimeString = []
tmp_bossDateString = []

bossFlag = []
bossFlag0 = []
bossMungFlag = []
bossMungCnt = []

channel_info = []
channel_name = []
channel_id = []
channel_voice_name = []
channel_voice_id = []
channel_type = []

client = discord.Client()

def init():
	global basicSetting
	global bossData

	global bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global player
	global voice_client1
	
	global task
	
	global channel_info
	global channel_name
	global channel_voice_name
	global channel_voice_id
	global channel_id
	global channel_type
	
	tmp_bossData = []
	f = []
	
	inidata = open('test_setting.ini','r', encoding = 'utf-8')
	
	inputData = inidata.readlines()

	for i in range(inputData.count('\n')):
		inputData.remove('\n')

	basicSetting.append(inputData[0][12:])
	basicSetting.append(inputData[1][15:])
	basicSetting.append(inputData[3][10:])
	basicSetting.append(inputData[2][15:])

	for i in range(len(basicSetting)):
		basicSetting[i] = basicSetting[i].strip()
	
	#print (inputData, len(inputData))
	
	bossNum = int((len(inputData)-4)/5)
	
	#print (bossNum)
	
	for i in range(bossNum):
		tmp_bossData.append(inputData[i*5+4:i*5+9])
		
	#print (tmp_bossData)
		
	for j in range(bossNum):
		for i in range(len(tmp_bossData[j])):
			tmp_bossData[j][i] = tmp_bossData[j][i].strip()
	
	for j in range(bossNum):
		tmp_len = tmp_bossData[j][1].find(':')
		f.append(tmp_bossData[j][0][11:])
		f.append(tmp_bossData[j][1][10:tmp_len])
		f.append(tmp_bossData[j][2][13:])
		f.append(tmp_bossData[j][3][20:])
		f.append(tmp_bossData[j][4][13:])
		f.append(tmp_bossData[j][1][tmp_len+1:])
		bossData.append(f)
		f = []
	'''
	for i in range(bossNum):
		print (bossData[i][0], bossData[i][1], bossData[i][5], bossData[i][2], bossData[i][3], bossData[i][4])
	'''
		
	print ('보스젠알림시간1 : ', basicSetting[1])
	print ('보스젠알림시간2 : ', basicSetting[3])
	print ('보스멍확인시간 : ', basicSetting[2])
	
	for i in range(bossNum):
		bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		tmp_bossTime.append(datetime.datetime.now()+datetime.timedelta(days=365))
		bossTimeString.append('99:99:99')
		bossDateString.append('9999-99-99')
		tmp_bossTimeString.append('')
		tmp_bossDateString.append('')
		bossFlag.append(False)
		bossFlag0.append(False)
		bossMungFlag.append(False)
		bossMungCnt.append(0)
		
	inidata.close()

init()

nowTimeString = '1'
	
token = basicSetting[0]

#channel = basicSetting[3]
channel = ''

async def my_background_task():
	await client.wait_until_ready()

	global channel
	global nowTimeString
	
	global basicSetting
	global bossData

	global bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global player
	global voice_client1
	
	global task
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type

	while not client.is_closed:
		now = datetime.datetime.now()
		priv0 = now+datetime.timedelta(minutes=int(basicSetting[3]))
		priv = now+datetime.timedelta(minutes=int(basicSetting[1]))
		privTimeString = priv.strftime('%H:%M:%S')
		nowTimeString = now.strftime('%H:%M:%S')
		aftr = now+datetime.timedelta(minutes=int(0-int(basicSetting[2])))
		aftrTimeString = aftr.strftime('%H:%M:%S')
		#print('loop check ' + bossTime[0].strftime('%H:%M:%S') + ' ' + nowTimeString + ' ' + privTimeString, '	' + aftrTimeString)
		#print('loop check ' + str(bossTime[0]) + ' ' + str(now) + ' ' + str(priv), '	' + str(aftr))

		if channel != '':
			for i in range(bossNum):
				#print (bossData[i][0], bossTime[i])
				if bossTime[i] <= priv0 and bossTime[i] > priv:
					if basicSetting[3] != '0':
						if bossFlag0[i] == False:
							bossFlag0[i] = True
							await client.send_message(client.get_channel(channel), bossData[i][0] + ' ' + basicSetting[3] + '분 전 ' + bossData[i][3], tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림1.mp3')
				
				if bossTime[i] <= priv and bossTime[i] > now:
					if basicSetting[1] != '0' :
						if bossFlag[i] == False:
							bossFlag[i] = True
							await client.send_message(client.get_channel(channel), bossData[i][0] + ' ' + basicSetting[1] + '분 전 ' + bossData[i][3], tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '알림.mp3')
						
				if bossTime[i] <= now :
					#print ('if ', bossTime[i])
					bossMungFlag[i] = True
					tmp_bossTime[i] = bossTime[i]
					bossTimeString[i] = '99:99:99'
					bossDateString[i] = '9999-99-99'
					bossTime[i] = now+datetime.timedelta(days=365)
					embed = discord.Embed(
							description= bossData[i][0] + '탐 ' + bossData[i][4],
							color=0x00ff00
							)
					await client.send_message(client.get_channel(channel), embed=embed, tts=False)
					await PlaySound(voice_client1, './sound/' + bossData[i][0] + '젠.mp3')
				
				if bossMungFlag[i] == True:
					if (bossTime[i]+datetime.timedelta(days=-365)) <= aftr:
						if bossData[i][2] == '0':
							await client.send_message(client.get_channel(channel), bossData[i][0] + ' 미입력 됐습니다.', tts=False)
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '미입력.mp3')
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = bossMungCnt[i] + 1
							bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(0-int(basicSetting[2])+int(bossData[i][5])))
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
								description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
								color=0xff0000
								)
							await client.send_message(client.get_channel(channel), embed=embed, tts=False)
						else :
							await client.send_message(client.get_channel(channel), bossData[i][0] + ' 멍 입니다.')
							await PlaySound(voice_client1, './sound/' + bossData[i][0] + '멍.mp3')
							bossFlag[i] = False
							bossFlag0[i] = False
							bossMungFlag[i] = False
							bossMungCnt[i] = bossMungCnt[i] + 1
							bossTime[i] = nextTime = now+datetime.timedelta(hours=int(bossData[i][1]), minutes=int(0-int(basicSetting[2])+int(bossData[i][5])))
							tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
							tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
							embed = discord.Embed(
								description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
								color=0xff0000
								)
							await client.send_message(client.get_channel(channel), embed=embed, tts=False)
											
		await asyncio.sleep(1) # task runs every 60 seconds
		
async def MakeSound(saveSTR, filename):
	tts = gTTS(saveSTR, lang = 'ko')
	tts.save('./' + filename + '.mp3')
	
async def PlaySound(voiceclient, filename):
	player = voiceclient.create_ffmpeg_player(filename)
	player.start()
	while not player.is_done():
		await asyncio.sleep(1)
	# disconnect after the player has finished
	player.stop()
	
# 봇이 구동되었을 때 동작되는 코드입니다.
@client.event
async def on_ready():
	global task
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chkvoicechannel
		
	print("Logged in as ") #화면에 봇의 아이디, 닉네임이 출력됩니다.
	print(client.user.name)
	print(client.user.id)
	print("===========")

	
	#await joinVoiceChannel()
	all_channels = client.get_all_channels()
	
	for channel1 in all_channels:
		channel_type.append(str(channel1.type))
		channel_info.append(channel1)
	
	for i in range(len(channel_info)):
		if channel_type[i] == "text":
			channel_name.append(str(channel_info[i].name))
			channel_id.append(str(channel_info[i].id))
			
	for i in range(len(channel_info)):
		if channel_type[i] == "voice":
			channel_voice_name.append(str(channel_info[i].name))
			channel_voice_id.append(str(channel_info[i].id))
	'''
	for i in range(len(channel_name)):
		print (channel_name[i])
		print (channel_id[i])
	'''
	
	try:
		file = open('my_bot.db', 'r')
		beforeBossData = file.readlines()
		
		for i in range(len(beforeBossData)-1):
			for j in range(bossNum):
				if beforeBossData[i+1].find(bossData[j][0]) != -1 :
					bossMungCnt[j] = 0
				
					tmp_len = beforeBossData[i+1].find(':')
					tmp_datelen = beforeBossData[i+1].find('@')

					years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
					months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
					days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]

					hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
					minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
					seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
					
					now2 = datetime.datetime.now()

					tmp_now = datetime.datetime.now()
					tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))

					if tmp_now < now2 : 
						deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
						while now2 > tmp_now :
							tmp_now = tmp_now + deltaTime
							
					now2 = tmp_now

					
					bossTime[j] = now2
					bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
					bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')
		file.close()
		print ("<불러오기 완료>")
		#await client.send_message(client.get_channel(channel), '< ' + client.get_channel(channel).name + ' 접속완료>', tts=False)
	except IOError:
		print ("보스타임 정보가 없습니다.")
	
	#task = client.loop.create_task(my_background_task())
	
	# 디스코드에는 현재 본인이 어떤 게임을 플레이하는지 보여주는 기능이 있습니다.
	# 이 기능을 사용하여 봇의 상태를 간단하게 출력해줄 수 있습니다.
	await client.change_presence(game=discord.Game(name="반갑습니다 :D", type=1))

	
# 봇이 새로운 메시지를 수신했을때 동작되는 코드입니다.
@client.event
async def on_message(msg):
	if msg.author.bot: #만약 메시지를 보낸사람이 봇일 경우에는
		return None #동작하지 않고 무시합니다.

	global channel
	global nowTimeString

	global basicSetting
	global bossData

	global bossNum
	global chkvoicechannel
	global chkrelogin

	global bossTime
	global tmp_bossTime

	global bossTimeString
	global bossDateString
	global tmp_bossTimeString
	global tmp_bossDateString

	global bossFlag
	global bossFlag0
	global bossMungFlag
	global bossMungCnt
	
	global player
	global voice_client1
	
	global task
	
	global channel_info
	global channel_name
	global channel_id
	global channel_voice_name
	global channel_voice_id
	global channel_type
	
	global chflg
	
	id = msg.author.id #id라는 변수에는 메시지를 보낸사람의 ID를 담습니다.
	
	if chflg == 0 :
		channel = msg.channel.id #channel이라는 변수에는 메시지를 받은 채널의 ID를 담습니다.
		await client.send_message(client.get_channel(channel), '< ' + client.get_channel(channel).name + ' 접속완료>', tts=False)
		chflg = 1
	#channel = '552122588768239646'
	#print ('msg', msg, 'channel', client.get_channel(channel), '  ID', channel)
	if client.get_channel(channel) != msg.channel :
		return None
	else :
		message = await client.get_message(client.get_channel(channel), msg.id)
		
		if message.content.startswith('!채널확인'):
			ch_information = ''
			for i in range(len(channel_name)):
				ch_information += channel_name[i] + '\n'
			print (ch_information)
			embed = discord.Embed(
				title = "----- 채널 정보 -----",
				description= ch_information,
				color=0xff00ff
				)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)
		
		if message.content.startswith('!채널이동'):
			tmp_sayMessage1 = message.content
			
			for i in range(len(channel_name)):
				if  channel_name[i] == str(tmp_sayMessage1[6:]):
					channel = channel_id[i]
				
			await client.send_message(client.get_channel(channel), '< ' + client.get_channel(channel).name + ' 이동완료>', tts=False)
		
		
		modify = ''
		
		hello = message.content

		
		for i in range(bossNum):
			if message.content.startswith(bossData[i][0] +'컷'):
				if hello.find(':') != -1 :
					chkpos = hello.find(':')
					hours1 = hello[chkpos-2:chkpos]
					minutes1 = hello[chkpos+1:chkpos+3]
					now2 = datetime.datetime.now()
					tmp_now = datetime.datetime.now()
					tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
				else:
					now2 = datetime.datetime.now()
					tmp_now = datetime.datetime.now()
					
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = 0

				if tmp_now > now2 :
					tmp_now = tmp_now + datetime.timedelta(days=int(-1))
					
				if tmp_now < now2 : 
					deltaTime = datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					while now2 > tmp_now :
						tmp_now = tmp_now + deltaTime
						bossMungCnt[i] = bossMungCnt[i] + 1
					now2 = tmp_now
					bossMungCnt[i] = bossMungCnt[i] - 1
				else :
					now2 = now2 + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
							
				bossTime[i] = nextTime = now2
				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				#print (tmp_bossTimeString[i])
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
				#print (tmp_bossDateString[i])
				#await client.send_message(channel, '다음 '+ bossData[i][0] + ' ' + bossTimeString[i] + '입니다.', tts=False)
				embed = discord.Embed(
						description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
						color=0xff0000
						)
				await client.send_message(client.get_channel(channel), embed=embed, tts=False)
				
			if message.content.startswith(bossData[i][0] +'멍'):
				if hello.find(':') != -1 :
					chkpos = hello.find(':')
					hours1 = hello[chkpos-2:chkpos]
					minutes1 = hello[chkpos+1:chkpos+3]
					tmp_now = datetime.datetime.now()
					tmp_now = tmp_now.replace(hour=int(hours1), minute=int(minutes1))
					nextTime = tmp_now + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					bossTime[i] = nextTime
				else:
					nextTime = bossTime[i] + datetime.timedelta(hours = int(bossData[i][1]), minutes = int(bossData[i][5]))
					bossTime[i] = nextTime
				
				bossFlag[i] = False
				bossFlag0[i] = False
				bossMungFlag[i] = False
				bossMungCnt[i] = bossMungCnt[i] + 1
				

				tmp_bossTimeString[i] = bossTimeString[i] = nextTime.strftime('%H:%M:%S')
				tmp_bossDateString[i] = bossDateString[i] = nextTime.strftime('%Y-%m-%d')
				embed = discord.Embed(
						description= '다음 ' + bossData[i][0] + ' ' + bossTimeString[i] + '입니다.',
						color=0xff0000
						)
				await client.send_message(client.get_channel(channel), embed=embed, tts=False)
				
			if message.content.startswith(bossData[i][0] +'삭제'):
				bossTime[i] = datetime.datetime.now()+datetime.timedelta(days=365)
				tmp_bossTime[i] =  datetime.datetime.now()+datetime.timedelta(days=365)
				bossTimeString[i] = '99:99:99'
				bossDateString[i] = '9999-99-99'
				tmp_bossTimeString[i] = ''
				tmp_bossDateString[i] = ''
				bossFlag[i] = (False)
				bossFlag0[i] = (False)
				bossMungFlag[i] = (False)
				bossMungCnt[i] = 0
				await client.send_message(client.get_channel(channel), '<' + bossData[i][0] + ' 삭제완료>', tts=False)
				print ('<' + bossData[i][0] + ' 삭제완료>')
			
		if message.content.startswith('!오빠'):
			#await client.send_message(channel, '오빠달려려어어어어어어 ', tts=False)
			await PlaySound(voice_client1, './sound/오빠.mp3')
		if message.content.startswith('!언니'):
			#await client.send_message(channel, '오빠달려려어어어어어어 ', tts=False)
			await PlaySound(voice_client1, './sound/언니.mp3')
		if message.content.startswith('!형'):
			#await client.send_message(channel, '오빠달려려어어어어어어 ', tts=False)
			await PlaySound(voice_client1, './sound/형.mp3')
			
		if message.content.startswith('!분배'):
			separate_money = []
			separate_money = message.content[4:].split(" ")
			num_sep = int(separate_money[0])
			cal_tax1 = int(float(separate_money[1])*0.05)
			real_money = int(int(separate_money[1]) - cal_tax1)
			cal_tax2 = int(real_money/num_sep) - int(float(int(real_money/num_sep))*0.95)
			if num_sep == 0 :
				await client.send_message(client.get_channel(channel), '분배 인원이 0입니다. 재입력 해주세요.', tts=False)
			else :
				await client.send_message(client.get_channel(channel), '1차세금 : ' + str(cal_tax1) + '\n1차 수령액 : ' + str(real_money) + '\n분배자 거래소등록금액 : ' + str(int(real_money/num_sep)) + '\n2차세금 : ' + str(cal_tax2) + '\n인당 실수령액 : ' + str(int(float(int(real_money/num_sep))*0.95)), tts=False)
		
		if message.content.startswith('!사다리'):
			ladder = []
			ladder = message.content[5:].split(" ")
			num_cong = int(ladder[0])
			del(ladder[0])
			if num_cong < len(ladder):
				result_ladder = random.sample(ladder, num_cong)
				print (result_ladder)
				await client.send_message(client.get_channel(channel), '----- 당첨! -----\n' + str(result_ladder), tts=False)
			else:
				await client.send_message(client.get_channel(channel), '추첨인원이 총 인원과 같거나 많습니다. 재입력 해주세요', tts=False)
			
		if message.content.startswith('!메뉴'):
			embed = discord.Embed(
					title = "----- 메뉴 -----",
					description= '!채널확인\n!채널이동 [채널명]\n!소환\n!불러오기\n!초기화\n!명치\n!미예약\n!분배 [인원] [금액]\n!사다리 [뽑을인원수] [아이디1] [아이디2] ...\n\n[보스명]컷\n[보스명]컷 00:00\n[보스명]멍\n[보스명]삭제\n보스탐',
					color=0xff00ff
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)
			
		if message.content.startswith('!미예약'):
			temp_bossTime2 = []
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' :
					temp_bossTime2.append(bossData[i][0])
					
			embed = discord.Embed(
					title = "----- 미예약보스 -----",
					description= str(temp_bossTime2),
					color=0x0000ff
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)
		
			
		if message.content.startswith('!v') or message.content.startswith('!ㅍ'):
			tmp_sayMessage = message.content
			sayMessage = tmp_sayMessage[3:]
			await MakeSound(message.author.display_name +'님이' + sayMessage, './sound/say')
			await client.send_message(client.get_channel(channel), "<@" +id+ ">님이 \"" + sayMessage + "\"", tts=False)
			await PlaySound(voice_client1, './sound/say.mp3')
			
		if message.content.startswith('!명치'):
			init()
			task.cancel()
			print ('task cancle')
			#client.close()
			#print ('client close')
			task = client.loop.create_task(my_background_task())
			await client.send_message(client.get_channel(channel), '<재접속 성공>', tts=False)
			print ("<재접속 성공>")
			
			voice_channel = message.author.voice.voice_channel

			if voice_channel is not None:
				if chkvoicechannel == 0:
					voice_client1 = await client.join_voice_channel(voice_channel)
					chkvoicechannel = 1
					await PlaySound(voice_client1, './sound/hello.mp3')
				else :
					await voice_client1.disconnect()
					voice_client1 = await client.join_voice_channel(voice_channel)
					await PlaySound(voice_client1, './sound/hello.mp3')
			else:
				await client.send_message(client.get_channel(channel), '음성채널에 먼저 들어가주세요.', tts=False)
			
		#############################
		if message.content.startswith('!소환'):
			voice_channel = message.author.voice.voice_channel

			if voice_channel is not None:
				if chkvoicechannel == 0:
					voice_client1 = await client.join_voice_channel(voice_channel)
					chkvoicechannel = 1
					await PlaySound(voice_client1, './sound/hello.mp3')
				else :
					await voice_client1.disconnect()
					voice_client1 = await client.join_voice_channel(voice_channel)
					await PlaySound(voice_client1, './sound/hello.mp3')
				task = client.loop.create_task(my_background_task())
			else:
				await client.send_message(client.get_channel(channel), '음성채널에 먼저 들어가주세요.', tts=False)
				
			
				
		##################################
					
		if message.content.startswith('!초기화'):
			basicSetting = []
			bossData = []

			bossTime = []
			tmp_bossTime = []

			bossTimeString = []
			bossDateString = []
			tmp_bossTimeString = []
			tmp_bossDateString = []

			bossFlag = []
			bossFlag0 = []
			bossMungFlag = []
			bossMungCnt = []
			
			init()

			await client.send_message(client.get_channel(channel), '<초기화 완료>', tts=False)
			print ("<초기화 완료>")

		if message.content.startswith('!설정확인'):			
			setting_val = '보스젠알림시간1 : ' + basicSetting[1] + ' 분 전\n' + '보스젠알림시간2 : ' + basicSetting[3] + ' 분 전\n' + '보스멍확인시간 : ' + basicSetting[2] + ' 분 후\n'
			embed = discord.Embed(
					title = "----- 설정내용 -----",
					description= setting_val,
					color=0xff00ff
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)
			print ('보스젠알림시간1 : ', basicSetting[1])
			print ('보스젠알림시간2 : ', basicSetting[3])
			print ('보스멍확인시간 : ', basicSetting[2])


		if message.content.startswith('!불러오기'):
			try:
				file = open('my_bot.db', 'r')
				beforeBossData = file.readlines()
				
				for i in range(len(beforeBossData)-1):
					for j in range(bossNum):
						if beforeBossData[i+1].find(bossData[j][0]) != -1 :
							bossMungCnt[j] = 0
							
							tmp_len = beforeBossData[i+1].find(':')
							tmp_datelen = beforeBossData[i+1].find('@')
							
							years1 = beforeBossData[i+1][tmp_datelen+2:tmp_datelen+6]
							months1 = beforeBossData[i+1][tmp_datelen+7:tmp_datelen+9]
							days1 = beforeBossData[i+1][tmp_datelen+10:tmp_datelen+12]
							
							hours1 = beforeBossData[i+1][tmp_len+2:tmp_len+4]
							minutes1 = beforeBossData[i+1][tmp_len+5:tmp_len+7]
							seconds1 = beforeBossData[i+1][tmp_len+8:tmp_len+10]
							
							now2 = datetime.datetime.now()

							tmp_now = datetime.datetime.now()
							tmp_now = tmp_now.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))
							'''
							if tmp_now > now2 :
								tmp_now = tmp_now + datetime.timedelta(days=int(-1))
							'''
							if tmp_now < now2 : 
								deltaTime = datetime.timedelta(hours = int(bossData[j][1]), minutes = int(bossData[j][5]))
								while now2 > tmp_now :
									tmp_now = tmp_now + deltaTime
							
							now2 = tmp_now
							'''
								now2 = tmp_now
							else :
								now2 = tmp_now
								#now2 = now2.replace(year = int(years1), month = int(months1), day = int(days1), hour=int(hours1), minute=int(minutes1), second = int(seconds1))
							'''
							bossTime[j] = now2
							bossTimeString[j] = bossTime[j].strftime('%H:%M:%S')
							bossDateString[j] = bossTime[j].strftime('%Y-%m-%d')
				file.close()
				await client.send_message(client.get_channel(channel), '<불러오기 완료>', tts=False)
				print ("<불러오기 완료>")
			except IOError:
				await client.send_message(client.get_channel(channel), '<보스타임 정보가 없습니다.>', tts=False)
				print ("보스타임 정보가 없습니다.")
		
		if message.content.startswith('보스탐'):

			for i in range(bossNum):
				for j in range(bossNum):
					if bossTimeString[i] and bossTimeString[j] != '99:99:99':
						if bossTimeString[i] == bossTimeString[j] and i != j:
							tmp_time1 = bossTimeString[j][:6]
							tmp_time2 = (int(bossTimeString[j][6:]) + 1)%100
							#print ('i : ', i, ' ', bossTimeString[i], ' j : ', j, ' ', bossTimeString[j])
							if tmp_time2 < 10 :
								tmp_time22 = '0' + str(tmp_time2)
							elif tmp_time2 == 60 :
								tmp_time22 = '00'
							else :
								tmp_time22 = str(tmp_time2)
							bossTimeString[j] = tmp_time1 + tmp_time22
							#print (bossTimeString[j])
							
			datelist = bossTime
			
			temp_bossTime1 = []
			for i in range(bossNum):
				if bossTimeString[i] == '99:99:99' :
					temp_bossTime1.append(bossData[i][0])
						
			information = ''
			information1 = '----- 보스탐 정보 -----\n'
			for timestring in sorted(datelist):
				for i in range(bossNum):
					if timestring == bossTime[i]:
						if bossTimeString[i] != '99:99:99' :
							if bossData[i][2] == '0' :
								if bossMungCnt[i] == 0 :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + '\n'
									information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + '\n'
								else :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + '\n'
									information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (미입력 ' + str(bossMungCnt[i]) + '회)' + '\n'
							else : 
								if bossMungCnt[i] == 0 :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + '\n'
									information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + '\n'
								else :
									information += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + '\n'
									information1 += ' - ' + bossData[i][0] + '(' + bossData[i][1] + '.' + bossData[i][5] + ') : ' + bossTimeString[i] + ' @ ' + bossDateString[i] + ' (멍 ' + str(bossMungCnt[i]) + '회)' + '\n'

			embed = discord.Embed(
					title = "----- 보스탐 정보 -----",
					description= information,
					color=0x0000ff
					)
			embed.add_field(
					name="----- 미예약보스 -----",
					value=str(temp_bossTime1)
					)
			await client.send_message(client.get_channel(channel), embed=embed, tts=False)
			#await client.send_message(client.get_channel(channel), '----- 미예약보스 -----\n' + str(temp_bossTime1), tts=False)
			
			file = open("my_bot.db", 'w')
			file.write(information1);
			file.close()
					
		if message.content.startswith('!현재시간'):
			await client.send_message(client.get_channel(channel), datetime.datetime.now().strftime('%H:%M:%S'), tts=False)

client.run(token)