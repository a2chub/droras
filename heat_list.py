#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

HEAT_COUNT = 3
ROUND_ID = 6


r6_data = ''' J18106 Open  冨谷 利光  Open  1
J17018 Open  杉山 健一  Open  1
J17024 Open  永塚 正樹  Open  1
none Open  None  Open  2
J18110 Open  福山 武治  Open  2
J18135 Open  鈴木 紀文  Open  2
J18109 Open  阿部 恭弘  Open  3
J18143 Open  中山 英司  Open  3
J18139 Oepn  佐藤 姫夏  Open  3
J18140 Open  中畑 健一  Open  4
J19206 Open  松留 貴文  Open  4
J17042 Exp  高坂 卓光  Expert  4
J18144 Exp  魚住 伸一  Expert  5
J18145 Exp  黒田 正義  Expert  5
J19228 Exp  齋藤 三佳  Expert  5
J17009 Exp  中村 敦  Expert  6
J17001 Exp  井上 裕二  Expert  6
J17037 Exp  須藤 公貴  Expert  6
J18108 Exp  佐藤 茂貴  Expert  7
J17080 Exp  白石 麻衣  Expert  7
J18126 Exp  中川 絵梨  Expert  7
J17076 Exp  冨塚 一行  Expert  8
J19212 Exp  犬飼 豊紀  Expert  8
J17023 Exp  松橋 伸行  Expert  8
J17040 Pro  小山 智彦  Pro  9
J17068 Pro  村上 元章  Pro  9
J18115 Pro  山田 開人  Pro  9
J17030 Pro  岡 聖章  Pro  10
J17043 Pro  高梨 智樹  Pro  10
J17071 Pro  川田 和輝  Pro  10
J19205 Pro  犬飼 明範  Pro  11
J17070 Pro  上関 風雅  Pro  11
J18129 Pro  高野 奏多  Pro  11
J17007 Pro  高橋 亨  Pro  12
J18103 Pro  小松 良誠  Pro  12
J17049 Pro  加藤 和幸  Pro  12 '''

r5_data = '''J17026  山崎 鉄兵  Open  1
J19253  楠本 竜也  Open  1
J17032  小池 卓三  Open  1
J19252  西脇 慎一  Open  2
J19250  清水 友理香  Open  2
J19249  重光 真吾  Open  2
J19248  石村 圭史  Open  3
J19247  梅野 吉則  Open  3
J19246  清水 煌世  Open  3
J19245  津村 昇二郎  Open  4
J17056  矢野 正樹  Open  4
J19217  田村 照明  Open  4
J19244  葛井 重直  Open  5
J17055  石井 弦  Open  5
J18127  田村 聡  Open  5
J19225  岡 貴司  Open  6
J19229  下鳥 遼  Open  6
J17054  笠原 康弘  Open  6
J19242  大塚 昌広  Open  7
J19241  藤田 好紀  Open  7
J19240  水戸 隆仁  Open  7
J19239  古川 稔  Open  8
J18102  江連 孝博  Open  8
J19238  福井 創太  Open  8
J19216  原 俊平  Open  9
J19206  松留 貴文  Open  9
キャンセル  小澤 諒祐  Open  9
J19224  永田 貴之  Expert  10
J18119  谷川 一成  Expert  10
J19251  三村 尚幸  Expert  10
J17053  川原 俊浩  Expert  11
J19243Open  上地 和憲  Open  11
J19213  木脇 文裕  Expert  11
J17009  中村 敦  Expert  12
J17023  松橋 伸行  Expert  12
J19228  齋藤 三佳  Expert  12
J18121  澤田 雅司  Expert  13
J17088  牧野 裕之  Expert  13
J17057  枡井 孝宏  Expert  13
J17080  白石 麻衣  Expert  14
J19214  小塚 研采  Expert  14
J19237  矢田 篤幹  Expert  14
J19210  岸本 貴子  Expert  15
J17059  芳之内 剛  Expert  15
J18126  中川 絵梨  Expert  15
J18101  矢沢 将紀  Expert  16
J19212  犬飼 豊紀  Expert  16
J19218  螻川内 努  Expert  16
J17030  岡 聖章  Pro  17
無し  無し    17
J17049  加藤 和幸  Pro  17
J17068  村上 元章  Pro  18
無し  無し    18
J19205  犬飼 明範  Pro  18
J18115  山田 開人  Pro  19
J17071  川田 和輝  Pro  19
J17075  荒川 大  Pro  19
J17007  高橋 亨  Pro  20
J17070  上関 風雅  Pro  20
J17043  高梨 智樹  Pro  20 '''

r4_data = '''J17034  高橋 阿岐寿  open  1
J19236  依田 邦章  open  1
J19235  松下 祐介  open  1
J19208  井上 亨太朗  open  2
J19207  鈴木 泰彦  open  2
J17048  八城 吉徳  open  2
J19204  清 正憲  open  3
J19211  倉岡 幸博  open  3
J17031  黒川 新介  open  3
J19232  田向 義和  open  4
J17019  新藤 正  open  4
J17024  永塚 正樹  open  4
J17073  富岡 幸一郎  open  5
J17086  土田 徳信  open  5
J19206  松留 貴文  open  5
J19202  細内 草太  open  6
J19227  千葉 秀之  open  6
J17032  小池 卓三  open  6
J18106  冨谷 利光  open  7
J17077  武田 圭史  open  7
J17087  浅井 章喜  open  7
J17072  千葉 栄治  open  8
J17023  松橋 伸行  open  8
J17063  松本 英三郎  open  8
J17018  杉山 健一  open  9
J19226  吉田 莉都  open  9
    open  9
J19228  齋藤 三佳  expert  10
J17001  井上 裕二  expert  10
    expert  10
J17090  倉橋 幸慎  expert  11
J17014  上野 まさひろ  expert  11
J18114  百瀬 徹  expert  11
J17088  牧野 裕之  expert  12
J17009  中村 敦  expert  12
J17039  逸見 鈴利  expert  12
J17010  吉田 哲生  expert  13
    expert  13
J18101  矢沢 将紀  expert  13
J19205  犬飼 明範  expert  14
J17080  白石 麻衣  expert  14
J19212  犬飼 豊紀  expert  14
J17092  井上 正行  expert  15
J19218  螻川内 努  expert  15
J17013  三浦 喜徳  expert  15
J18115  山田 開人  pro  16
J17038  阿左美 和馬  pro  16
J17070  上関 風雅  pro  16
J17030  岡 聖章  pro  17
J18103  小松 良誠  pro  17
J17071  川田 和輝  pro  17
J18126  中川 絵梨  pro  18
J18129  高野 奏多  pro  18
J17049  加藤 和幸  pro  18
J17068  村上 元章  pro  19
J17021  鈴木 匠  pro  19
J17075  荒川 大  pro  19
J17043  高梨 智樹  pro  20
J17007  高橋 亨  pro  20
J17040  小山 智彦  pro  20'''



r3_data = '''J19211  倉岡 幸博  Open  1
J19228  齋藤 三佳  Open  1
J19207  鈴木 泰彦  Open  1
J19206  松留 貴文  Open  2
J18127  田村 聡  Open  2
J17086  土田 徳信  Open  2
J18135  鈴木 紀文  Open  3
J18106  冨谷 利光  Open  3
J19202  細内 草太  Open  3
J17090  倉橋 幸慎  Open  4
J17004  藤山 貴敬  Open  4
J19227  千葉 秀之  Open  4
J17019  新藤 正  Open  5
J17018  杉山 健一  Open  5
J19209  川田 哲也  Open  5
J18132  五十嵐 朝哉  Open  6
J19226  吉田 莉都  Open  6
J17032  小池 卓三  Open  6
J17024  永塚 正樹  Open  7
J19203  松本 麻希  Open  7
J19225  岡 貴司  Open  7
J17048  八城 吉徳  Open  8
J17023  松橋 伸行  Open  8
J17063  松本 英三郎  Open  8
J18126  中川 絵梨  Expert  9
J17037  須藤 公貴  Expert  9
J17014  上野 まさひろ  Expert  9
J17017  小河 匡史  Expert  10
J17080  白石 麻衣  Expert  10
J17013  三浦 喜徳  Expert  10
J17016  大鳥 浩史  Expert  11
J19214  小塚 研采  Expert  11
J18101  矢沢 将紀  Expert  11
J18114  百瀬 徹  Expert  12
J17051  岡田 祐哉  Expert  12
J18133  播磨 靖之  Expert  12
J18125  Andy Nguyen  Expert  13
J17076  冨塚 一行  Expert  13
J17042  高坂 卓光  Expert  13
J17088  牧野 裕之  Expert  14
J17010  吉田 哲生  Expert  14
J19205  犬飼 明範  Expert  14
J17075  荒川 大  Expert  15
J19212  犬飼 豊紀  Expert  15
J17001  井上 裕二  Expert  15
J17030  岡 聖章  Pro  16
None  None  Pro  16
J18115  山田 開人  Pro  16
J17021  鈴木  匠  Pro  17
J17038  阿左美 和馬  Pro  17
J18103  小松 良誠  Pro  17
J18129  高野 奏多  Pro  18
J17068  村上 元章  Pro  18
J17040  小山 智彦  Pro  18
J17071  川田 和輝  Pro  19
J17049  加藤 和幸  Pro  19
J17007  高橋 亨  Pro  19
J17070  上関 風雅  Pro  20
J17043  高梨 智樹  Pro  20
J17009  中村 敦  Pro  20'''

def get_heat(h_idx):
  heat_data =  make_heat()
  h_idx = int(h_idx)
  if h_idx < 1:
    h_idx = len(heat_data)
  elif h_idx > len( heat_data ):
    h_idx = 1
  else:
    h_idx = h_idx
  return heat_data[h_idx -1]


def make_heat():
  print('start "make_heat"')
  global HEAT_COUNT, ROUND_ID
  all_pilot = get_round_data(ROUND_ID)
  heat_cnt = 0
  race_arr = []
  one_heat = []
  for i in range( len(all_pilot)):
    one_heat.append( all_pilot[i] )
    heat_cnt += 1
    if heat_cnt == HEAT_COUNT:
      race_arr.append( one_heat )
      one_heat = []
      heat_cnt = 0
  return race_arr


def get_round_data(round_id):
  race_dict = []
  row_data = eval('r%s_data'%(round_id)).split('\n')
  for i in row_data:
    pilot = i.split('  ')
    one_pilot = {
        "heat" : pilot[3],
        "JDL_ID" : pilot[0],
        "class" : pilot[2],
        "name" : pilot[1]
        }
    race_dict.append(one_pilot)
  return race_dict


if __name__ == "__main__":
  #print( get_round_data(5))
  print( json.dumps(make_heat(), indent=2, ensure_ascii=False))
  print( get_heat(1) )
