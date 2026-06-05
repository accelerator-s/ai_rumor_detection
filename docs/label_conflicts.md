# 标签冲突完整记录

> 基于 RoBERTa 模型评测，val.csv Acc=0.865，54 个错误

> 每个错误列出：错误样本 + 语义相似但标签相反的对照样本


## Event 0


### 1. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3139

**错误样本：**
       来源: val | ID: 535721996391178242 | Event: 0 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Swiss museum close to accepting #Gurlitt bequest, returning any #Nazi-looted pieces http://t.co/eCo07tfpkF via @WSJ

**同事件矛盾（val，sim=0.48）：**
       来源: val | ID: 536810390739755009 | Event: 0 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Swiss museum, German officials to announce fate of  #Gurlitt art collection at 11CET. http://t.co/7NlXiG4hcz
       矛盾点: 语义高度相似(sim=0.48)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.46）：**
       来源: train | ID: 536825396990607360 | Event: 0 | 标签: 非谣言(0)
       文本: Swiss Museum: #Gurlitt collection will be researched according to Washington Principles; looted works will be restituted.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.35）：**
       来源: val | ID: 499665704300191745 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: More startling statistics about the segregated population of #Ferguson, Mo. http://t.co/uYrldQHoj7 http://t.co/vgxuLMYDhz
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 2. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2921

**错误样本：**
       来源: val | ID: 536845753394536448 | Event: 0 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Swiss museum will accept Gurlitt art trove http://t.co/PJVU6DJXTW

**同事件矛盾（val，sim=0.62）：**
       来源: val | ID: 536810390739755009 | Event: 0 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Swiss museum, German officials to announce fate of  #Gurlitt art collection at 11CET. http://t.co/7NlXiG4hcz
       矛盾点: 语义高度相似(sim=0.62)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.66）：**
       来源: train | ID: 536812027571109888 | Event: 0 | 标签: 非谣言(0)
       文本: Swiss museum deciding on Gurlitt art trove http://t.co/WIfA6dDq3Q
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.38）：**
       来源: val | ID: 499388619425980416 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: This is #Ferguson, a suburb in America. http://t.co/GfmHLo4u5q
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


## Event 1


### 3. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2879

**错误样本：**
       来源: val | ID: 499553593041903616 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: BREAKING: #Anonymous has obtained audio files of police dispatch and EMS during the #MikeBrown shooting. Will release ASAP. #Ferguson

**同事件矛盾（val，sim=0.48）：**
       来源: val | ID: 500362679039840257 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: RT @FreeTopher: OFFICER DARREN WILSON STANDING OVER MIKE BROWN'S BODY AFTER SHOOTING HIM 9 TIMES #Ferguson http://t.co/7uAMFPdyPO
       矛盾点: 语义高度相似(sim=0.48)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.49）：**
       来源: train | ID: 499698828845780993 | Event: 1 | 标签: 非谣言(0)
       文本: Protesters asking: "what are we doing wrong" as police advance. Police dogs barking. #MikeBrown #Ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.36）：**
       来源: val | ID: 544287332061298688 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: DO NOT TWEET POLICE MOVEMENTS. Don't tweet photos of police, their faces, their location, anything. Seriously. It's simple #sydneysiege
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 4. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.1860

**错误样本：**
       来源: val | ID: 500336373833170945 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: #Ferguson police are embarking on what can only be described as an elaborate smear campaign of Michael Brown http://t.co/SaLZExqR1D

**同事件矛盾（val，sim=0.46）：**
       来源: val | ID: 499688532391526400 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: #Ferguson heavily armed police in military gear arriving on armed personnel carriers now http://t.co/GbGdrhZBlM
       矛盾点: 语义高度相似(sim=0.46)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.45）：**
       来源: train | ID: 500277382461530112 | Event: 1 | 标签: 非谣言(0)
       文本: #Ferguson, Mo., police identify Darren Wilson as the officer who killed Michael Brown last week.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.38）：**
       来源: val | ID: 524974900017373184 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Just hearing the news, thoughts today are back home with the citizens and dedicated public servants in Ottawa and across the country.
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 5. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.0761

**错误样本：**
       来源: val | ID: 500303238810574849 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Someone with better eyes than me please #checkthedatestamp on the bottom left photo. Isn't that JUNE? #Ferguson http://t.co/PTNuxY2v5B

**同事件矛盾（val，sim=0.51）：**
       来源: val | ID: 499488337338843137 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Is that a bag of chips?! #REAL RT @GinoTheGhost: May be the dopest photo of the year #Ferguson http://t.co/ZxF3zhbjHb
       矛盾点: 语义高度相似(sim=0.51)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.44）：**
       来源: train | ID: 499377813758443520 | Event: 1 | 标签: 非谣言(0)
       文本: There's a town that's a no-fly-zone with a media blackout right in the middle of our country. Let that sink in. #Ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.42）：**
       来源: val | ID: 524950455743291392 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Thinking about everyone in Ottawa right now. Please be careful and stay safe until the situation is under control.
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 6. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.1385

**错误样本：**
       来源: val | ID: 499494187969298432 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: What are #Ferguson Police hiding about "drive by" shooting of black woman recording last night's action? http://t.co/wfuDYm9q27 #OpFerguson

**同事件矛盾（val，sim=0.46）：**
       来源: val | ID: 500364705622671360 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Exactly How Often Do Police Shoot Unarmed Black Men? http://t.co/6KXMOhu2EA #Ferguson http://t.co/1Cd6egf2LQ
       矛盾点: 语义高度相似(sim=0.46)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.48）：**
       来源: train | ID: 499588291335692288 | Event: 1 | 标签: 非谣言(0)
       文本: New statement from #Ferguson police on shooting of #MichaelBrown ht @abake6 http://t.co/bGeRVUVQDO
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 0，sim=0.38）：**
       来源: val | ID: 536835870293512192 | Event: 0 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Gurlitt press release concludes. Many questions being raised by attendees on state of task force investigation and limbo nazi loot objects.
       矛盾点: Event 0 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 7. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.1527

**错误样本：**
       来源: val | ID: 498272309535191041 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: 200 cops in riot gear in #ferguson because there is a prayer circle and a concerned compassionate community

**同事件矛盾（val，sim=0.41）：**
       来源: val | ID: 498575704582148096 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: If u r white &amp; u r not outraged about #Ferguson then the problem is much bigger than the police. #americaforall
       矛盾点: 语义高度相似(sim=0.41)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.43）：**
       来源: train | ID: 499691556652449792 | Event: 1 | 标签: 非谣言(0)
       文本: Those people in #Ferguson must think they have some kind of constitutional right to protest or something.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.34）：**
       来源: val | ID: 544337283801829376 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: My thoughts are with the hostages, their families and everyone in Sydney right now.
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 8. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2165

**错误样本：**
       来源: val | ID: 500368579875704832 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: I'm so disgusted. #Ferguson RT @ZandarVTS: This has now devolved into the worst police shooting cover-up attempt in US history.

**同事件矛盾（val，sim=0.44）：**
       来源: val | ID: 499579650926858240 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Image of #Ferguson protester throwing tear gas back at police, wearing the American flag, is amazing. http://t.co/JXi1sibnGG @AntonioFrench
       矛盾点: 语义高度相似(sim=0.44)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.43）：**
       来源: train | ID: 498508707244683264 | Event: 1 | 标签: 非谣言(0)
       文本: So #Ferguson police want me to believe #MikeBrown tried to get into a police car and wrestle the officer's gun away. I'm gonna need video.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.40）：**
       来源: val | ID: 524958516822671360 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: If your first response to the #ottawashooting is to make a political point, your humanity is sadly and sorely lacking.
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 9. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2333

**错误样本：**
       来源: val | ID: 500284871541940225 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: I'm NOT believing this story because I know how the police lie and will keep lying and will organize together AND LIE. #MIKEBROWN #Ferguson

**同事件矛盾（val，sim=0.41）：**
       来源: val | ID: 499703033174179840 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Jammers used again. Both livestreams went down again, looks like police is trying to hide something. #Ferguson
       矛盾点: 语义高度相似(sim=0.41)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.44）：**
       来源: train | ID: 498268463639851008 | Event: 1 | 标签: 非谣言(0)
       文本: calling the neighbors a mob = dehumanizing a community to justify all future wrongdoing. #mikebrown #ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.39）：**
       来源: val | ID: 524974900017373184 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Just hearing the news, thoughts today are back home with the citizens and dedicated public servants in Ottawa and across the country.
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 10. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2812

**错误样本：**
       来源: val | ID: 499366666300846081 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Line of police cars with high beams on greets anyone trying to enter #Ferguson. It's shut down. No media allowed. http://t.co/bk6jFFM7jj

**同事件矛盾（val，sim=0.43）：**
       来源: val | ID: 499602333404504064 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Police militarization on display in #Ferguson http://t.co/m9jyPq3ALq
       矛盾点: 语义高度相似(sim=0.43)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.43）：**
       来源: train | ID: 499697729225105408 | Event: 1 | 标签: 非谣言(0)
       文本: More police cars heading into #Ferguson https://t.co/cguoQrqjCn
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.37）：**
       来源: val | ID: 524979881525137409 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Image from @kellyhobson shows police running to search buildings in downtown Ottawa. http://t.co/lLtW5skkJe
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 11. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3179

**错误样本：**
       来源: val | ID: 500328758201815041 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Disgusting: MO chapter of Klan raising money as “reward” for the officer killing #MikeBrown. #Ferguson #UniteBlue http://t.co/xRCCazRSFs

**同事件矛盾（val，sim=0.47）：**
       来源: val | ID: 499672226887897089 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: RT @freegcf: RT @organizemo: @OpFerguson PLS RT! Jail support info for ppl arrested at #mikebrown rallies. #ferguson http://t.co/GRJvO1dAlp
       矛盾点: 语义高度相似(sim=0.47)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.47）：**
       来源: train | ID: 500332097064550400 | Event: 1 | 标签: 非谣言(0)
       文本: Dear media: If Michael Brown's race is mentioned in a news report, so should officer Darren Wilson's race. #Ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.37）：**
       来源: val | ID: 544286688436969472 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: thinking of the people in Martin Place in Sydney right now, and for the police, etc having to deal with the situation. so terrifying
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 12. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2729

**错误样本：**
       来源: val | ID: 500289307257868288 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: The selective release of information by #Ferguson PD tells us nothing about the shooting. Instead appears to be a basic smear job.

**同事件矛盾（val，sim=0.41）：**
       来源: val | ID: 499699803576881152 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: The live stream from #Ferguson is back up and running. Watch here while you can: http://t.co/7QTY8soT46
       矛盾点: 语义高度相似(sim=0.41)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.44）：**
       来源: train | ID: 500335927248429056 | Event: 1 | 标签: 非谣言(0)
       文本: The #TeaParty was unable to stand up to Goverment tyranny in #Ferguson due to being too busy tweeting about President Obama's golf game.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.36）：**
       来源: val | ID: 544373945206460416 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: The #SydneySiege only works to sabotage the message Islam.
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 13. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3504

**错误样本：**
       来源: val | ID: 500298752469770240 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Shoot unarmed kid. Conceal evidence. Impose martial law. Harass reporters. Smear the victim. Worst. Police. Ever. #Ferguson #MikeBrown

**同事件矛盾（val，sim=0.45）：**
       来源: val | ID: 500163501961142275 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Photo taken by @FroGoddess "thanks for the advice #Palestine" - #Ferguson #STL #MikeBrown http://t.co/UkfKu2Zzdl
       矛盾点: 语义高度相似(sim=0.45)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.41）：**
       来源: train | ID: 499457882144796672 | Event: 1 | 标签: 非谣言(0)
       文本: So let me get this right - cops shoot an unarmed kid then put the town under effective martial law? In the USA? In 2014? #Ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.34）：**
       来源: val | ID: 544286688436969472 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: thinking of the people in Martin Place in Sydney right now, and for the police, etc having to deal with the situation. so terrifying
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 14. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.4629

**错误样本：**
       来源: val | ID: 498274493337702401 | Event: 1 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: : Teenager #MikeBrown won't start college on Monday because he was shot ten times by a #Ferguson police officer. http://t.co/dCFmzlkFRD”

**同事件矛盾（val，sim=0.41）：**
       来源: val | ID: 500291116403789824 | Event: 1 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Let's not forget that even if Mike Brown did shoplift, that's not why police said he was stopped or why he was shot. #mikebrown #ferguson
       矛盾点: 语义高度相似(sim=0.41)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.90）：**
       来源: train | ID: 498305825341845504 | Event: 1 | 标签: 谣言(1)
       文本: Teenager #MikeBrown won't start college on Monday because he was shot ten times by a #Ferguson police officer. http://t.co/B4hWevO7l9
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 4，sim=0.37）：**
       来源: val | ID: 580885624883904512 | Event: 4 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: One pilot in #Germanwings crash was locked out of cockpit, @nytimes reports http://t.co/doZIZCHP4o
       矛盾点: Event 4 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 15. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.4509

**错误样本：**
       来源: val | ID: 499536812109742080 | Event: 1 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: The fact that while we've been focused on #Ferguson another black man was killed by cops in LA and it barely made the news says a lot.

**同事件矛盾（val，sim=0.34）：**
       来源: val | ID: 500277808883830784 | Event: 1 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: BREAKING: #Ferguson police chief just announced that officer Darren Wilson shot the unarmed teen, Michael Brown.
       矛盾点: 语义高度相似(sim=0.34)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.40）：**
       来源: train | ID: 499612545909415938 | Event: 1 | 标签: 谣言(1)
       文本: Nearly 7k blacks were murdered last yr--almost all by other blacks. A tiny % were unarmed-killed-by-cop. Where's Al, Jesse? #tcot #ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.39）：**
       来源: val | ID: 525026715123601408 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Cpl. Nathan Cirillo identified as soldier shot, killed in Ottawa today, aunt says - @globeandmail http://t.co/oVrp10U6uG
       矛盾点: Event 6 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 16. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5157

**错误样本：**
       来源: val | ID: 499703156889362432 | Event: 1 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: #BREAKING: State Senator Maria Chapelle Nadal has been taken into police custody; she had been tear-gassed at an earlier protest. #Ferguson

**同事件矛盾（val，sim=0.35）：**
       来源: val | ID: 500354853680340993 | Event: 1 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Boom RT @newsneighbor Why was #Ferguson PD still looking for the suspect 7 hours after Michael Brown had been killed? http://t.co/4TH5aFsge2
       矛盾点: 语义高度相似(sim=0.35)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.40）：**
       来源: train | ID: 500360248767840256 | Event: 1 | 标签: 谣言(1)
       文本: the media didn't even know the video existed, but he just said they requested it? DUDE. #Ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.46）：**
       来源: val | ID: 529724254183780355 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #Breaking @LiveNationON has tweeted out there is no Prince show at Massey Hall tonight.
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 17. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2513

**错误样本：**
       来源: val | ID: 500417151346696192 | Event: 1 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Americans are 8 times more likely to be killed by a police officer than by a terrorist. #Ferguson

**同事件矛盾（val，sim=0.44）：**
       来源: val | ID: 499700824432717824 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: On some Tiananmen shit. RT @sebwalker: Military-style police: 3 APCs, ~100 officers, high-powered rifles #Ferguson http://t.co/JK0ZBrnEIO
       矛盾点: 语义高度相似(sim=0.44)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.48）：**
       来源: train | ID: 500332097064550400 | Event: 1 | 标签: 非谣言(0)
       文本: Dear media: If Michael Brown's race is mentioned in a news report, so should officer Darren Wilson's race. #Ferguson
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.40）：**
       来源: val | ID: 524978422188376064 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Hearts and prayers go out to everyone affected by the shootings in Ottawa today.
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


## Event 4


### 18. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2984

**错误样本：**
       来源: val | ID: 580321350750990336 | Event: 4 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Hashtags #4U9525 #GermanWings #A320 all useful for latest info on plane crash in southern France.

**同事件矛盾（val，sim=0.43）：**
       来源: val | ID: 580330454869512192 | Event: 4 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Everything we know about the Germanwings plane crash in France http://t.co/o0ZSGb1lQq http://t.co/N4TTbxlOY4
       矛盾点: 语义高度相似(sim=0.43)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.53）：**
       来源: train | ID: 580329265251536896 | Event: 4 | 标签: 非谣言(0)
       文本: Germanwings plane crashes in southern France http://t.co/Y4vqLg5RL8
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.39）：**
       来源: val | ID: 499704241741520897 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: People who claim to be against big, intrusive government and for the Constitution are cheerleading for the cops in #Ferguson now. Telling.
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 19. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3433

**错误样本：**
       来源: val | ID: 580319968484421633 | Event: 4 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: A Germanwings A320 has crashed en route to Dusseldorf. Flight Radar 24 of the last known position. #4U9525 http://t.co/FrI93NrYFF

**同事件矛盾（val，sim=0.53）：**
       来源: val | ID: 580322653472493569 | Event: 4 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: IMAGE: Flightradar24 has this as the plane's last position. #4U9525 http://t.co/CIeAyJ4AOf - @BBCRosAtkins
       矛盾点: 语义高度相似(sim=0.53)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.49）：**
       来源: train | ID: 580325486477357056 | Event: 4 | 标签: 非谣言(0)
       文本: BREAKING: Germanwings Airbus A320 en route from Barcelona to Dusseldorf crashes in southern French Alps -- French PM. http://t.co/UhEDxeVTkX
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.35）：**
       来源: val | ID: 499381917490237440 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Something being talked about tonight is the makeup of the #Ferguson Police Dept. Here's a breakdown: #MichaelBrown http://t.co/gYd5qgJh5M
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 20. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3032

**错误样本：**
       来源: val | ID: 580326871302316033 | Event: 4 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: IMAGE: .@flightradar24 altitude &amp; speed chart of #4U9525. Aircraft entered a steep but constant descent. http://t.co/MoG0h2Dvaq

**同事件矛盾（val，sim=0.42）：**
       来源: val | ID: 580322653472493569 | Event: 4 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: IMAGE: Flightradar24 has this as the plane's last position. #4U9525 http://t.co/CIeAyJ4AOf - @BBCRosAtkins
       矛盾点: 语义高度相似(sim=0.42)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.51）：**
       来源: train | ID: 580327058158551041 | Event: 4 | 标签: 非谣言(0)
       文本: UPDATE @flightradar24 altitude &amp; speed chart of #4U9525 http://t.co/wGXZMtDVDI http://t.co/pFdVDioV0e
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.36）：**
       来源: val | ID: 499362348940144640 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Police still at one end of W. Florissant, protesters now at Greater St. Mark Church. #Ferguson p/v @JustinGlawe http://t.co/ujLgUmKLNS
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 21. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5888

**错误样本：**
       来源: val | ID: 580327576218046464 | Event: 4 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: BREAKING NEWS: Germanwings flight GWI18G crashes in French Alps: http://t.co/v8yssTEbHR http://t.co/GA8ZdGUq30

**同事件矛盾（val，sim=0.58）：**
       来源: val | ID: 580330302251393024 | Event: 4 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #BREAKING: #Germanwings Airbus A320 crew sent distress signal before French Alps crash - reports http://t.co/JLDCz6AhFR
       矛盾点: 语义高度相似(sim=0.58)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.63）：**
       来源: train | ID: 580320563891019776 | Event: 4 | 标签: 谣言(1)
       文本: BREAKING: Germanwings Airbus A320 crashes in French Alps | via @BBCBreaking
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.41）：**
       来源: val | ID: 500277526590423041 | Event: 1 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: BREAKING NEWS: NAME OF OFFICER WHO SHOT #MIKEBROWN - OFFICER DAREN WILSON - #Ferguson
       矛盾点: Event 1 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 22. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.6355

**错误样本：**
       来源: val | ID: 580332232121933824 | Event: 4 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: BREAKING: A Germanwings jet crashed in France as it traveled from Barcelona to Dusseldorf http://t.co/vqUUuspIFk http://t.co/mwguIFT1iu

**同事件矛盾（val，sim=0.54）：**
       来源: val | ID: 580333763512705025 | Event: 4 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #Germanwings latest: http://t.co/8tZopIBYLh - #Airbus A320 crashes in French Alps - Barcelona-to-Dusseldorf flight - 142 passengers &amp; 6 crew
       矛盾点: 语义高度相似(sim=0.54)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.64）：**
       来源: train | ID: 580321327845765120 | Event: 4 | 标签: 谣言(1)
       文本: BREAKING: A #Lufthansa #Germanwings Airbus jet carrying 148 people has crashed in southern #France, en route from #Barcelona to #Duesseldorf
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.40）：**
       来源: val | ID: 529724254183780355 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #Breaking @LiveNationON has tweeted out there is no Prince show at Massey Hall tonight.
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 23. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5436

**错误样本：**
       来源: val | ID: 580329219646988289 | Event: 4 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: Last position of the #GermanWings Airbus A320 passenger jet that crashed in the French Alps http://t.co/8UPMsinQkX http://t.co/K3etnEPmxk

**同事件矛盾（val，sim=0.58）：**
       来源: val | ID: 580330302251393024 | Event: 4 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #BREAKING: #Germanwings Airbus A320 crew sent distress signal before French Alps crash - reports http://t.co/JLDCz6AhFR
       矛盾点: 语义高度相似(sim=0.58)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.62）：**
       来源: train | ID: 580317998147325952 | Event: 4 | 标签: 谣言(1)
       文本: 142 PEOPLE ON BOARD GERMANWINGS AIRBUS A320 THAT CRASHED IN SOUTHERN FRANCE
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.38）：**
       来源: val | ID: 544351969658564608 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: UPDATE: Reports the gunman has released three hostages, with the six hour #siege unravelling. Details to come. #9News
       矛盾点: Event 5 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 24. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.8349

**错误样本：**
       来源: val | ID: 580324804403818496 | Event: 4 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: An Airbus A320 plane operated by Germanwings crashed in France near Digne les Bains, French Prime Minister says. http://t.co/iWeLBpmiHS

**同事件矛盾（val，sim=0.64）：**
       来源: val | ID: 580322346508124160 | Event: 4 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Germanwings #A320 plane crashes in southern France, French prime minister says. More soon. http://t.co/k6pv4OsCQI
       矛盾点: 语义高度相似(sim=0.64)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.55）：**
       来源: train | ID: 580320964875014145 | Event: 4 | 标签: 谣言(1)
       文本: Airbus plane operated by Lufthansa's Germanwings airline crashes in southern France, officials say - @Reuters http://t.co/by471NAzFg
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.42）：**
       来源: val | ID: 524956372199555072 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Map of areas where Ottawa shootings were reported: National War Memorial, near the Rideau Centre and Parliament Hill. http://t.co/NcfNCR5VCV
       矛盾点: Event 6 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


## Event 5


### 25. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4361

**错误样本：**
       来源: val | ID: 544511130249744384 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: #sydneysiege: A series of loud blasts and bursts of ammunition have been heard at the cafe. http://t.co/IxPuyIrNy2 http://t.co/olteaN8zjH

**同事件矛盾（val，sim=0.42）：**
       来源: val | ID: 544477404342018048 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: #IllRideWithYou  Sydney Stands Up To Racism &amp; Bigotry With One Beautiful Hashtag  http://t.co/Ajaa1AQmG5 http://t.co/BQN4rBxhYK
       矛盾点: 语义高度相似(sim=0.42)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.43）：**
       来源: train | ID: 544314810884562946 | Event: 5 | 标签: 非谣言(0)
       文本: #sydneysiege We sit in the reality of grief, shock and unknowing. For this moment that is enough. http://t.co/bnUK0ZFvJt
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 0，sim=0.39）：**
       来源: val | ID: 536830979714056192 | Event: 0 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Berlin, Munich and Kunstmuseum Bern have signed an agreement on the management of Gurlitt's estate.
       矛盾点: Event 0 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 26. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2792

**错误样本：**
       来源: val | ID: 544289880805605376 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: The PM's office releases a statement about  #sydneysiege. http://t.co/7NdqPYhwcY http://t.co/jeYdlwywO7

**同事件矛盾（val，sim=0.65）：**
       来源: val | ID: 544410900854091776 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Australian Muslim community releases statement in response to #sydneysiege. http://t.co/KE9UFxdXuD
       矛盾点: 语义高度相似(sim=0.65)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.58）：**
       来源: train | ID: 544410895602839552 | Event: 5 | 标签: 非谣言(0)
       文本: Australian Muslim community releases statement in response to #sydneysiege. http://t.co/r6UMUVGxHV
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.39）：**
       来源: val | ID: 499665704300191745 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: More startling statistics about the segregated population of #Ferguson, Mo. http://t.co/uYrldQHoj7 http://t.co/vgxuLMYDhz
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 27. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4664

**错误样本：**
       来源: val | ID: 544341406094213121 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Deserted grounds of the evacuated #Sydney Opera House - More on our LIVE page: http://t.co/VaKt3ZpRZR #sydneysiege http://t.co/pKWvDgpOle

**同事件矛盾（val，sim=0.50）：**
       来源: val | ID: 544464445787750401 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: RT @mina_ysf: Religious leaders meet at Lakemba mosque in Sydney to pray for hostages  #sydneysiege http://t.co/D0nQRWwz5D
       矛盾点: 语义高度相似(sim=0.50)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.45）：**
       来源: train | ID: 544520795511611392 | Event: 5 | 标签: 非谣言(0)
       文本: A hostage situation at a Sydney cafe has come to an end, after police stormed the scene. Live updates: http://t.co/Z6JPQTstYO #Sydneysiege
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.38）：**
       来源: val | ID: 499665704300191745 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: More startling statistics about the segregated population of #Ferguson, Mo. http://t.co/uYrldQHoj7 http://t.co/vgxuLMYDhz
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 28. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.5034

**错误样本：**
       来源: val | ID: 544511676088066048 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: What we know about Sheikh Haron, the suspected hostage taker in #SydneySiege http://t.co/KUEe3Bl2tp http://t.co/ZRzH6vunkh

**同事件矛盾（val，sim=0.51）：**
       来源: val | ID: 544379787246981122 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Their faces say it all. #Sydneysiege continues more&gt;http://t.co/6EAaEKw4n9 http://t.co/NkzVcf9mxv
       矛盾点: 语义高度相似(sim=0.51)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.64）：**
       来源: train | ID: 544515517546254338 | Event: 5 | 标签: 非谣言(0)
       文本: What we know about suspected hostage taker in Sydney http://t.co/B17EiJYhWu http://t.co/lKolS1SkGN
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 4，sim=0.44）：**
       来源: val | ID: 580330454869512192 | Event: 4 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Everything we know about the Germanwings plane crash in France http://t.co/o0ZSGb1lQq http://t.co/N4TTbxlOY4
       矛盾点: Event 4 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 29. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3844

**错误样本：**
       来源: val | ID: 544296671950020609 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: From @guardian on Ray Hadley's speculative reports: #sydneysiege http://t.co/qRXKjmJZyq

**同事件矛盾（val，sim=0.54）：**
       来源: val | ID: 544376469279875072 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: "You never see non-Muslims do things like this." #SydneySiege http://t.co/nPxTMBmK11
       矛盾点: 语义高度相似(sim=0.54)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.48）：**
       来源: train | ID: 544429942323167233 | Event: 5 | 标签: 非谣言(0)
       文本: friendly reminder. #sydneysiege http://t.co/auO7vbaPgu
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.39）：**
       来源: val | ID: 499598945417703424 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: More from #Ferguson this morning http://t.co/82Ylq2SqzK
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 30. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.1717

**错误样本：**
       来源: val | ID: 544340091615715329 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: hostages in Sydney right now... my thoughts and prayers are with you guys.   so much hatred in the world. this isn't the way.. #sydneysiege

**同事件矛盾（val，sim=0.49）：**
       来源: val | ID: 544508313220567041 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: All my thoughts &amp; prayers are with the people of Sydney.
       矛盾点: 语义高度相似(sim=0.49)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.49）：**
       来源: train | ID: 544476597512699904 | Event: 5 | 标签: 非谣言(0)
       文本: My thoughts and prayers to the hostages, their families and friends. #sydneysiege
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.52）：**
       来源: val | ID: 524967231902318592 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Our thoughts and prayers are with those affected by the shootings in Ottawa. Stay safe! #PrayForOttawa
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 31. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2503

**错误样本：**
       来源: val | ID: 544287991959539713 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: ABC understands the national security committee of cabinet has just wrapped up a meeting about the #sydneysiege http://t.co/7NdqPYhwcY

**同事件矛盾（val，sim=0.49）：**
       来源: val | ID: 544348392944463872 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: BREAKING: Australian National Imams Council condemns Sydney siege http://t.co/qFdU4gHjAE
       矛盾点: 语义高度相似(sim=0.49)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.45）：**
       来源: train | ID: 544337816298070017 | Event: 5 | 标签: 非谣言(0)
       文本: You gotta admire the ability of Daily Tele editors to resist fads like fact-checking #sydneysiege
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.36）：**
       来源: val | ID: 524979179235069952 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Remembrance Day ceremony in Ottawa is emotional every year. Can't imagine what it will be like this year. The entire country may be there.
       矛盾点: Event 6 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 32. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4984

**错误样本：**
       来源: val | ID: 544278985249550337 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Geoblock lifted on #ABCNews24. Streaming coverage of the Martin Place siege in Sydney here  http://t.co/HvQuvP4SIb.

**同事件矛盾（val，sim=0.45）：**
       来源: val | ID: 544423869981802496 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: We condemn the actions of the criminals at #martinsplace #sydneysiege   Islam is free from terrorism. Visit: http://t.co/fsBE3gEuYH
       矛盾点: 语义高度相似(sim=0.45)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.44）：**
       来源: train | ID: 544294274674593792 | Event: 5 | 标签: 非谣言(0)
       文本: Police are requesting that no photos of the Lindt cafe siege are shared on social media #MartinPlaceSiege #SydneySiege #MartinPlace
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 4，sim=0.36）：**
       来源: val | ID: 580346858846822400 | Event: 4 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: This picture from a helicopter sent to the #Germanwings Alps plane crash site shows how remote the area is http://t.co/Fo6h66ZehE
       矛盾点: Event 4 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 33. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4454

**错误样本：**
       来源: val | ID: 544296158206894081 | Event: 5 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Breaking: Sydney On Lockdown as Dramatic Siege Unfolds http://t.co/Xpjpgbf2Pb #sydneysiege http://t.co/31KmD0zuIx

**同事件矛盾（val，sim=0.51）：**
       来源: val | ID: 544461947882586112 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: 'Sick' people are actually taking selfies at the site of the #sydneysiege http://t.co/DebSinfhyH http://t.co/rHDxHczlWc
       矛盾点: 语义高度相似(sim=0.51)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.48）：**
       来源: train | ID: 544518044643770368 | Event: 5 | 标签: 非谣言(0)
       文本: #BREAKING: Police have confirmed Sydney hostage taking is over. #Sydneysiege
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 4，sim=0.36）：**
       来源: val | ID: 580351083383517185 | Event: 4 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: BREAKING Emergency units staging in Seyne-les-Alpes, near #4U9525 crash site /@Aviaponcho http://t.co/wFg8KTSve2 http://t.co/NaHq3MIOlz
       矛盾点: Event 4 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 34. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.6093

**错误样本：**
       来源: val | ID: 544497307933474816 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: #SydneySiege UPDATE: Gunman identified as local resident Man Monis, has police records http://t.co/6bXGBh0qHD http://t.co/3vw2bF1Ojo

**同事件矛盾（val，sim=0.52）：**
       来源: val | ID: 544352874969698305 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #SYDNEYSIEGE: 3 people escape gunman-held Lindt Café http://t.co/1ZlzKDjvSf http://t.co/DJCj55u6qk
       矛盾点: 语义高度相似(sim=0.52)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.70）：**
       来源: train | ID: 544490782183657474 | Event: 5 | 标签: 谣言(1)
       文本: BREAKING: #SydneySiege gunman identified as local resident Man Monis - reports http://t.co/m51P8dUPhB
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.42）：**
       来源: val | ID: 525040408653754368 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: BREAKING NEWS: Suspected Ottawa gunman identified as Michael Joseph Hall, an #ISIS sympathizer. #OttawaShooting
       矛盾点: Event 6 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 35. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5139

**错误样本：**
       来源: val | ID: 544520344976232449 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: #BREAKING: Australian police confirm Sydney siege is over

**同事件矛盾（val，sim=0.54）：**
       来源: val | ID: 544511112654618624 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #BREAKING: Heavily armed police look to be storming the Lindt Café. #SydneySiege #9News
       矛盾点: 语义高度相似(sim=0.54)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.70）：**
       来源: train | ID: 544517264725516288 | Event: 5 | 标签: 谣言(1)
       文本: #BREAKING: Police have confirmed that the #SydneySiege is over. #9News
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.37）：**
       来源: val | ID: 500277808883830784 | Event: 1 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: BREAKING: #Ferguson police chief just announced that officer Darren Wilson shot the unarmed teen, Michael Brown.
       矛盾点: Event 1 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 36. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5594

**错误样本：**
       来源: val | ID: 544443377643954176 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: Watch: Escaped hostages are helping police create 'peaceful outcome' for #Sydneysiege http://t.co/TzSlNsgTip http://t.co/0O3kEAf7Pt

**同事件矛盾（val，sim=0.52）：**
       来源: val | ID: 544451181754744832 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #sydneysiege: Up to 20 hostages are being held in darkness in a cafe in Sydney. http://t.co/5jtd36wFOU http://t.co/Gmt7PAuHzb
       矛盾点: 语义高度相似(sim=0.52)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.48）：**
       来源: train | ID: 544350480780914688 | Event: 5 | 标签: 谣言(1)
       文本: BREAKING: Hostages are running out of the cafe #sydneysiege
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.36）：**
       来源: val | ID: 529644676333453312 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: WHAT?  RT @CityNews #BREAKING: Prince reportedly to perform surprise show at Massey Hall tonight http://t.co/jT8Tx5P1Kw #Toronto
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 37. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5157

**错误样本：**
       来源: val | ID: 544357264333615104 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: This is well written and comforting as well. #sydneysiege #SydneyHostageCrisis http://t.co/mdJvf6NEdf

**同事件矛盾（val，sim=0.44）：**
       来源: val | ID: 544355924224532481 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: JUST IN: Police: 3 people were able to run from Sydney cafe during ongoing hostage situation - @9NewsAUS http://t.co/wFfwbG9Gg6
       矛盾点: 语义高度相似(sim=0.44)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.53）：**
       来源: train | ID: 544514645571420160 | Event: 5 | 标签: 谣言(1)
       文本: Sydney gunman was shot by police and is confirmed dead #sydneysiege #SydneyHostageCrisis
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.37）：**
       来源: val | ID: 529671440829005825 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Is Prince playing a surprise show at Massey Hall tonight? http://t.co/mv0Ca9ro6a
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 38. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.7854

**错误样本：**
       来源: val | ID: 544495167836016640 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: At least 5 dead as gunman goes on rampage in PA, suspect reportedly barricaded in a home http://t.co/aCLslANGxu http://t.co/H4Mhm1cyOm

**同事件矛盾（val，sim=0.45）：**
       来源: val | ID: 544288799711592448 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Hostages taken in Sydney cafe as Islamic flag is reportedly flown http://t.co/OD9gOTGh2w
       矛盾点: 语义高度相似(sim=0.45)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.46）：**
       来源: train | ID: 544430771688439808 | Event: 5 | 标签: 谣言(1)
       文本: "At least 1 gunman" in #SydneySiege (image of suspect not verified) No injuries known - police http://t.co/XLklHFHCT3 http://t.co/Rxh3RH2RMS
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.40）：**
       来源: val | ID: 529399936434327552 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: can someone get us in 2 the secret prince show in toronto tomorrow
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 39. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.7649

**错误样本：**
       来源: val | ID: 544299273664593920 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: Australian prime minister Tony Abbott to hold news conference live on Sky News at 1.30am GMT about ongoing Sydney hostage situation

**同事件矛盾（val，sim=0.45）：**
       来源: val | ID: 544355924224532481 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: JUST IN: Police: 3 people were able to run from Sydney cafe during ongoing hostage situation - @9NewsAUS http://t.co/wFfwbG9Gg6
       矛盾点: 语义高度相似(sim=0.45)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.52）：**
       来源: train | ID: 544289311504355328 | Event: 5 | 标签: 谣言(1)
       文本: Statement from Prime Minister Tony Abbott on Sydney hostage situation. http://t.co/MHkNRZFQWB
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 2，sim=0.35）：**
       来源: val | ID: 521358118597689344 | Event: 2 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Milan have stated that the reports about Essien having Ebola are completely false. http://t.co/Sb9v9ulfTX @MichaelEssien
       矛盾点: Event 2 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 40. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.6820

**错误样本：**
       来源: val | ID: 544503425082613761 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: The man believed to be holding hostages in Sydney is Man Haron Monis, known as Sheikh Haron, source says http://t.co/6T7xVdcwdD

**同事件矛盾（val，sim=0.48）：**
       来源: val | ID: 544272701108797440 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: JUST IN: Two gunmen, dozen hostages inside cafe in Sydney, Australia. ISIS flags remain on display. - @KristyMayr7 http://t.co/p4GyCRobSa
       矛盾点: 语义高度相似(sim=0.48)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.44）：**
       来源: train | ID: 544283387087691776 | Event: 5 | 标签: 谣言(1)
       文本: For those confused: gunmen have taken hostages in a Sydney cafe holding a Shahada flag (NOT THE SAME AS ISIS) http://t.co/i9VVwyqN1G
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.36）：**
       来源: val | ID: 524944544681705472 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Ottawa police: Actively looking for one or more suspects in Canadian parliament shooting. http://t.co/UQ4xo5jvhF
       矛盾点: Event 6 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 41. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5237

**错误样本：**
       来源: val | ID: 544434192478519297 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: A female hostage stands by the front entrance of the cafe as she turns the lights off in Sydney. #sydneysiege http://t.co/qNfCMv9yZt

**同事件矛盾（val，sim=0.48）：**
       来源: val | ID: 544377700677615616 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Total number of people who have left the cafe in Sydney up to 5. The latest: http://t.co/Nl3BNlFidA #SydneySiege http://t.co/TgZkYFNlR9
       矛盾点: 语义高度相似(sim=0.48)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.50）：**
       来源: train | ID: 544316384273248256 | Event: 5 | 标签: 谣言(1)
       文本: Our thoughts and prayers are with the hostages and the families in Sydney. #sydneysiege http://t.co/TYH5KaeLSA
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.37）：**
       来源: val | ID: 529726211241803776 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Bad news for the Prince fans in the queue. No show in Toronto unfortunately. (according to Livenation) https://t.co/BbaUOo9k1x
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 42. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.5170

**错误样本：**
       来源: val | ID: 544336572141694976 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: #SYDNEYSIEGE: Crowd gathers at police cordon in anticipation of news on hostage situation  http://t.co/2zFjvlPC1n http://t.co/YW5zGPMEWS

**同事件矛盾（val，sim=0.51）：**
       来源: val | ID: 544387967037763584 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #sydneysiege: There are reports the hostage-taker claims to have up to four bombs. http://t.co/1gMsZkOTjC http://t.co/hrMncBhLy5
       矛盾点: 语义高度相似(sim=0.51)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.50）：**
       来源: train | ID: 544290258951892992 | Event: 5 | 标签: 谣言(1)
       文本: Central Sydney shut down by police amid ongoing hostage situation: http://t.co/TvAlMmqFxP
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 6，sim=0.39）：**
       来源: val | ID: 524947424482435073 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #BREAKING: Shooter is dead, according to sources on Parliament Hill
       矛盾点: Event 6 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 43. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.8468

**错误样本：**
       来源: val | ID: 544515072203444224 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: Breaking News: Police Storm Sydney Cafe Where Hostages Are Held http://t.co/P3f2OV2Gmz

**同事件矛盾（val，sim=0.62）：**
       来源: val | ID: 544369667096477696 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Police Surround Sydney Cafe, Where Armed Person Holds Hostages http://t.co/CPrsOcTuis
       矛盾点: 语义高度相似(sim=0.62)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.70）：**
       来源: train | ID: 544357487911395329 | Event: 5 | 标签: 谣言(1)
       文本: BREAKING: Police have confirmed 3 people escape Sydney cafe where hostages are being held
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.42）：**
       来源: val | ID: 529724254183780355 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #Breaking @LiveNationON has tweeted out there is no Prince show at Massey Hall tonight.
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 44. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.8926

**错误样本：**
       来源: val | ID: 544301589931241472 | Event: 5 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: Australian PM Abbott expected to speak soon on "reported hostage-taking incident" in Sydney, @9NewsAUS reports - @WorldNews

**同事件矛盾（val，sim=0.44）：**
       来源: val | ID: 544272701108797440 | Event: 5 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: JUST IN: Two gunmen, dozen hostages inside cafe in Sydney, Australia. ISIS flags remain on display. - @KristyMayr7 http://t.co/p4GyCRobSa
       矛盾点: 语义高度相似(sim=0.44)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.65）：**
       来源: train | ID: 544293783702364162 | Event: 5 | 标签: 谣言(1)
       文本: UPDATE: Australian PM Abbott: Police dealing with "reported hostage-taking incident" in Sydney's business district - http://t.co/iqgdmiCDNh
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.35）：**
       来源: val | ID: 529729911926583296 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: TORONTO: In case you missed it @LiveNationON are saying no Prince shows @masseyhall either today or tomorrow.
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


## Event 6


### 45. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2683

**错误样本：**
       来源: val | ID: 524975847846203393 | Event: 6 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: NHL says date of rescheduled game TBD. NHL  ``wishes to express its sympathy and prayers to all affected by the tragic events in Ottawa''

**同事件矛盾（val，sim=0.48）：**
       来源: val | ID: 524978422188376064 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Hearts and prayers go out to everyone affected by the shootings in Ottawa today.
       矛盾点: 语义高度相似(sim=0.48)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.49）：**
       来源: train | ID: 524956648151191553 | Event: 6 | 标签: 非谣言(0)
       文本: Thoughts and prayer goes out to all those involved in the tragic events this morning in Ottawa.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.33）：**
       来源: val | ID: 499704241741520897 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: People who claim to be against big, intrusive government and for the Constitution are cheerleading for the cops in #Ferguson now. Telling.
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 46. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4040

**错误样本：**
       来源: val | ID: 524995771587108864 | Event: 6 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: This afternoon we've lowered our flags to half mast in honour of the Canadian Reservist who lost his life in Ottawa. http://t.co/3oTF5sd2Lf

**同事件矛盾（val，sim=0.39）：**
       来源: val | ID: 524979881525137409 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Image from @kellyhobson shows police running to search buildings in downtown Ottawa. http://t.co/lLtW5skkJe
       矛盾点: 语义高度相似(sim=0.39)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.43）：**
       来源: train | ID: 524957105296404480 | Event: 6 | 标签: 非谣言(0)
       文本: What we know so far about the Canadian Parliament shooting in Ottawa http://t.co/3NUfy6joHM http://t.co/9iWwhBPPZv
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.40）：**
       来源: val | ID: 500210207986028544 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: #wakeup #MarshallLaw #Ferguson - America - how's that land of the free working out? http://t.co/uI9nWUXr8a
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 47. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.3426

**错误样本：**
       来源: val | ID: 524956294395224064 | Event: 6 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Here are the 3 locations of shootings in #Ottawa around Parliament Hill (GoofleEarth) From: @CNNJason http://t.co/DSyNgBC02U

**同事件矛盾（val，sim=0.44）：**
       来源: val | ID: 524968185016360960 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: #Leafs Joffrey Lupul praises officers in Ottawa, as team remains in lock down http://t.co/OPooNxTsiv http://t.co/yBjIu2JaaP
       矛盾点: 语义高度相似(sim=0.44)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.53）：**
       来源: train | ID: 524942851944493056 | Event: 6 | 标签: 非谣言(0)
       文本: Please DO NOT tweet photos or locations of police in #ottawa at the Parliament Buildings! @TorontoPolice @OttawaPolice
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.37）：**
       来源: val | ID: 544280391226761218 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: What's happening in Sydney will happen in the uk it's inevitable, and our political leaders will have blood on their hands
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 48. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4178

**错误样本：**
       来源: val | ID: 525055879545380864 | Event: 6 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: Our thoughts are with the family and friends of Cpl. Nathan Cirillo and all those affected by the events in Ottawa today. #OttawaStrong

**同事件矛盾（val，sim=0.56）：**
       来源: val | ID: 524967231902318592 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Our thoughts and prayers are with those affected by the shootings in Ottawa. Stay safe! #PrayForOttawa
       矛盾点: 语义高度相似(sim=0.56)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.62）：**
       来源: train | ID: 524978999534317568 | Event: 6 | 标签: 非谣言(0)
       文本: Our thoughts are with all those affected by today’s events in Ottawa.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.40）：**
       来源: val | ID: 544337283801829376 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: My thoughts are with the hostages, their families and everyone in Sydney right now.
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 49. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.2423

**错误样本：**
       来源: val | ID: 525045145079533568 | Event: 6 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: .@pmharper and I have been speaking to some of our allies around the world. The PM will address the nation this evening. #OttawaShooting

**同事件矛盾（val，sim=0.43）：**
       来源: val | ID: 524964166936068097 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Public servants being asked to stay inside their buildings as the active shooter investigation continues in Ottawa. #cbcOTT# OTTnews
       矛盾点: 语义高度相似(sim=0.43)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.43）：**
       来源: train | ID: 524950203476869120 | Event: 6 | 标签: 非谣言(0)
       文本: Please exercise restraint in looking for someone or some group to immediately blame for this. #ottawashooting
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 1，sim=0.38）：**
       来源: val | ID: 499698357397237762 | Event: 1 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: Those cops on line in #Ferguson don't have riot shields and batons. They have rifles. The only thing they can do with those is shoot people.
       矛盾点: Event 1 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 50. [FN (漏报)] 模型判 非谣言(0)，真实 谣言(1)，prob=0.4138

**错误样本：**
       来源: val | ID: 524981689781870593 | Event: 6 | 标签: 谣言(1) | 模型判: 非谣言(0) ✗
       文本: One shooting victim succumbed to injuries. He was a member of the Canadian Forces. Our thoughts and prayers are with him and his loved ones.

**同事件矛盾（val，sim=0.41）：**
       来源: val | ID: 525068253341970432 | Event: 6 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: What an awful day in Ottawa. Thoughts and prayers are with our @Senators family, the entire city of Ottawa and all of Canada.
       矛盾点: 语义高度相似(sim=0.41)，但标签为 非谣言(0)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.45）：**
       来源: train | ID: 525049481679892481 | Event: 6 | 标签: 非谣言(0)
       文本: Along with all our fellow Canadians, our thoughts are with the family of the @CanadianForces member killed today. #OttawaShooting
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 5，sim=0.41）：**
       来源: val | ID: 544508313220567041 | Event: 5 | 标签: 非谣言(0) | 模型判: 非谣言(0) ✓
       文本: All my thoughts &amp; prayers are with the people of Sydney.
       矛盾点: Event 5 中同样文本风格被标为 非谣言(0)，但本样本被标为 谣言(1)


### 51. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.4965

**错误样本：**
       来源: val | ID: 525063393309630464 | Event: 6 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: VIDEO: Key moments in today's Parliament Hill shootings. http://t.co/kR1mIPoJJg http://t.co/6gYfgPTH7q

**同事件矛盾（val，sim=0.62）：**
       来源: val | ID: 524952883343925249 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Watch video showing gunfire inside Canada's parliament in Ottawa http://t.co/CJpXNAk8nS http://t.co/hxwr2NEr2K
       矛盾点: 语义高度相似(sim=0.62)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.52）：**
       来源: train | ID: 524972277406773248 | Event: 6 | 标签: 谣言(1)
       文本: Video: Reporter captures shoot-out in Ottawa's Parliament Hill building. Watch: http://t.co/BIemkWAVtc http://t.co/d0BakjCrAB
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 4，sim=0.37）：**
       来源: val | ID: 580365368805486592 | Event: 4 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: 150 people were on board plane that crashed in France today, #Germanwings CEO says. http://t.co/HAhU3MmiMf http://t.co/QFCbhPWSJI
       矛盾点: Event 4 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 52. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.8761

**错误样本：**
       来源: val | ID: 524924987774631936 | Event: 6 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: #BREAKING: Shooting reported at the War Memorial in Ottawa

**同事件矛盾（val，sim=0.49）：**
       来源: val | ID: 524981513637888000 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: UPDATE: This morning’s shooting incidents occurred at the National War Memorial and on Parliament Hill.  Not Rideau Centre. #ottnews
       矛盾点: 语义高度相似(sim=0.49)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.62）：**
       来源: train | ID: 524923341359300608 | Event: 6 | 标签: 谣言(1)
       文本: Uniformed Canadian soldier shot at War Memorial in #Ottawa.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.47）：**
       来源: val | ID: 529724254183780355 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #Breaking @LiveNationON has tweeted out there is no Prince show at Massey Hall tonight.
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 53. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.4809

**错误样本：**
       来源: val | ID: 524958741259886592 | Event: 6 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: BREAKING: Four Blackwater guards convicted of voluntary manslaughter in 2007 Baghdad shooting http://t.co/hR7xe18RJ2

**同事件矛盾（val，sim=0.48）：**
       来源: val | ID: 524966904885428226 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: BREAKING UPDATE: Canadian soldier injured at Parliament Hill shooting dies http://t.co/Zp9AKplH9p  #Ottawa
       矛盾点: 语义高度相似(sim=0.48)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.50）：**
       来源: train | ID: 524983366261936130 | Event: 6 | 标签: 谣言(1)
       文本: BREAKING: Police say soldier, 1 suspected gunman dead in Ottawa shootings.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.41）：**
       来源: val | ID: 529724254183780355 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: #Breaking @LiveNationON has tweeted out there is no Prince show at Massey Hall tonight.
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


### 54. [FP (误报)] 模型判 谣言(1)，真实 非谣言(0)，prob=0.4939

**错误样本：**
       来源: val | ID: 524946461621235712 | Event: 6 | 标签: 非谣言(0) | 模型判: 谣言(1) ✗
       文本: RAW VIDEO War Memorial shooting. http://t.co/c9wCpS2Af9 #cbcnews

**同事件矛盾（val，sim=0.47）：**
       来源: val | ID: 524966904885428226 | Event: 6 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: BREAKING UPDATE: Canadian soldier injured at Parliament Hill shooting dies http://t.co/Zp9AKplH9p  #Ottawa
       矛盾点: 语义高度相似(sim=0.47)，但标签为 谣言(1)（与错误样本相反），模型预测正确

**同事件矛盾（train，sim=0.49）：**
       来源: train | ID: 524951625556066304 | Event: 6 | 标签: 谣言(1)
       文本: CTV reports that soldier shot at war memorial still alive.
       矛盾点: 训练集中存在语义相似的相反标签样本，模型在训练时就收到了矛盾信号

**跨事件矛盾（Event 3，sim=0.37）：**
       来源: val | ID: 529695299200360448 | Event: 3 | 标签: 谣言(1) | 模型判: 谣言(1) ✓
       文本: Prince rumoured to play secret Toronto show today http://t.co/ODT5L7b8Pi
       矛盾点: Event 3 中同样文本风格被标为 谣言(1)，但本样本被标为 非谣言(0)


---
总计: 54 个错误，全部存在标签矛盾
