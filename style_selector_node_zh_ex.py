# -----------------------------------------------------------------
# 这是一个ComfyUI的自定义节点
# 功能：根据用户选择的风格，将输入的文本应用到预设的提示词模板中。
# -----------------------------------------------------------------

# 1. 定义你的风格列表
# 你可以在这里添加、删除或修改任何风格。
# "name": 将会显示在节点的下拉菜单中。
# "prompt": 正面提示词模板，"{prompt}" 将会被用户的输入替换。
# "negative_prompt": 负面提示词模板。
import random
import time

style_list = [
    {"name": "(None)", "prompt": "{prompt}", "negative_prompt": ""},
    # ========================
    # 🌟 必选神仙光影 (Lighting)
    # ========================
    {
        "name": "青春 - 迟到的转角 (转角遇到爱)",
        "prompt": "{prompt}, school street corner, running late with toast in mouth (optional), bumping into viewer (POV), books flying in air, dynamic motion blur, surprised expression, blushing heavily, panties slightly visible (accidental), cherry blossoms falling, high key vibrant pastel colors, honeyworks mv aesthetic",
        "negative_prompt": "static, boring, dark, horror, realistic violence",
    },
    {
        "name": "青春 - 借一只耳机 (心跳距离)",
        "prompt": "{prompt}, sitting on train or park bench, sharing one earphone with viewer (POV), wire connecting us, looking away shyly, face red, very close proximity, golden hour sunset lighting, lens flare, romantic atmosphere, shoujo manga vibe, heart skipping a beat",
        "negative_prompt": "distant, sad, angry, wireless earbuds",
    },
    {
        "name": "青春 - 鞋柜情书 (被发现了)",
        "prompt": "{prompt}, standing in front of school shoe lockers (getabako), holding a love letter with both hands, startled expression looking at camera, caught in the act, morning sunlight, dust motes, nervous sweating, pure love aesthetic, school uniform",
        "negative_prompt": "trash, dirty, night, scary",
    },
    {
        "name": "青春 - 借物赛跑 (题目是你)",
        "prompt": "{prompt}, school sports festival, scavenger hunt race, grabbing viewer's hand (POV) and running, looking back with a determined but shy smile, 'the item I need is you' concept, sweat, bright blue sky, motion lines, energetic youth",
        "negative_prompt": "indoor, rain, static, slow",
    },
    {
        "name": "青春 - 图书馆触碰 (手背重叠)",
        "prompt": "{prompt}, library bookshelf, reaching for the same book as viewer (POV), hands touching, extreme close-up on face, wide eyes, startled blush, quiet atmosphere, soft dust particles, romantic tension, freeze frame moment",
        "negative_prompt": "loud, party, fighting, far away",
    },
    {
        "name": "青春 - 放学后的雨 (共撑一把伞)",
        "prompt": "{prompt}, sharing one umbrella (aiaigasa), walking home in rain, wet school uniform, looking up at viewer, shoulder touching, shy happy smile, rain droplets, reflection on wet pavement, cinematic emotional lighting, honeyworks ballad style",
        "negative_prompt": "sunny, dry, alone, distant",
    },
    {
        "name": "青春 - 告白实行委员会 (练习)",
        "prompt": "{prompt}, standing on school rooftop, sunset backdrop, shouting confession towards the ocean (or viewer), hands cupped around mouth, tears of nervousness in corners of eyes, emotional climax, wind blowing hair, vibrant orange and purple sky",
        "negative_prompt": "indoor, night, calm, bored",
    },
    {
        "name": "青春 - 视线交汇 (上课偷看)",
        "prompt": "{prompt}, classroom setting, sitting at desk, resting chin on hand, looking at viewer (POV), suddenly realizing eye contact, flustered, trying to hide face with book, sunlight streaming through window, dreamy atmosphere",
        "negative_prompt": "sleeping, studying hard, teacher",
    },
    {
        "name": "王道 - 偶像MV (糖果甜美风)",
        "prompt": "{prompt}, J-pop idol photography, twin tails with ribbons, frilly idol costume, pastel color palette, blooming flower garden background, soft diffused lighting, high key, vibrant but soft colors, kawaii aesthetic, commercial music video look, dreamy bokeh, doll-like makeup, heavy blush",
        "negative_prompt": "dark, gloomy, low contrast, edgy, monochrome, realistic street, horror, gritty",
    },
    {
        "name": "王道 - 动感舞蹈 (速度感)",
        "prompt": "{prompt}, high energy dancing, dynamic pose, motion blur on hands and hair, hair flying in the air, skirt flowing, shutter speed priority, dynamic camera angle, dutch angle, stage lights trailing, energetic atmosphere",
        "negative_prompt": "static, standing still, frozen, sharp focus everywhere",
    },
    {
        "name": "王道 - 后台休息 (真实感)",
        "prompt": "{prompt}, sitting in dressing room backstage, messy background with costumes and makeup tools, drinking water with a straw, towel around neck, sweating, tired but happy smile, looking at mirror reflection, candid off-shot, warm light bulb lighting",
        "negative_prompt": "stage lights, performing, dancing, outdoor",
    },
    {
        "name": "王道 - 闪耀舞台 (C位光环)",
        "prompt": "{prompt}, live stage performance, standing center stage, sparkling confetti falling, stage spotlights, energetic dance pose, glistening sweat, vibrant stage costume, concert atmosphere, fans lightsticks in background blur",
        "negative_prompt": "dark, static, boring, empty audience",
    },
    {
        "name": "王道 - 夏日泳池 (清凉MV)",
        "prompt": "{prompt}, summer idol music video, poolside dancing, blue sky and white clouds, water splashing, high key lighting, bright cyan and white theme, swimsuit or summer dress, energetic smile, refreshing atmosphere, lens flare",
        "negative_prompt": "winter, dark, cloudy, indoor",
    },
    {
        "name": "王道 - 梦幻爱丽丝 (童话风)",
        "prompt": "{prompt}, fantasy fairytale theme, Alice in Wonderland style, giant flowers and mushrooms prop, pastel lolita dress, tea party setting, soft dreamy filter, magical atmosphere, whimsical, storybook aesthetic",
        "negative_prompt": "realistic, gritty, urban, sci-fi",
    },
    {
        "name": "王道 - 樱花毕业季 (伤感风)",
        "prompt": "{prompt}, under cherry blossom trees, falling sakura petals, school uniform with cardigan, emotional expression, singing ballad, soft pink filter, spring breeze, sentimental atmosphere, crying but beautiful, lens haze",
        "negative_prompt": "happy, energetic, summer, green leaves",
    },
    {
        "name": "王道 - 情人节特辑 (巧克力)",
        "prompt": "{prompt}, valentine's day special, holding handmade chocolate heart, kitchen studio set, wearing apron over cute outfit, red and pink ribbons, warm lighting, shy expression, sweet romantic mood, soft focus",
        "negative_prompt": "cold colors, blue, cool tone",
    },
    {
        "name": "王道 - 纯白天使 (圣洁风)",
        "prompt": "{prompt}, wearing white angel costume with wings, feathers floating in air, heavenly bright white background, strong bloom effect, ethereal lighting, angelic smile, pure and innocent look, high exposure",
        "negative_prompt": "black, dark, devil, red",
    },
    {
        "name": "王道 - 校园天台 (青春喊话)",
        "prompt": "{prompt}, school rooftop, blue sky background, shouting to the ocean, wind blowing hair, seishun drama style, school uniform, lens flare, wide angle shot, energetic and emotional, youth movie vibe",
        "negative_prompt": "night, indoor, rain",
    },
    {
        "name": "王道 - 睡衣派对 (私房感)",
        "prompt": "{prompt}, pajama party MV scene, wearing fluffy cute roomwear, sitting on bed with stuffed animals, pastel balloons, soft bedroom lighting, intimate camera angle, playful and relaxed, girly room",
        "negative_prompt": "outdoor, formal wear, suit",
    },
    {
        "name": "王道 - 圣诞限定 (冬日恋歌)",
        "prompt": "{prompt}, christmas idol special, santa claus inspired cute costume, snowy background, christmas lights bokeh, holding candle or gift, winter breath vapor, romantic holiday atmosphere, sparkling night",
        "negative_prompt": "summer, beach, sun",
    },
    {
        "name": "王道 - 酷飒甜心 (Girl Crush)",
        "prompt": "{prompt}, cool and cute style, black and pink costume, neon studio lighting, confident expression, k-pop influence, geometric background, sharp focus, fashion editorial look, edgy but kawaii",
        "negative_prompt": "soft, blurry, traditional, vintage",
    },
    {
        "name": "王道 - 泡泡浴缸 (缤纷色彩)",
        "prompt": "{prompt}, inside a bathtub filled with colorful plastic balls and balloons, playful expression, vibrant pop colors, overhead shot, music video aesthetic, candy color palette, bright studio light",
        "negative_prompt": "water, real bath, nudity, dark",
    },
    {
        "name": "王道 - 昭和复古 (80年代偶像)",
        "prompt": "{prompt}, vintage photograph, 35mm film photo, flash photography, grainy texture, 1980s japanese idol, Matsuda Seiko hairstyle, soft focus lens, studio portrait, starry filter effect, nostalgic hazy look, pastel dress, vintage tv show quality",
        "negative_prompt": "4k, sharp, modern, digital",
    },
    {
        "name": "王道 - 啦啦队 (元气应援)",
        "prompt": "{prompt}, cheerleader costume, holding pom-poms, sports stadium background, jumping pose, high energy, dynamic angle, bright sunlight, sweat, cheering for you, genki girl",
        "negative_prompt": "tired, sad, sitting, night",
    },
    {
        "name": "王道 - 教室课桌 (同桌的你)",
        "prompt": "{prompt}, sitting at school desk, looking at camera (POV), sunlight streaming through window, dust motes, classroom background, daydreaming expression, innocent crush vibe, soft shadows",
        "negative_prompt": "teacher, dark, horror",
    },
    {
        "name": "王道 - 哥特萝莉 (暗黑童话)",
        "prompt": "{prompt}, gothic lolita fashion, black frills and ribbons, holding a red rose, mysterious garden background, dark fantasy atmosphere, dramatic lighting, doll-like makeup, elegant pose",
        "negative_prompt": "casual, sunny, happy, sport",
    },
    {
        "name": "王道 - 镜面舞蹈 (练习室)",
        "prompt": "{prompt}, dance practice studio, mirror reflection, wearing training wear (jersey), sweat, focused expression, dance studio lighting, candid behind the scenes look, hard work theme",
        "negative_prompt": "stage costume, concert, outdoor",
    },
    {
        "name": "王道 - 夏日祭浴衣 (花火)",
        "prompt": "{prompt}, wearing floral yukata, holding festival fan, night festival background with bokeh lanterns, turning back to look at viewer, soft flash photography, traditional japanese summer vibe",
        "negative_prompt": "western clothes, day time, winter",
    },
    {
        "name": "王道 - 公主茶会 (洛可可)",
        "prompt": "{prompt}, rococo style garden tea party, elegant princess dress, eating cake, white table and chairs, soft sunlight, pastel floral background, high society ojou-sama vibe, elegant",
        "negative_prompt": "poor, dirty, messy, dark",
    },
    {
        "name": "王道 - 雨中独舞 (透明伞)",
        "prompt": "{prompt}, dancing in the rain, holding clear umbrella, splashing water, dramatic backlighting, wet hair, emotional performance, blue and purple tones, cinematic music video shot",
        "negative_prompt": "sunny, dry, happy",
    },
    {
        "name": "王道 - 终场定格 (Ending Pose)",
        "prompt": "{prompt}, final ending pose of a concert, heavy breathing, looking directly at camera, extreme close-up, sweating, confetti stuck on hair, emotional smile, stage lights flaring behind, ending credit vibe",
        "negative_prompt": "beginning, clean, dry",
    },
    {
        "name": "王道 - 握手会 (神对应)",
        "prompt": "{prompt}, idol handshake event, view across the table, leaning forward to hold hands, plastic partition (optional), eye contact, very close proximity, genuine happy smile, blurred fans in background, indoor event hall lighting, POV shot",
        "negative_prompt": "distant, stage, dancing, angry",
    },
    {
        "name": "王道 - 签名拍立得 (物贩)",
        "prompt": "{prompt}, holding a sharpie marker, signing on a instax photo, looking up at camera, close-up shot, cute doodle on face, backstage or event booth background, interaction vibe, personal gift",
        "negative_prompt": "far away, full body, landscape",
    },
    {
        "name": "王道 - 直播营业 (Showroom)",
        "prompt": "{prompt}, smartphone selfie camera angle, vertical aspect ratio, wearing loungewear or casual clothes, ring light reflection in eyes, bedroom background, waving hand, reading comments, streaming interface overlay style, cozy atmosphere",
        "negative_prompt": "professional camera, studio, outdoor",
    },
    {
        "name": "王道 - 喂食视点 (啊~)",
        "prompt": "{prompt}, holding a spoon or fork with food towards camera (Saying Ahh), restaurant or cafe date, girlfriend POV, focus on face and food, blurred background, sweet expression, bokeh",
        "negative_prompt": "eating alone, messy, wide shot",
    },
    {
        "name": "王道 - 惊喜礼物 (递给你)",
        "prompt": "{prompt}, holding a wrapped gift box towards camera with both hands, shy blushing expression, bowing slightly, valentine or birthday vibe, school corridor or park background, confessing love, soft lighting",
        "negative_prompt": "taking gift, angry, rejecting",
    },
    {
        "name": "王道 - 车站送别 (不要走)",
        "prompt": "{prompt}, standing at train station platform, wearing coat and scarf, waving goodbye, teary eyes but smiling, train leaving in background, shinkansen, emotional cinematic shot, blue hour lighting",
        "negative_prompt": "happy, party, indoor, studio",
    },
    {
        "name": "王道 - 赖床女友 (早安)",
        "prompt": "{prompt}, lying in white bed sheets, rubbing eyes, messy morning hair, oversized white t-shirt, morning sunlight leaks, soft exposure, intimate POV, looking at viewer, pure and defenseless",
        "negative_prompt": "night, dark, heavy makeup, dress",
    },
    {
        "name": "王道 - 电车偶遇 (上学路)",
        "prompt": "{prompt}, sitting in japanese commuter train, school uniform, holding a school bag on lap, listening to music with earphones, looking out window then turning to camera, morning rush hour light, slice of life",
        "negative_prompt": "empty train, night, horror",
    },
    {
        "name": "王道 - 游乐园约会 (旋转木马)",
        "prompt": "{prompt}, sitting on a merry-go-round horse, night time amusement park, glowing lights, looking back at camera, laughing, bokeh light bubbles, romantic date vibe, fairytale atmosphere",
        "negative_prompt": "scary, day time, plain background",
    },
    {
        "name": "王道 - 躲猫猫 (偷看)",
        "prompt": "{prompt}, peeking from behind a curtain or wall, playful expression, hiding face partially, indoor studio, soft natural light, mischievous cute vibe, close up",
        "negative_prompt": "full body, far away, serious",
    },
    {
        "name": "王道 - 赛博歌姬 (电音风)",
        "prompt": "{prompt}, futuristic idol costume, holographic vinyl material, neon geometric background, laser beams, technopop perfume style, cool expression, cyan and magenta lighting, digital art aesthetic",
        "negative_prompt": "vintage, rustic, nature, soft",
    },
    {
        "name": "王道 - 摇滚甜心 (朋克风)",
        "prompt": "{prompt}, plaid skirt, leather jacket, holding an electric guitar, standing in a garage studio, rebellious but cute, avril lavigne style, dynamic angle, concert lighting, punk rock idol",
        "negative_prompt": "soft, elegant, traditional, quiet",
    },
    {
        "name": "王道 - 魔法少女 (变身)",
        "prompt": "{prompt}, magical girl transformation sequence, glowing ribbons and stars, floating in space, frilly battle costume, anime style effects, dynamic pose, vibrant rainbow colors, sailor moon vibe",
        "negative_prompt": "realistic, dark, gritty, plain",
    },
    {
        "name": "王道 - 森之精灵 (森女系)",
        "prompt": "{prompt}, wearing white cotton dress, barefoot, deep green forest background, sunbeams through trees (tyndall effect), holding a fern or flower, organic natural makeup, ethereal pure atmosphere",
        "negative_prompt": "urban, concrete, studio, flash",
    },
    {
        "name": "王道 - 昭和不良 (太妹风)",
        "prompt": "{prompt}, sukeban style long skirt school uniform, sailor collar, holding a wooden sword, leaning on graffiti wall, defiant expression, retro 80s film grain, warm sunset lighting, dramatic shadow",
        "negative_prompt": "cute, happy, smiling, modern",
    },
    {
        "name": "王道 - 侦探少女 (推理风)",
        "prompt": "{prompt}, wearing sherlock holmes style cape and hat, holding a magnifying glass, library background, curious expression, sepia tone filter, mystery novel cover style, intellectual cute",
        "negative_prompt": "sporty, beach, swimsuit, neon",
    },
    {
        "name": "王道 - 旗袍丸子头 (中华风)",
        "prompt": "{prompt}, modernized cute cheongsam (qipao), odango hair buns, holding a dim sum steamer, chinatown neon background, vibrant red and gold colors, festive energetic vibe, kung fu pose",
        "negative_prompt": "traditional, dark, sad, dull",
    },
    {
        "name": "王道 - 喵喵女仆 (猫耳娘)",
        "prompt": "{prompt}, wearing cat ears and maid outfit, paw pose, huge bell choker, pastel pink room background, floating yarn balls, anime aesthetic, super kawaii, soft focus",
        "negative_prompt": "realistic animal, horror, dark",
    },
    {
        "name": "王道 - 蒸汽波 (Vaporwave)",
        "prompt": "{prompt}, 90s anime aesthetic, pastel purple and blue gradient, glitch art effect, statue bust props, palm trees, nostalgic lo-fi vibe, retro computer graphics background, dreamy gaze",
        "negative_prompt": "hd, sharp, realistic, modern",
    },
    {
        "name": "王道 - 提线木偶 (人偶风)",
        "prompt": "{prompt}, posing like a marionette doll, strings attached to limbs (optional), ball jointed doll makeup, gothic theater stage background, stiff but elegant pose, surreal artistic vibe, spotlight",
        "negative_prompt": "natural movement, running, candid",
    },
    {
        "name": "王道 - 一日署长 (女警)",
        "prompt": "{prompt}, police uniform with mini skirt, saluting pose, standing in front of police car, handcuffs on belt, bright day light, authoritative but cute, justice vibe, official event photo",
        "negative_prompt": "bloody, criminal, dark, night",
    },
    {
        "name": "王道 - 治愈天使 (护士)",
        "prompt": "{prompt}, pastel pink nurse uniform, holding a clipboard or giant syringe prop, white hospital studio set, caring smile, soft high key lighting, dreamy medical theme, clean aesthetic",
        "negative_prompt": "scary, blood, dirty, horror",
    },
    {
        "name": "王道 - 元气店员 (快餐店)",
        "prompt": "{prompt}, american diner waitress uniform, roller skates, holding a milkshake tray, checkered floor, neon jukebox background, 50s retro pop vibe, bubblegum colors, energetic smile",
        "negative_prompt": "dark, fancy restaurant, sad",
    },
    {
        "name": "王道 - 巫女祈福 (新年)",
        "prompt": "{prompt}, traditional japanese miko outfit (red hakama white top), holding a omamori charm, shinto shrine background, falling snow, serene expression, new year wish, spiritual atmosphere",
        "negative_prompt": "modern, neon, western clothes",
    },
    {
        "name": "王道 - 乘务员 (空姐)",
        "prompt": "{prompt}, flight attendant uniform, scarf around neck, pulling a carry-on suitcase, airport terminal background, walking confidently, travel show vibe, professional elegance",
        "negative_prompt": "messy, casual, home, sleeping",
    },
    {
        "name": "王道 - 棒球经理 (运动系)",
        "prompt": "{prompt}, wearing baseball team jersey and cap, holding a clipboard and whistle, baseball dugout background, watching the game, sunset golden hour, youth sports drama vibe, ponytail",
        "negative_prompt": "indoor, studio, dark, night",
    },
    {
        "name": "王道 - 美术生 (画室)",
        "prompt": "{prompt}, wearing apron covered in colorful paint, holding a palette and brush, art studio background with canvas, paint on cheek, creative messy vibe, warm light, artistic",
        "negative_prompt": "clean, sterile, office, suit",
    },
    {
        "name": "王道 - 图书委员 (文学少女)",
        "prompt": "{prompt}, school library background, standing between bookshelves, wearing glasses, holding a heavy book, shushing gesture (finger on lips), quiet atmosphere, intellectual beauty",
        "negative_prompt": "loud, party, sport, outdoor",
    },
    {
        "name": "王道 - 实验课 (理科女)",
        "prompt": "{prompt}, wearing white lab coat, protective goggles, holding a test tube with colored liquid, chemistry classroom background, curious expression, science experiment vibe, bright lighting",
        "negative_prompt": "dark, magic, fantasy, outdoor",
    },
    {
        "name": "王道 - 婚礼幻想 (花嫁)",
        "prompt": "{prompt}, pure white wedding dress, holding a bouquet of white roses, chapel background with stained glass, veil lifting, shy happy smile, ideal bride concept, soft glow effect",
        "negative_prompt": "black dress, funeral, sad, gothic",
    },
    {
        "name": "王道 - 录音棚 (认真模式)",
        "prompt": "{prompt}, wearing large professional headphones, standing in front of pop filter microphone, recording studio booth, sheet music in hand, serious singing expression, dimly lit with mood lighting, artist vibe",
        "negative_prompt": "dancing, stage, outdoor, playful",
    },
    {
        "name": "王道 - 烟火大会 (仙女棒)",
        "prompt": "{prompt}, holding a sparkler firework, beach at night, sparks flying, illuminating face with warm glow, yukata or summer dress, emotional nostalgic vibe, summer memory",
        "negative_prompt": "day time, bright sun, studio",
    },
    {
        "name": "王道 - 水族馆 (蓝色梦境)",
        "prompt": "{prompt}, silhouette against a giant aquarium tank, blue ambient lighting, watching fish and jellyfish, reflection on glass, quiet romantic date, dreamy and mysterious, side profile",
        "negative_prompt": "bright white light, outdoor, park",
    },
    {
        "name": "王道 - 街机厅 (夹娃娃)",
        "prompt": "{prompt}, standing in front of UFO catcher machine, pressing buttons, colorful neon arcade lights, reflection on glass, focused cute expression, playful date vibe, vibrant colors",
        "negative_prompt": "nature, forest, rustic, quiet",
    },
    {
        "name": "王道 - 甜品探店 (吃货)",
        "prompt": "{prompt}, sitting at a trendy cafe, giant pancake or parfait on table, holding fork, happy foodie expression, bright window natural light, pastel interior, casual date",
        "negative_prompt": "dark, bar, alcohol, night",
    },
    {
        "name": "王道 - 河提骑行 (风)",
        "prompt": "{prompt}, riding a bicycle along the river bank, wind blowing hair and skirt, blue sky and green grass, wide angle shot, energetic youth, anime opening theme vibe, motion blur",
        "negative_prompt": "indoor, stationary, night, rain",
    },
    {
        "name": "王道 - 豪车派对 (名流感)",
        "prompt": "{prompt}, sitting inside a stretch limousine, holding a glass of champagne (or juice), party dress, disco lights inside, luxury leather seats, night out vibe, rich idol aesthetic",
        "negative_prompt": "bus, train, cheap, dirty",
    },
    {
        "name": "王道 - 雪夜围巾 (呼气)",
        "prompt": "{prompt}, thick knitted scarf covering mouth, winter coat, snowing at night, street lights, white breath vapor visible, cold but cozy, waiting for someone, romantic winter drama",
        "negative_prompt": "summer, sweat, beach, swimsuit",
    },
    {
        "name": "王道 - 逆光剪影 (登场前)",
        "prompt": "{prompt}, silhouette shot, standing at the entrance of stage curtain, bright stage lights beaming through, back view or side view, outline of body, anticipation atmosphere, atmospheric",
        "negative_prompt": "front view, clear face, flat lighting",
    },
    {
        "name": "王道 - 庆功宴 (干杯)",
        "prompt": "{prompt}, holding a glass for a toast (kanpai), restaurant background, blurred food dishes, cheerful smile, looking at camera, casual clothes, after party vibe, warm izakaya lighting",
        "negative_prompt": "stage, formal, serious, sad",
    },
    {
        "name": "过渡 - 连帽衫下的秘密 (Hoodie & Bikini)",
        "prompt": "{prompt}, wearing an oversized grey zip-up hoodie (unzipped), colorful bikini visible underneath, casual street fashion, standing on balcony, morning sunlight, shy smile, pulling hoodie strings, boyfriend POV, gap moe (contrast)",
        "negative_prompt": "nudity, nipples, lewd, dark, dirty",
    },
    {
        "name": "过渡 - 湿身白衬衫 (Wet Shirt)",
        "prompt": "{prompt}, wearing an oversized white dress shirt, soaked with water, translucent fabric sticking to skin, swimsuit or lingerie faintly visible underneath, beach or pool background, playful splashing, high key lighting, summer gravure style",
        "negative_prompt": "dry, thick fabric, full nudity",
    },
    {
        "name": "过渡 - 瑜伽伸展 (Yoga Time)",
        "prompt": "{prompt}, wearing tight yoga leggings and sports bra, doing stretching exercise on yoga mat, living room background, sweat on skin, body curves highlighted by lighting, healthy beauty, ponytail, focus on fitness",
        "negative_prompt": "bed, lingerie, sexual act, messy",
    },
    {
        "name": "过渡 - 晨跑结束 (Jogging)",
        "prompt": "{prompt}, wearing running shorts and crop top, drinking water from bottle, park background, morning sun, sweating, heavy breathing, dynamic angle, healthy thighs, energetic vibe",
        "negative_prompt": "night, indoor, dark, pajamas",
    },
    {
        "name": "过渡 - 温泉裹巾 (Onsen Mist)",
        "prompt": "{prompt}, wrapped in a white bath towel, sitting on the edge of open-air hot spring (onsen), steam rising, snowy scenery in background, blushing cheeks, wet hair, skin glistening, japanese gravure aesthetic, soft focus",
        "negative_prompt": "swimsuit, modern pool, western bath",
    },
    {
        "name": "过渡 - 刚睡醒 (Oversized T)",
        "prompt": "{prompt}, wearing only a very long oversized t-shirt, sitting on bed with knees up (no panty shot), messy hair, rubbing eyes, thighs visible, soft morning light, innocent but suggestive, girlfriend pov",
        "negative_prompt": "pants, jeans, dress, dark",
    },
    {
        "name": "日系雨夜透明伞 (电影感)",
        "prompt": "{prompt}, holding a clear vinyl umbrella, rainy night in Tokyo, rain droplets, neon lights reflecting on wet street, cinematic bokeh, emotional atmosphere, street photography, sharp focus on face, glowing city background",
        "negative_prompt": "sunny, dry, daytime, opaque umbrella",
    },
    {
        "name": "日系深夜便利店 (生活感)",
        "prompt": "{prompt}, inside a japanese convenience store (konbini), holding a drink or snack, standing in front of colorful product shelves, bright fluorescent lighting, glass reflection, candid shot, late night vibe, clear facial features",
        "negative_prompt": "dark, dim lighting, empty shelves, horror",
    },
    {
        "name": "日系对镜自拍 (OOTD风)",
        "prompt": "{prompt}, mirror selfie, holding smartphone covering face, reflection in mirror, bathroom mirror or fitting room, flash reflection on glass, focus on outfit, messy room background, daily life vibe, casual aesthetic",
        "negative_prompt": "camera lens visible, professional studio, no phone",
    },
    {
        "name": "日系JK手机自拍 (大头贴风)",
        "prompt": "{prompt}, selfie shot, holding camera, wide angle, shot on iPhone, flash photography, messy hair, playful, candid moment, social media quality, slight motion blur",
        "negative_prompt": "professional lighting, tripod, perfect posture",
    },
    {
        "name": "日系灵魂特写 (极致细节)",
        "prompt": "{prompt}, photography, visible eyelashes, detailed skin texture, sunlight hitting the face, emotional expression, 8k resolution, raw photo",
        "negative_prompt": "blur, low resolution, painting, illustration",
    },
    {
        "name": "日系清新 (透明感)",
        "prompt": "{prompt}, Japanese photography style, high key lighting, soft natural light, clean background, slight overexposure, low contrast, airy atmosphere, pale cyan and white tones, transparent feel",
        "negative_prompt": "heavy shadows, high contrast, dark atmosphere, grunge",
    },
    {
        "name": "日系木漏れ日 (树隙光)",
        "prompt": "{prompt}, komorebi, dappled sunlight filtering through trees, shadows of leaves on face, peaceful nature atmosphere, sunspots, gentle breeze feeling, 35mm film look",
        "negative_prompt": "studio lighting, artificial light, harsh shadows",
    },
    {
        "name": "日系蓝调时刻 (清冷情绪)",
        "prompt": "{prompt}, blue hour photography, cold color temperature, melancholic atmosphere, dim lighting, soft twilight, cinematic teal tones, emotional movie scene, solitude",
        "negative_prompt": "warm colors, sunset, bright sunlight, cheerful",
    },
    {
        "name": "日系唯美逆光 (夕阳)",
        "prompt": "{prompt}, golden hour, strong backlight, rim light, sun flare, lens flare, warm haze, silhouette, romantic atmosphere, emotional, glowing hair",
        "negative_prompt": "flat lighting, front lighting, cool colors",
    },
    {
        "name": "日系昭和胶片 (怀旧风)",
        "prompt": "{prompt}, retro japanese film look, showa era style, film grain, noise, faded colors, nostalgic mood, warm vintage filter, slightly blurred, fujifilm simulation",
        "negative_prompt": "4k, sharp focus, digital clean look, modern style",
    },
    {
        "name": "日系窗边侧光 (生活感)",
        "prompt": "{prompt}, soft window light, side lighting, sheer curtains, indoor slice of life, cozy atmosphere, domestic setting, natural shadows, intimate feel, Hirokazu Kore-eda style",
        "negative_prompt": "outdoor, dramatic lighting, fantasy",
    },
    {
        "name": "日系雨夜霓虹 (都市忧郁)",
        "prompt": "{prompt}, rainy night in Tokyo, wet street reflections, neon lights reflecting on wet surfaces, bokeh city lights, umbrella, cyberpunk vibes but realistic, moody cinematic lighting",
        "negative_prompt": "daytime, dry, countryside, sunshine",
    },
    {
        "name": "日系自动贩卖机 (孤独光源)",
        "prompt": "{prompt}, illuminated by vending machine light, night street, soft artificial glow on face, cold fluorescence, urban loneliness, cinematic night scene, dark surroundings",
        "negative_prompt": "sunlight, natural light, bright background",
    },
    {
        "name": "日系夏日过曝 (青春感)",
        "prompt": "{prompt}, intense summer sunlight, blinding white sky, high contrast, vibrant greens and blues, sweat, heat haze, youth drama style, energetic, overexposed highlights",
        "negative_prompt": "winter, snow, dark, cloudy",
    },
    {
        "name": "日系教室自然光 (校园剧)",
        "prompt": "{prompt}, classroom setting, sunlight through windows, dust motes, chalk dust, nostalgic school life, soft shadows, afternoon atmosphere, seishun (youth) drama vibes",
        "negative_prompt": "night, office, horror",
    },
    {
        "name": "日系花火大会 (多彩面光)",
        "prompt": "{prompt}, illuminated by fireworks, colorful light reflections on face, yukata, night festival, dark sky background, festive but emotional, soft colorful glow, bokeh fireworks",
        "negative_prompt": "daytime, white light, studio light",
    },
    {
        "name": "日系电车通勤 (冷淡风)",
        "prompt": "{prompt}, subway train interior, fluorescent ceiling lights, reflection in glass window, sterile atmosphere, cool tones, motion blur background, urban solitude, cinematic shot",
        "negative_prompt": "warm lighting, cozy, nature",
    },
    {
        "name": "日系海边朦胧 (空气感)",
        "prompt": "{prompt}, seaside, overcast sky, diffused soft light, misty horizon, pale blue and grey tones, windblown hair, melancholic seascape, soft focus, ethereal",
        "negative_prompt": "bright sun, saturated colors, sharp details",
    },
    {
        "name": "日系居酒屋 (暖调灯笼)",
        "prompt": "{prompt}, izakaya interior, warm lantern lighting, orange and red tones, dim ambient light, bokeh bottles background, lively but cozy, intimate depth of field",
        "negative_prompt": "cold light, blue tones, clinical",
    },
    {
        "name": "日系柔光人像 (少女漫改)",
        "prompt": "{prompt}, soft focus filter, bloom effect, glowing skin, angelic lighting, dreamy romance, shoujo manga live action style, pastel color palette, gentle atmosphere",
        "negative_prompt": "gritty, realistic texture, hard contrast",
    },
    {
        "name": "日系隧道光影 (对比构图)",
        "prompt": "{prompt}, inside a tunnel, silhouette against bright exit, green fluorescent tunnel lights, symmetrical composition, cinematic depth, mystery, road movie vibe",
        "negative_prompt": "cluttered, flat lighting",
    },
    {
        "name": "日系雪景散射 (纯白世界)",
        "prompt": "{prompt}, snowy day, overcast lighting, diffuse white light, low contrast, muted colors, soft texture, silent atmosphere, Love Letter (movie) vibe, breath vapor",
        "negative_prompt": "sunny, colorful, high contrast",
    },
    {
        "name": "日系便利店流光 (现代生活)",
        "prompt": "{prompt}, convenience store interior, bright fluorescent strips, clean white lighting, colorful product shelves background, glass reflections, modern japan daily life",
        "negative_prompt": "dim, vintage, dirty",
    },
    {
        "name": "日系黄昏魔术时刻 (紫霞)",
        "prompt": "{prompt}, magic hour, purple and pink sky gradients, fading light, silhouettes, anime background style (Makoto Shinkai style), dramatic clouds, sentimental atmosphere",
        "negative_prompt": "midday, pure blue sky, pitch black",
    },
    {
        "name": "日系胶卷漏光 (艺术MV)",
        "prompt": "{prompt}, heavy light leaks, film burn effects, artistic experimental photography, prism refraction, random color overlay, vintage music video style, imperfect aesthetic",
        "negative_prompt": "clean image, digital perfection, standard lighting",
    },
    {
        "name": "日系赛博歌姬 (未来科幻)",
        "prompt": "{prompt}, cyberpunk tokyo, futuristic idol costume, neon glowing headphones, holographic interface, chromatic aberration, rainy neon street background, mechanical details, cool blue and purple lighting, sci-fi movie atmosphere, cinematic composition",
        "negative_prompt": "vintage, rustic, natural, warm colors",
    },
    {
        "name": "日系绝美和服 (大和抚子)",
        "prompt": "{prompt}, wearing elaborate colorful kimono with gold patterns, traditional japanese hairstyle with kanzashi hair ornaments, standing in a tatami room, sliding doors (shoji) background, falling cherry blossoms, soft warm lantern light, elegant pose, mysterious japanese beauty, cinematic historical drama vibe",
        "negative_prompt": "modern clothes, glasses, neon lights, messy background",
    },
    {
        "name": "空气透视 (丁达尔光)",
        "prompt": "{prompt}, floating dust particles in the light rays, tyndall effect, hazy atmosphere, god rays, volumetric lighting",
        "negative_prompt": "",
    },
    {
        "name": "梦幻景深 (大光圈)",
        "prompt": "{prompt}, Macro photography, extreme close-up, bokeh background, shallow depth of field, f/1.8 aperture, dreamy light leaks",
        "negative_prompt": "",
    },
    {
        "name": "伦勃朗光 (经典人像)",
        "prompt": "{prompt}, Rembrandt lighting, chiaroscuro, dramatic shadows, artistic contrast, masterpiece",
        "negative_prompt": "",
    },
    {
        "name": "爱心光斑 (创意)",
        "prompt": "{prompt}, heart shaped bokeh, shaped bokeh background, romantic atmosphere, night city background, f/1.2",
        "negative_prompt": "",
    },
    {
        "name": "电影侧逆光 (轮廓光)",
        "prompt": "{prompt}, backlit, rim lighting, golden halo effect around hair, silhouette against light, cinematic atmosphere",
        "negative_prompt": "",
    },
    {
        "name": "柔光箱摄影 (商业大片)",
        "prompt": "{prompt}, soft lighting, beauty dish, professional fashion photography, even lighting, flawless skin",
        "negative_prompt": "",
    },
    {
        "name": "赛博霓虹 (夜景)",
        "prompt": "{prompt}, cyberpunk city night, neon lights reflection, blue and purple color grading, wet street, futuristic vibe",
        "negative_prompt": "",
    },
    {
        "name": "情绪侧写 (Profile)",
        "prompt": "{prompt}, side profile, looking away, emotional expression, rim lighting, storytelling, cinematic composition, magical atmosphere",
        "negative_prompt": "looking at camera, front view",
    },
    {
        "name": "黄金时刻 (夕阳)",
        "prompt": "{prompt}, golden hour lighting, warm sunlight, sunset glow, long shadows, romantic atmosphere, lens flare",
        "negative_prompt": "",
    },
    {
        "name": "蓝色时刻 (清晨/黄昏)",
        "prompt": "{prompt}, blue hour, moody cold tones, dim lighting, cinematic color grading, melancholic vibe",
        "negative_prompt": "",
    },
    {
        "name": "自然窗光 (居家感)",
        "prompt": "{prompt}, natural sunlight streaming through window, soft shadows, cozy indoor atmosphere, morning vibe",
        "negative_prompt": "",
    },
    {
        "name": "暗调奢华 (Low Key)",
        "prompt": "{prompt}, low key lighting, dark background, mysterious atmosphere, elegant shadows, noir style",
        "negative_prompt": "",
    },
    # ========================
    # 📸 摄影与胶片质感 (Film Stocks)
    # ========================
    {
        "name": "Kodak Portra 400 (人像胶片)",
        "prompt": "{prompt}, shot on Kodak Portra 400, warm grain, analog photography, vintage film look, nostalgic",
        "negative_prompt": "",
    },
    {
        "name": "Fujifilm Velvia (日系清冷)",
        "prompt": "{prompt}, shot on Fujifilm Velvia, vivid colors, slight green tint, japanese aesthetic, clean and crisp",
        "negative_prompt": "",
    },
    {
        "name": "Polaroid (拍立得)",
        "prompt": "{prompt}, Polaroid vintage photo, camera flash, soft focus, vignette, instant film aesthetic, candid shot",
        "negative_prompt": "",
    },
    {
        "name": "徕卡黑白 (Monochrome)",
        "prompt": "{prompt}, black and white photography, Leica M6, high contrast, grain, emotional, timeless",
        "negative_prompt": "",
    },
    {
        "name": "一次性相机 (闪光灯)",
        "prompt": "{prompt}, disposable camera, direct flash, harsh lighting, 90s party vibe, candid, raw aesthetics",
        "negative_prompt": "",
    },
    {
        "name": "8mm 电影胶片 (复古)",
        "prompt": "{prompt}, Super 8mm film frame, film grain, scratches, dust, vintage movie look, color bleed",
        "negative_prompt": "",
    },
    {
        "name": "Lomography (Lomo风格)",
        "prompt": "{prompt}, Lomography style, oversaturated colors, heavy vignette, cross processing, experimental",
        "negative_prompt": "",
    },
    {
        "name": "GoPro (广角)",
        "prompt": "{prompt}, GoPro wide angle shot, fisheye lens effect, immersive perspective, action camera",
        "negative_prompt": "",
    },
    {
        "name": "CCTV (监控视角)",
        "prompt": "{prompt}, CCTV footage, security camera view, grainy, low resolution style, timestamp overlay, surveillance",
        "negative_prompt": "",
    },
    {
        "name": "湿版摄影 (古董感)",
        "prompt": "{prompt}, Wet plate collodion photography, vintage 19th century style, imperfections, silver plate texture",
        "negative_prompt": "",
    },
    # ========================
    # 🎨 艺术与插画风格 (Art Styles)
    # ========================
    {
        "name": "油画 (古典)",
        "prompt": "{prompt}, classic oil painting, visible brushstrokes, textured canvas, renaissance style, masterpiece",
        "negative_prompt": "photo, realistic",
    },
    {
        "name": "水彩画 (清新)",
        "prompt": "{prompt}, watercolor painting, soft edges, pastel colors, artistic splatter, wet on wet technique",
        "negative_prompt": "photo, realistic",
    },
    {
        "name": "新海诚 (动漫背景)",
        "prompt": "{prompt}, anime style, Makoto Shinkai style, highly detailed clouds, vibrant blue sky, cinematic anime art",
        "negative_prompt": "photo, realistic",
    },
    {
        "name": "赛博朋克动画 (Edgerunners)",
        "prompt": "{prompt}, Studio Trigger style, vibrant neon colors, sharp outlines, dynamic composition, anime aesthetic",
        "negative_prompt": "photo, realistic",
    },
    {
        "name": "皮克斯 3D (迪士尼)",
        "prompt": "{prompt}, Pixar style 3D render, cute features, smooth textures, ambient occlusion, cinema 4d, redshift",
        "negative_prompt": "",
    },
    {
        "name": "虚幻引擎 5 (CG写实)",
        "prompt": "{prompt}, Unreal Engine 5 render, 8k resolution, ray tracing, digital human, octane render, 3D masterpiece",
        "negative_prompt": "",
    },
    {
        "name": "浮世绘 (日本传统)",
        "prompt": "{prompt}, Ukiyo-e art style, woodblock print, flat colors, traditional japanese art, Hokusai style",
        "negative_prompt": "photo, realistic",
    },
    {
        "name": "素描 (铅笔)",
        "prompt": "{prompt}, pencil sketch, graphite drawing, rough lines, shading, sketchbook style, monochrome",
        "negative_prompt": "color, photo",
    },
    {
        "name": "概念艺术 (Concept Art)",
        "prompt": "{prompt}, digital concept art, matte painting, epic scale, highly detailed, artstation trending",
        "negative_prompt": "",
    },
    {
        "name": "波普艺术 (Warhol)",
        "prompt": "{prompt}, Pop Art style, Andy Warhol style, bold colors, halftone dots, comic book aesthetic",
        "negative_prompt": "photo",
    },
    # ========================
    # 👗 时尚与穿搭Vibe (Fashion)
    # ========================
    {
        "name": "Vogue 杂志封面",
        "prompt": "{prompt}, Vogue editorial, high fashion, studio lighting, stylish outfit, fashion magazine cover shot",
        "negative_prompt": "",
    },
    {
        "name": "街头潮牌 (Streetwear)",
        "prompt": "{prompt}, hypebeast style, streetwear fashion, urban background, sneakers, hoodie, candid street shot",
        "negative_prompt": "",
    },
    {
        "name": "老钱风 (Old Money)",
        "prompt": "{prompt}, old money aesthetic, quiet luxury, ralph lauren style, country club, elegant, vintage vibe",
        "negative_prompt": "",
    },
    {
        "name": "Y2K 千禧辣妹",
        "prompt": "{prompt}, Y2K aesthetic, 2000s fashion, glossy, pink retro vibe, butterfly clips, low rise jeans",
        "negative_prompt": "",
    },
    {
        "name": "哥特风 (Goth)",
        "prompt": "{prompt}, gothic fashion, dark makeup, black lace, victorian goth, moody atmosphere, pale skin",
        "negative_prompt": "",
    },
    {
        "name": "机能风 (Techwear)",
        "prompt": "{prompt}, techwear fashion, futuristic clothing, straps and buckles, urban ninja, cyberpunk city background",
        "negative_prompt": "",
    },
    {
        "name": "极简主义 (Minimalist)",
        "prompt": "{prompt}, minimalist photography, clean background, neutral colors, simple composition, negative space",
        "negative_prompt": "",
    },
    {
        "name": "维密秀 (天使)",
        "prompt": "{prompt}, Victoria's Secret runway style, angel wings, glamour, stage lighting, confetti, lingerie model",
        "negative_prompt": "",
    },
    {
        "name": "汉服/古风",
        "prompt": "{prompt}, wearing traditional Chinese Hanfu, ancient chinese garden background, ethereal, wuxia style",
        "negative_prompt": "",
    },
    {
        "name": "办公室穿搭 (Office)",
        "prompt": "{prompt}, professional office wear, blazer, modern office background, confident businesswoman look",
        "negative_prompt": "",
    },
    # ========================
    # 🎬 著名导演/电影风格 (Directors)
    # ========================
    {
        "name": "韦斯·安德森 (对称/粉彩)",
        "prompt": "{prompt}, Wes Anderson style, symmetrical composition, pastel color palette, whimsical, grand budapest hotel vibe",
        "negative_prompt": "",
    },
    {
        "name": "王家卫 (香港霓虹)",
        "prompt": "{prompt}, Wong Kar-wai style, motion blur, neon lights, step printing, cinematic hong kong vibe, emotional",
        "negative_prompt": "",
    },
    {
        "name": "银翼杀手 2049 (橙色废土)",
        "prompt": "{prompt}, Blade Runner 2049 style, orange hazy atmosphere, massive architecture, futuristic dystopian",
        "negative_prompt": "",
    },
    {
        "name": "黑客帝国 (绿色代码)",
        "prompt": "{prompt}, The Matrix style, green color grading, digital rain code background, leather trench coat, sci-fi",
        "negative_prompt": "",
    },
    {
        "name": "吉卜力 (Ghibli)",
        "prompt": "{prompt}, Studio Ghibli style, Miyazaki art, beautiful watercolor background, vibrant colors, anime food",
        "negative_prompt": "photo, realistic",
    },
    {
        "name": "沙丘 (Dune)",
        "prompt": "{prompt}, Dune movie style, desert planet, muted beige colors, epic scale, utilitarian fashion, cinematic",
        "negative_prompt": "",
    },
    {
        "name": "美剧亢奋 (Euphoria)",
        "prompt": "{prompt}, Euphoria TV show style, glitter makeup, purple and blue neon lighting, emotional, dreamy",
        "negative_prompt": "",
    },
    {
        "name": "权力的游戏 (中世纪)",
        "prompt": "{prompt}, Game of Thrones style, medieval fantasy, gritty texture, castle background, fur cloak, dramatic",
        "negative_prompt": "",
    },
    {
        "name": "罪恶之城 (黑白红)",
        "prompt": "{prompt}, Sin City style, high contrast black and white, selective color red, comic book noir",
        "negative_prompt": "",
    },
    {
        "name": "布里奇顿 (摄政风)",
        "prompt": "{prompt}, Bridgerton style, regency era fashion, pastel garden, floral, romantic, elegant",
        "negative_prompt": "",
    },
    # ========================
    # 🌦️ 季节与天气 (Weather)
    # ========================
    {
        "name": "樱花季 (春)",
        "prompt": "{prompt}, cherry blossoms falling, spring season, pink petals, soft romantic atmosphere, park background",
        "negative_prompt": "",
    },
    {
        "name": "雨夜 (Rain)",
        "prompt": "{prompt}, heavy rain, wet skin, reflection on ground, umbrella, moody rainy night, cinematic",
        "negative_prompt": "",
    },
    {
        "name": "暴风雪 (Winter)",
        "prompt": "{prompt}, heavy blizzard, snow falling, winter fashion, frost on eyelashes, cold atmosphere, white background",
        "negative_prompt": "",
    },
    {
        "name": "热浪 (Summer)",
        "prompt": "{prompt}, summer heatwave, sweating skin, bright harsh sunlight, beach background, mirage effect",
        "negative_prompt": "",
    },
    {
        "name": "秋日落叶 (Fall)",
        "prompt": "{prompt}, autumn season, orange and red leaves, forest background, cozy sweater, warm tone",
        "negative_prompt": "",
    },
    {
        "name": "迷雾森林 (Fog)",
        "prompt": "{prompt}, thick fog, misty forest, mysterious atmosphere, silent hill vibe, low visibility",
        "negative_prompt": "",
    },
    {
        "name": "雷暴 (Lightning)",
        "prompt": "{prompt}, thunderstorm background, lightning bolts, dramatic sky, dark clouds, powerful atmosphere",
        "negative_prompt": "",
    },
    {
        "name": "极光 (Aurora)",
        "prompt": "{prompt}, aurora borealis background, starry night sky, magical atmosphere, green and purple lights",
        "negative_prompt": "",
    },
    {
        "name": "彩虹 (Rainbow)",
        "prompt": "{prompt}, double rainbow in background, after rain, bright and cheerful, vivid colors",
        "negative_prompt": "",
    },
    {
        "name": "多云阴天 (柔光)",
        "prompt": "{prompt}, overcast sky, diffused lighting, soft shadows, moody portrait, neutral colors",
        "negative_prompt": "",
    },
    # ========================
    # 🧪 创意与特效 (Creative)
    # ========================
    {
        "name": "双重曝光 (Double Exposure)",
        "prompt": "{prompt}, double exposure art, silhouette combined with forest landscape, artistic, dreamlike",
        "negative_prompt": "",
    },
    {
        "name": "故障艺术 (Glitch)",
        "prompt": "{prompt}, glitch art style, digital distortion, pixel sorting, chromatic aberration, cyberpunk vibe",
        "negative_prompt": "",
    },
    {
        "name": "赛博机械姬 (Cyborg)",
        "prompt": "{prompt}, cyborg features, robotic arm, metal skin parts, glowing wires, sci-fi portrait",
        "negative_prompt": "",
    },
    {
        "name": "生物发光 (Avatar)",
        "prompt": "{prompt}, bioluminescent skin, glowing patterns, avatar style, night forest, magical",
        "negative_prompt": "",
    },
    {
        "name": "大理石雕像",
        "prompt": "{prompt}, marble statue style, classical sculpture, museum lighting, white stone texture",
        "negative_prompt": "human skin, color",
    },
    {
        "name": "瓷娃娃 (Porcelain)",
        "prompt": "{prompt}, porcelain doll look, cracks on face, glossy ceramic texture, surreal, creepy cute",
        "negative_prompt": "",
    },
    {
        "name": "霓虹泼墨",
        "prompt": "{prompt}, neon paint splatter, UV light, glowing makeup, blacklight party, artistic chaos",
        "negative_prompt": "",
    },
    {
        "name": "水中摄影",
        "prompt": "{prompt}, underwater photography, floating hair, bubbles, light refraction, blue tones, serene",
        "negative_prompt": "",
    },
    {
        "name": "碎玻璃特效",
        "prompt": "{prompt}, seen through broken glass, shattered mirror effect, reflection shards, dramatic",
        "negative_prompt": "",
    },
    {
        "name": "HDR 高动态范围",
        "prompt": "{prompt}, HDR photography, high dynamic range, vivid details, hyperrealistic, clarity",
        "negative_prompt": "",
    },
    # ========================
    # 🎥 镜头视角 (Angles)
    # ========================
    {
        "name": "超低角度 (英雄视角)",
        "prompt": "{prompt}, extreme low angle shot, looking up at subject, heroic stance, epic sky background",
        "negative_prompt": "",
    },
    {
        "name": "俯视镜头 (Drone)",
        "prompt": "{prompt}, high angle shot, drone view, looking down, birds eye view, interesting perspective",
        "negative_prompt": "",
    },
    {
        "name": "荷兰倾斜角 (动态)",
        "prompt": "{prompt}, dutch angle shot, tilted camera, dynamic composition, uneasy atmosphere, action movie vibe",
        "negative_prompt": "",
    },
    {
        "name": "自拍视角 (Selfie)",
        "prompt": "{prompt}, selfie angle, holding camera, looking at lens, casual vibe, phone camera quality",
        "negative_prompt": "",
    },
    {
        "name": "背影 (Mystery)",
        "prompt": "{prompt}, view from behind, walking away, looking at horizon, mysterious, storytelling",
        "negative_prompt": "face",
    },
    {
        "name": "鱼眼镜头",
        "prompt": "{prompt}, fisheye lens, distorted perspective, spherical effect, 90s music video style",
        "negative_prompt": "",
    },
    {
        "name": "移轴摄影 (微缩模型)",
        "prompt": "{prompt}, tilt-shift photography, miniature effect, blurred top and bottom, toy-like city",
        "negative_prompt": "",
    },
    {
        "name": "第一人称 (FPS)",
        "prompt": "{prompt}, POV shot, first person perspective, reaching out hand, immersive",
        "negative_prompt": "",
    },
    {
        "name": "动态模糊 (Motion)",
        "prompt": "{prompt}, motion blur background, moving fast, rushing, dynamic speed lines",
        "negative_prompt": "",
    },
    {
        "name": "超特写 (眼部)",
        "prompt": "{prompt}, extreme close-up on eyes, detailed iris, macro eyelashes, intense gaze",
        "negative_prompt": "",
    },
    {
        "name": "经典街拍风(纽约)",
        "prompt": "Photorealistic, a stunningly beautiful blonde woman with blue eyes, New York City street style. She is {prompt}, walking confidently down a street in SoHo. Soft, natural afternoon light. Shot on 35mm film.",
        "negative_prompt": "",
    },
    {
        "name": "时尚大片风(纽约 Vogue)",
        "prompt": "Fashion editorial style photo, a gorgeous supermodel with long, wavy honey-blonde hair. Posing on {prompt}. She has a cool, sophisticated expression. Wearing a stylish trench coat. Cinematic lighting, ultra detailed.",
        "negative_prompt": "",
    },
    {
        "name": "甜美邻家风(纽约)",
        "prompt": "A beautiful young woman with bright blonde hair and a friendly smile, {prompt}. She is wearing a cute sweater and jeans. The scene is warm and inviting. Shallow depth of field, sharp focus on her face.",
        "negative_prompt": "",
    },
    {
        "name": "时尚大片风(可变服装)",
        "prompt": "Fashion editorial style photo, a gorgeous supermodel with long, wavy honey-blonde hair. Posing on a rooftop overlooking the Manhattan skyline at sunset. She has a cool, sophisticated expression. Wearing {prompt}. Cinematic lighting, ultra detailed.",
        "negative_prompt": "",
    },
    {
        "name": "动画4引擎",
        "prompt": "{prompt}, depth of field, faux traditional media, painterly, impressionism, photo background",
        "negative_prompt": "",
    },
    {
        "name": "绘画",
        "prompt": "{prompt}, painterly, painting (medium)",
        "negative_prompt": "",
    },
    {"name": "像素艺术", "prompt": "{prompt}, pixel art", "negative_prompt": ""},
    {
        "name": "1980年代",
        "prompt": "{prompt}, 1980s (style), retro artstyle",
        "negative_prompt": "",
    },
    {
        "name": "1990年代",
        "prompt": "{prompt}, 1990s (style), retro artstyle",
        "negative_prompt": "",
    },
    {
        "name": "2000年代",
        "prompt": "{prompt}, 2000s (style), retro artstyle",
        "negative_prompt": "",
    },
    {"name": "卡通", "prompt": "{prompt}, toon (style)", "negative_prompt": ""},
    {
        "name": "线条艺术",
        "prompt": "{prompt}, lineart, thick lineart",
        "negative_prompt": "",
    },
    {"name": "新艺术", "prompt": "{prompt}, art nouveau", "negative_prompt": ""},
    {
        "name": "西方漫画",
        "prompt": "{prompt}, western comics (style)",
        "negative_prompt": "",
    },
    {"name": "3D", "prompt": "{prompt}, 3d", "negative_prompt": ""},
    {
        "name": "写实",
        "prompt": "{prompt}, realistic, photorealistic",
        "negative_prompt": "",
    },
    {"name": "荧光朋克", "prompt": "{prompt}, neonpunk", "negative_prompt": ""},
    {
        "name": "电影风格",
        "prompt": "{prompt}, cinematic still, emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "nsfw, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "摄影风格",
        "prompt": "{prompt}, cinematic photo, 35mm photograph, film, bokeh, professional, 8k, highly detailed",
        "negative_prompt": "nsfw, drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
    },
    {
        "name": "动漫风格",
        "prompt": "{prompt}, anime artwork, anime style, key visual, vibrant, studio anime, highly detailed",
        "negative_prompt": "nsfw, photo, deformed, black and white, realism, disfigured, low contrast",
    },
    {
        "name": "漫画风格",
        "prompt": "{prompt}, manga style, vibrant, high-energy, detailed, iconic, Japanese comic style",
        "negative_prompt": "nsfw, ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, Western comic style",
    },
    {
        "name": "数字艺术",
        "prompt": "{prompt}, concept art, digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "nsfw, photo, photorealistic, realism, ugly",
    },
    {
        "name": "像素艺术",
        "prompt": "{prompt}, pixel-art, low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "nsfw, sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic",
    },
    {
        "name": "奇幻艺术",
        "prompt": "{prompt}, ethereal fantasy concept art, magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "nsfw, photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
    },
    {
        "name": "霓虹朋克",
        "prompt": "{prompt}, neonpunk style, cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "nsfw, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "3D模型",
        "prompt": "{prompt}, professional 3d model, octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "nsfw, ugly, deformed, noisy, low poly, blurry, painting",
    },
    {
        "name": "菲菲时尚",
        "prompt": "{prompt}, poses,natural, High-quality photography, creative composition, fashion foresight, a strong visual style, and an aura of luxury and sophistication collectively define the distinctive aesthetic of Vogue magazine",
        "negative_prompt": "lowres,",
    },
    {
        "name": "菲菲杂志",
        "prompt": "{prompt}, poses,natural, High-quality photography, creative composition, fashion foresight, a strong visual style, and an aura of luxury and sophistication collectively define the distinctive aesthetic of fashion magazine",
        "negative_prompt": "lowres,",
    },
    {
        "name": "菲菲高清",
        "prompt": "hyper-realistic 8K image of {prompt}. ultra-detailed, lifelike, high-resolution, sharp, vibrant colors, photorealistic",
        "negative_prompt": "cartoonish, low resolution, blurry, simplistic, abstract, deformed, ugly",
    },
    {
        "name": "菲菲黑白",
        "prompt": "black and white collage of {prompt}. monochromatic, timeless, classic, dramatic contrast",
        "negative_prompt": "colorful, vibrant, bright, flashy",
    },
    {
        "name": "菲菲宝丽来",
        "prompt": "collage of polaroid photos featuring {prompt}. vintage style, high contrast, nostalgic, instant film aesthetic",
        "negative_prompt": "digital, modern, low quality, blurry",
    },
    {
        "name": "菲菲水彩",
        "prompt": "watercolor collage of {prompt}. soft edges, translucent colors, painterly effects",
        "negative_prompt": "digital, sharp lines, solid colors",
    },
    {
        "name": "菲菲电影风格",
        "prompt": "cinematic collage of {prompt}. film stills, movie posters, dramatic lighting",
        "negative_prompt": "static, lifeless, mundane",
    },
    {
        "name": "菲菲怀旧",
        "prompt": "nostalgic collage of {prompt}. retro imagery, vintage objects, sentimental journey",
        "negative_prompt": "contemporary, futuristic, forward-looking",
    },
    {
        "name": "菲菲复古",
        "prompt": "vintage collage of {prompt}. aged paper, sepia tones, retro imagery, antique vibes",
        "negative_prompt": "modern, contemporary, futuristic, high-tech",
    },
    {
        "name": "菲菲剪贴簿",
        "prompt": "scrapbook style collage of {prompt}. mixed media, hand-cut elements, textures, paper, stickers, doodles",
        "negative_prompt": "clean, digital, modern, low quality",
    },
    {
        "name": "菲菲霓虹光效",
        "prompt": "neon glow collage of {prompt}. vibrant colors, glowing effects, futuristic vibes",
        "negative_prompt": "dull, muted colors, vintage, retro",
    },
    {
        "name": "菲菲几何",
        "prompt": "geometric collage of {prompt}. abstract shapes, colorful, sharp edges, modern design, high quality",
        "negative_prompt": "blurry, low quality, traditional, dull",
    },
    {
        "name": "菲菲主题",
        "prompt": "thematic collage of {prompt}. cohesive theme, well-organized, matching colors, creative layout",
        "negative_prompt": "random, messy, unorganized, clashing colors",
    },
    {
        "name": "菲菲3840 x 2160",
        "prompt": "hyper-realistic 8K image of {prompt}. ultra-detailed, lifelike, high-resolution, sharp, vibrant colors, photorealistic",
        "negative_prompt": "cartoonish, low resolution, blurry, simplistic, abstract, deformed, ugly",
    },
    {
        "name": "菲菲2560 x 1440",
        "prompt": "hyper-realistic 8k image of {prompt}. ultra-detailed, lifelike, high-resolution, sharp, vibrant colors, photorealistic",
        "negative_prompt": "cartoonish, low resolution, blurry, simplistic, abstract, deformed, ugly",
    },
    {
        "name": "菲菲高清+",
        "prompt": "hyper-realistic 2K image of {prompt}. ultra-detailed, lifelike, high-resolution, sharp, vibrant colors, photorealistic",
        "negative_prompt": "cartoonish, low resolution, blurry, simplistic, abstract, deformed, ugly",
    },
    {
        "name": "Nvidia Rtx 4090",
        "prompt": "{prompt} ,Ray Tracing , DLSS 3 , Reflex,",
        "negative_prompt": "lowres,face asymmetry, eyes asymmetry, deformed eyes, open mouth,",
    },
    {
        "name": "菲菲光影的艺术",
        "prompt": "astonishing gloomy art made mainly of shadows and lighting, forming {prompt}. masterful usage of lighting, shadows and chiaroscuro. truly captivating, Her delicate fingers caress the fabric seductively, stunning figure speaks volumes",
        "negative_prompt": "lowres,face asymmetry, eyes asymmetry, deformed eyes",
    },
    {
        "name": "菲菲动漫电影风格",
        "prompt": "{prompt}, cinematic still, emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "菲菲动漫摄影风格",
        "prompt": "{prompt}, cinematic photo, 35mm photograph, film, bokeh, professional, 8k, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
    },
    {
        "name": "菲菲动漫风格",
        "prompt": "{prompt}, anime artwork, anime style, key visual, vibrant, studio anime, highly detailed",
        "negative_prompt": "photo, deformed, black and white, realism, disfigured, low contrast",
    },
    {
        "name": "菲菲动漫漫画风格",
        "prompt": "{prompt}, manga style, vibrant, high-energy, detailed, iconic, Japanese comic style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, Western comic style",
    },
    {
        "name": "菲菲动漫数字艺术",
        "prompt": "{prompt}, concept art, digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "photo, photorealistic, realism, ugly",
    },
    {
        "name": "菲菲动漫像素艺术",
        "prompt": "{prompt}, pixel-art, low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic",
    },
    {
        "name": "菲菲动漫奇幻艺术",
        "prompt": "{prompt}, ethereal fantasy concept art, magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
    },
    {
        "name": "菲菲动漫霓虹朋克",
        "prompt": "{prompt}, neonpunk style, cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "菲菲动漫3D模型",
        "prompt": "{prompt}, professional 3d model, octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "ugly, deformed, noisy, low poly, blurry, painting",
    },
    {
        "name": "菲菲质量标准v3.0",
        "prompt": "{prompt}, masterpiece, best quality",
        "negative_prompt": "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name",
    },
    {
        "name": "菲菲质量标准v3.1",
        "prompt": "{prompt}, masterpiece, best quality, very aesthetic, absurdres",
        "negative_prompt": "lowres, (bad), text, error, fewer, extra, missing, worst quality, jpeg artifacts, low quality, watermark, unfinished, displeasing, oldest, early, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract]",
    },
    {
        "name": "菲菲质量轻量v3.1",
        "prompt": "{prompt}, (masterpiece), best quality, very aesthetic, perfect face",
        "negative_prompt": "(low quality, worst quality:1.2), very displeasing, 3d, watermark, signature, ugly, poorly drawn",
    },
    {
        "name": "菲菲质量重量v3.1",
        "prompt": "{prompt}, (masterpiece), (best quality), (ultra-detailed), very aesthetic, illustration, disheveled hair, perfect composition, moist skin, intricate details",
        "negative_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, pubic hair, extra digit, fewer digits, cropped, worst quality, low quality, very displeasing",
    },
    {
        "name": "菲菲3D模型",
        "prompt": "professional 3d model {prompt} . octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "ugly, deformed, noisy, low poly, blurry, painting",
    },
    {
        "name": "菲菲模拟胶片",
        "prompt": "analog film photo {prompt} . faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "菲菲动漫",
        "prompt": "anime artwork {prompt} . anime style, key visual, vibrant, studio anime,  highly detailed",
        "negative_prompt": "photo, deformed, black and white, realism, disfigured, low contrast",
    },
    {
        "name": "菲菲电影风格",
        "prompt": "cinematic film still {prompt} . shallow depth of field, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "菲菲漫画书",
        "prompt": "comic {prompt} . graphic illustration, comic art, graphic novel art, vibrant, highly detailed",
        "negative_prompt": "photograph, deformed, glitch, noisy, realistic, stock photo",
    },
    {
        "name": "菲菲手工粘土",
        "prompt": "play-doh style {prompt} . sculpture, clay art, centered composition, Claymation",
        "negative_prompt": "sloppy, messy, grainy, highly detailed, ultra textured, photo",
    },
    {
        "name": "菲菲数字艺术",
        "prompt": "concept art {prompt} . digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "photo, photorealistic, realism, ugly",
    },
    {
        "name": "菲菲增强",
        "prompt": "breathtaking {prompt} . award-winning, professional, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, distorted, grainy",
    },
    {
        "name": "菲菲奇幻艺术",
        "prompt": "ethereal fantasy concept art of  {prompt} . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
    },
    {
        "name": "菲菲等距风格",
        "prompt": "isometric style {prompt} . vibrant, beautiful, crisp, detailed, ultra detailed, intricate",
        "negative_prompt": "deformed, mutated, ugly, disfigured, blur, blurry, noise, noisy, realistic, photographic",
    },
    {
        "name": "菲菲线条艺术",
        "prompt": "line art drawing {prompt} . professional, sleek, modern, minimalist, graphic, line art, vector graphics",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, blurry, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, mutated, realism, realistic, impressionism, expressionism, oil, acrylic",
    },
    {
        "name": "菲菲低多边形",
        "prompt": "low-poly style {prompt} . low-poly game art, polygon mesh, jagged, blocky, wireframe edges, centered composition",
        "negative_prompt": "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo",
    },
    {
        "name": "菲菲霓虹朋克",
        "prompt": "neonpunk style {prompt} . cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "菲菲折纸",
        "prompt": "origami style {prompt} . paper art, pleated paper, folded, origami art, pleats, cut and fold, centered composition",
        "negative_prompt": "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo",
    },
    {
        "name": "菲菲摄影风格",
        "prompt": "cinematic photo {prompt} . 35mm photograph, film, bokeh, professional, 8k, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
    },
    {
        "name": "菲菲像素艺术",
        "prompt": "pixel-art {prompt} . low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic",
    },
    {
        "name": "菲菲纹理",
        "prompt": "texture {prompt} top down close-up",
        "negative_prompt": "ugly, deformed, noisy, blurry",
    },
    {
        "name": "菲菲广告",
        "prompt": "Advertising poster style {prompt} . Professional, modern, product-focused, commercial, eye-catching, highly detailed",
        "negative_prompt": "noisy, blurry, amateurish, sloppy, unattractive",
    },
    {
        "name": "菲菲美食摄影",
        "prompt": "Food photography style {prompt} . Appetizing, professional, culinary, high-resolution, commercial, highly detailed",
        "negative_prompt": "unappetizing, sloppy, unprofessional, noisy, blurry",
    },
    {
        "name": "菲菲房地产",
        "prompt": "Real estate photography style {prompt} . Professional, inviting, well-lit, high-resolution, property-focused, commercial, highly detailed",
        "negative_prompt": "dark, blurry, unappealing, noisy, unprofessional",
    },
    {
        "name": "菲菲抽象",
        "prompt": "Abstract style {prompt} . Non-representational, colors and shapes, expression of feelings, imaginative, highly detailed",
        "negative_prompt": "realistic, photographic, figurative, concrete",
    },
    {
        "name": "菲菲立体主义",
        "prompt": "Cubist artwork {prompt} . Geometric shapes, abstract, innovative, revolutionary",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "菲菲涂鸦",
        "prompt": "Graffiti style {prompt} . Street art, vibrant, urban, detailed, tag, mural",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "菲菲超现实主义",
        "prompt": "Hyperrealistic art {prompt} . Extremely high-resolution details, photographic, realism pushed to extreme, fine texture, incredibly lifelike",
        "negative_prompt": "simplified, abstract, unrealistic, impressionistic, low resolution",
    },
    {
        "name": "菲菲印象派",
        "prompt": "Impressionist painting {prompt} . Loose brushwork, vibrant color, light and shadow play, captures feeling over form",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "菲菲点彩派",
        "prompt": "Pointillism style {prompt} . Composed entirely of small, distinct dots of color, vibrant, highly detailed",
        "negative_prompt": "line drawing, smooth shading, large color fields, simplistic",
    },
    {
        "name": "菲菲波普艺术",
        "prompt": "Pop Art style {prompt} . Bright colors, bold outlines, popular culture themes, ironic or kitsch",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, minimalist",
    },
    {
        "name": "菲菲迷幻艺术",
        "prompt": "Psychedelic style {prompt} . Vibrant colors, swirling patterns, abstract forms, surreal, trippy",
        "negative_prompt": "monochrome, black and white, low contrast, realistic, photorealistic, plain, simple",
    },
    {
        "name": "菲菲文艺复兴",
        "prompt": "Renaissance style {prompt} . Realistic, perspective, light and shadow, religious or mythological themes, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, modernist, minimalist, abstract",
    },
    {
        "name": "菲菲蒸汽朋克",
        "prompt": "Steampunk style {prompt} . Antique, mechanical, brass and copper tones, gears, intricate, detailed",
        "negative_prompt": "deformed, glitch, noisy, low contrast, anime, photorealistic",
    },
    {
        "name": "菲菲超现实主义",
        "prompt": "Surrealist art {prompt} . Dreamlike, mysterious, provocative, symbolic, intricate, detailed",
        "negative_prompt": "anime, photorealistic, realistic, deformed, glitch, noisy, low contrast",
    },
    {
        "name": "菲菲字体设计",
        "prompt": "Typographic art {prompt} . Stylized, intricate, detailed, artistic, text-based",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "菲菲水彩",
        "prompt": "Watercolor painting {prompt} . Vibrant, beautiful, painterly, detailed, textural, artistic",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "菲菲格斗游戏",
        "prompt": "Fighting game style {prompt} . Dynamic, vibrant, action-packed, detailed character design, reminiscent of fighting video games",
        "negative_prompt": "peaceful, calm, minimalist, photorealistic",
    },
    {
        "name": "菲菲GTA",
        "prompt": "GTA-style artwork {prompt} . Satirical, exaggerated, pop art style, vibrant colors, iconic characters, action-packed",
        "negative_prompt": "realistic, black and white, low contrast, impressionist, cubist, noisy, blurry, deformed",
    },
    {
        "name": "菲菲超级马里奥",
        "prompt": "Super Mario style {prompt} . Vibrant, cute, cartoony, fantasy, playful, reminiscent of Super Mario series",
        "negative_prompt": "realistic, modern, horror, dystopian, violent",
    },
    {
        "name": "菲菲我的世界",
        "prompt": "Minecraft style {prompt} . Blocky, pixelated, vibrant colors, recognizable characters and objects, game assets",
        "negative_prompt": "smooth, realistic, detailed, photorealistic, noise, blurry, deformed",
    },
    {
        "name": "菲菲宝可梦",
        "prompt": "Pokémon style {prompt} . Vibrant, cute, anime, fantasy, reminiscent of Pokémon series",
        "negative_prompt": "realistic, modern, horror, dystopian, violent",
    },
    {
        "name": "菲菲复古街机",
        "prompt": "Retro arcade style {prompt} . 8-bit, pixelated, vibrant, classic video game, old school gaming, reminiscent of 80s and 90s arcade games",
        "negative_prompt": "modern, ultra-high resolution, photorealistic, 3D",
    },
    {
        "name": "菲菲复古游戏",
        "prompt": "Retro game art {prompt} . 16-bit, vibrant colors, pixelated, nostalgic, charming, fun",
        "negative_prompt": "realistic, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "菲菲RPG奇幻游戏",
        "prompt": "Role-playing game (RPG) style fantasy {prompt} . Detailed, vibrant, immersive, reminiscent of high fantasy RPG games",
        "negative_prompt": "sci-fi, modern, urban, futuristic, low detailed",
    },
    {
        "name": "菲菲策略游戏",
        "prompt": "Strategy game style {prompt} . Overhead view, detailed map, units, reminiscent of real-time strategy video games",
        "negative_prompt": "first-person view, modern, photorealistic",
    },
    {
        "name": "菲菲街头霸王",
        "prompt": "Street Fighter style {prompt} . Vibrant, dynamic, arcade, 2D fighting game, highly detailed, reminiscent of Street Fighter series",
        "negative_prompt": "3D, realistic, modern, photorealistic, turn-based strategy",
    },
    {
        "name": "菲菲塞尔达传说",
        "prompt": "Legend of Zelda style {prompt} . Vibrant, fantasy, detailed, epic, heroic, reminiscent of The Legend of Zelda series",
        "negative_prompt": "sci-fi, modern, realistic, horror",
    },
    {
        "name": "菲菲建筑",
        "prompt": "Architectural style {prompt} . Clean lines, geometric shapes, minimalist, modern, architectural drawing, highly detailed",
        "negative_prompt": "curved lines, ornate, baroque, abstract, grunge",
    },
    {
        "name": "菲菲迪斯科",
        "prompt": "Disco-themed {prompt} . Vibrant, groovy, retro 70s style, shiny disco balls, neon lights, dance floor, highly detailed",
        "negative_prompt": "minimalist, rustic, monochrome, contemporary, simplistic",
    },
    {
        "name": "菲菲梦境",
        "prompt": "Dreamscape {prompt} . Surreal, ethereal, dreamy, mysterious, fantasy, highly detailed",
        "negative_prompt": "realistic, concrete, ordinary, mundane",
    },
    {
        "name": "菲菲反乌托邦",
        "prompt": "Dystopian style {prompt} . Bleak, post-apocalyptic, somber, dramatic, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, cheerful, optimistic, vibrant, colorful",
    },
    {
        "name": "菲菲童话",
        "prompt": "Fairy tale {prompt} . Magical, fantastical, enchanting, storybook style, highly detailed",
        "negative_prompt": "realistic, modern, ordinary, mundane",
    },
    {
        "name": "菲菲哥特",
        "prompt": "Gothic style {prompt} . Dark, mysterious, haunting, dramatic, ornate, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, cheerful, optimistic",
    },
    {
        "name": "菲菲垃圾摇滚",
        "prompt": "Grunge style {prompt} . Textured, distressed, vintage, edgy, punk rock vibe, dirty, noisy",
        "negative_prompt": "smooth, clean, minimalist, sleek, modern, photorealistic",
    },
    {
        "name": "菲菲恐怖",
        "prompt": "Horror-themed {prompt} . Eerie, unsettling, dark, spooky, suspenseful, grim, highly detailed",
        "negative_prompt": "cheerful, bright, vibrant, light-hearted, cute",
    },
    {
        "name": "菲菲极简主义",
        "prompt": "Minimalist style {prompt} . Simple, clean, uncluttered, modern, elegant",
        "negative_prompt": "ornate, complicated, highly detailed, cluttered, disordered, messy, noisy",
    },
    {
        "name": "菲菲单色",
        "prompt": "Monochrome {prompt} . Black and white, contrast, tone, texture, detailed",
        "negative_prompt": "colorful, vibrant, noisy, blurry, deformed",
    },
    {
        "name": "菲菲航海",
        "prompt": "Nautical-themed {prompt} . Sea, ocean, ships, maritime, beach, marine life, highly detailed",
        "negative_prompt": "landlocked, desert, mountains, urban, rustic",
    },
    {
        "name": "菲菲太空",
        "prompt": "Space-themed {prompt} . Cosmic, celestial, stars, galaxies, nebulas, planets, science fiction, highly detailed",
        "negative_prompt": "earthly, mundane, ground-based, realism",
    },
    {
        "name": "菲菲彩色玻璃",
        "prompt": "Stained glass style {prompt} . Vibrant, beautiful, translucent, intricate, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "菲菲科技时尚",
        "prompt": "Techwear fashion {prompt} . Futuristic, cyberpunk, urban, tactical, sleek, dark, highly detailed",
        "negative_prompt": "vintage, rural, colorful, low contrast, realism, sketch, watercolor",
    },
    {
        "name": "菲菲部落",
        "prompt": "Tribal style {prompt} . Indigenous, ethnic, traditional patterns, bold, natural colors, highly detailed",
        "negative_prompt": "modern, futuristic, minimalist, pastel",
    },
    {
        "name": "菲菲禅绕画",
        "prompt": "Zentangle {prompt} . Intricate, abstract, monochrome, patterns, meditative, highly detailed",
        "negative_prompt": "colorful, representative, simplistic, large fields of color",
    },
    {
        "name": "菲菲拼贴",
        "prompt": "Collage style {prompt} . Mixed media, layered, textural, detailed, artistic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "菲菲平面剪纸",
        "prompt": "Flat papercut style {prompt} . Silhouette, clean cuts, paper, sharp edges, minimalist, color block",
        "negative_prompt": "3D, high detail, noise, grainy, blurry, painting, drawing, photo, disfigured",
    },
    {
        "name": "菲菲剪纸艺术",
        "prompt": "Kirigami representation of {prompt} . 3D, paper folding, paper cutting, Japanese, intricate, symmetrical, precision, clean lines",
        "negative_prompt": "painting, drawing, 2D, noisy, blurry, deformed",
    },
    {
        "name": "菲菲纸浆",
        "prompt": "Paper mache representation of {prompt} . 3D, sculptural, textured, handmade, vibrant, fun",
        "negative_prompt": "2D, flat, photo, sketch, digital art, deformed, noisy, blurry",
    },
    {
        "name": "菲菲纸卷",
        "prompt": "Paper quilling art of {prompt} . Intricate, delicate, curling, rolling, shaping, coiling, loops, 3D, dimensional, ornamental",
        "negative_prompt": "photo, painting, drawing, 2D, flat, deformed, noisy, blurry",
    },
    {
        "name": "菲菲剪纸拼贴",
        "prompt": "Papercut collage of {prompt} . Mixed media, textured paper, overlapping, asymmetrical, abstract, vibrant",
        "negative_prompt": "photo, 3D, realistic, drawing, painting, high detail, disfigured",
    },
    {
        "name": "菲菲剪纸阴影盒",
        "prompt": "3D papercut shadow box of {prompt} . Layered, dimensional, depth, silhouette, shadow, papercut, handmade, high contrast",
        "negative_prompt": "painting, drawing, photo, 2D, flat, high detail, blurry, noisy, disfigured",
    },
    {
        "name": "菲菲堆叠剪纸",
        "prompt": "Stacked papercut art of {prompt} . 3D, layered, dimensional, depth, precision cut, stacked layers, papercut, high contrast",
        "negative_prompt": "2D, flat, noisy, blurry, painting, drawing, photo, deformed",
    },
    {
        "name": "菲菲厚层剪纸",
        "prompt": "Thick layered papercut art of {prompt} . Deep 3D, volumetric, dimensional, depth, thick paper, high stack, heavy texture, tangible layers",
        "negative_prompt": "2D, flat, thin paper, low stack, smooth texture, painting, drawing, photo, deformed",
    },
    {
        "name": "菲菲外星人",
        "prompt": "Alien-themed {prompt} . Extraterrestrial, cosmic, otherworldly, mysterious, sci-fi, highly detailed",
        "negative_prompt": "earthly, mundane, common, realistic, simple",
    },
    {
        "name": "菲菲黑色电影",
        "prompt": "Film noir style {prompt} . Monochrome, high contrast, dramatic shadows, 1940s style, mysterious, cinematic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, vibrant, colorful",
    },
    {
        "name": "菲菲HDR",
        "prompt": "HDR photo of {prompt} . High dynamic range, vivid, rich details, clear shadows and highlights, realistic, intense, enhanced contrast, highly detailed",
        "negative_prompt": "flat, low contrast, oversaturated, underexposed, overexposed, blurred, noisy",
    },
    {
        "name": "菲菲长时间曝光",
        "prompt": "Long exposure photo of {prompt} . Blurred motion, streaks of light, surreal, dreamy, ghosting effect, highly detailed",
        "negative_prompt": "static, noisy, deformed, shaky, abrupt, flat, low contrast",
    },
    {
        "name": "菲菲霓虹黑色",
        "prompt": "Neon noir {prompt} . Cyberpunk, dark, rainy streets, neon signs, high contrast, low light, vibrant, highly detailed",
        "negative_prompt": "bright, sunny, daytime, low contrast, black and white, sketch, watercolor",
    },
    {
        "name": "菲菲剪影",
        "prompt": "Silhouette style {prompt} . High contrast, minimalistic, black and white, stark, dramatic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, color, realism, photorealistic",
    },
    {
        "name": "菲菲倾斜移位",
        "prompt": "Tilt-shift photo of {prompt} . Selective focus, miniature effect, blurred background, highly detailed, vibrant, perspective control",
        "negative_prompt": "blurry, noisy, deformed, flat, low contrast, unrealistic, oversaturated, underexposed",
    },
    {
        "name": "mre-电影动态",
        "prompt": "epic cinematic shot of dynamic {prompt} in motion. main subject of high budget action movie. raw photo, motion blur. best quality, high resolution",
        "negative_prompt": "static, still, motionless, sluggish. drawing, painting, illustration, rendered. low budget. low quality, low resolution",
    },
    {
        "name": "mre-自发图片",
        "prompt": "spontaneous picture of {prompt}, taken by talented amateur. best quality, high resolution. magical moment, natural look. simple but good looking",
        "negative_prompt": "overthinked. low quality, low resolution",
    },
    {
        "name": "mre-艺术视野",
        "prompt": "powerful artistic vision of {prompt}. breathtaking masterpiece made by great artist. best quality, high resolution",
        "negative_prompt": "insignificant, flawed, made by bad artist. low quality, low resolution",
    },
    {
        "name": "mre-黑暗梦境",
        "prompt": "dark and unsettling dream showing {prompt}. best quality, high resolution. created by genius but depressed mad artist. grim beauty",
        "negative_prompt": "naive, cheerful. comfortable, casual, boring, cliche. low quality, low resolution",
    },
    {
        "name": "mre-阴郁艺术",
        "prompt": "astonishing gloomy art made mainly of shadows and lighting, forming {prompt}. masterful usage of lighting, shadows and chiaroscuro. made by black-hearted artist, drawing from darkness. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-噩梦",
        "prompt": "picture from really bad dream about terrifying {prompt}, true horror. bone-chilling vision. mad world that shouldn't exist. best quality, high resolution",
        "negative_prompt": "nice dream, pleasant experience. low quality, low resolution",
    },
    {
        "name": "mre-地下",
        "prompt": "uncanny caliginous vision of {prompt}, created by remarkable underground artist. best quality, high resolution. raw and brutal art, careless but impressive style. inspired by darkness and chaos",
        "negative_prompt": "photography, mainstream, civilized. low quality, low resolution",
    },
    {
        "name": "mre-超现实主义绘画",
        "prompt": "surreal painting representing strange vision of {prompt}. harmonious madness, synergy with chance. unique artstyle, mindbending art, magical surrealism. best quality, high resolution",
        "negative_prompt": "photography, illustration, drawing. realistic, possible. logical, sane. low quality, low resolution",
    },
    {
        "name": "mre-动态插画",
        "prompt": "insanely dynamic illustration of {prompt}. best quality, high resolution. crazy artstyle, careless brushstrokes, emotional and fun",
        "negative_prompt": "photography, realistic. static, still, slow, boring. low quality, low resolution",
    },
    {
        "name": "mre-亡灵艺术",
        "prompt": "long forgotten art created by undead artist illustrating {prompt}, tribute to the death and decay. miserable art of the damned. wretched and decaying world. best quality, high resolution",
        "negative_prompt": "alive, playful, living. low quality, low resolution",
    },
    {
        "name": "mre-元素艺术",
        "prompt": "art illustrating insane amounts of raging elemental energy turning into {prompt}, avatar of elements. magical surrealism, wizardry. best quality, high resolution",
        "negative_prompt": "photography, realistic, real. low quality, low resolution",
    },
    {
        "name": "mre-太空艺术",
        "prompt": "winner of inter-galactic art contest illustrating {prompt}, symbol of the interstellar singularity. best quality, high resolution. artstyle previously unseen in the whole galaxy",
        "negative_prompt": "created by human race, low quality, low resolution",
    },
    {
        "name": "mre-古代插画",
        "prompt": "sublime ancient illustration of {prompt}, predating human civilization. crude and simple, but also surprisingly beautiful artwork, made by genius primeval artist. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-勇敢艺术",
        "prompt": "brave, shocking, and brutally true art showing {prompt}. inspired by courage and unlimited creativity. truth found in chaos. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-英雄奇幻",
        "prompt": "heroic fantasy painting of {prompt}, in the dangerous fantasy world. airbrush over oil on canvas. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-黑暗赛博朋克",
        "prompt": "dark cyberpunk illustration of brutal {prompt} in a world without hope, ruled by ruthless criminal corporations. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-抒情几何",
        "prompt": "geometric and lyrical abstraction painting presenting {prompt}. oil on metal. best quality, high resolution",
        "negative_prompt": "photography, realistic, drawing, rendered. low quality, low resolution",
    },
    {
        "name": "mre-水墨象征",
        "prompt": "big long brushstrokes of deep black sumi-e turning into symbolic painting of {prompt}. master level raw art. best quality, high resolution",
        "negative_prompt": "photography, rendered. low quality, low resolution",
    },
    {
        "name": "mre-水墨细节",
        "prompt": "highly detailed black sumi-e painting of {prompt}. in-depth study of perfection, created by a master. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-漫画",
        "prompt": "manga artwork presenting {prompt}. created by japanese manga artist. highly emotional. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-动漫",
        "prompt": "anime artwork illustrating {prompt}. created by japanese anime studio. highly emotional. best quality, high resolution",
        "negative_prompt": "low quality, low resolution",
    },
    {
        "name": "mre-漫画",
        "prompt": "breathtaking illustration from adult comic book presenting {prompt}. fabulous artwork. best quality, high resolution",
        "negative_prompt": "deformed, ugly, low quality, low resolution",
    },
    {
        "name": "MK彩色石版画",
        "prompt": "Chromolithograph {prompt}. Vibrant colors, intricate details, rich color saturation, meticulous registration, multi-layered printing, decorative elements, historical charm, artistic reproductions, commercial posters, nostalgic, ornate compositions.",
        "negative_prompt": "monochromatic, simple designs, limited color palette, imprecise registration, minimalistic, modern aesthetic, digital appearance.",
    },
    {
        "name": "MK交叉处理印刷",
        "prompt": "Cross processing print {prompt}. Experimental color shifts, unconventional tonalities, vibrant and surreal hues, heightened contrasts, unpredictable results, artistic unpredictability, retro and vintage feel, dynamic color interplay, abstract and dreamlike.",
        "negative_prompt": "predictable color tones, traditional processing, realistic color representation, subdued contrasts, standard photographic aesthetics.",
    },
    {
        "name": "MK杜菲彩色照片",
        "prompt": "Dufaycolor photograph {prompt}. Vintage color palette, distinctive color rendering, soft and dreamy atmosphere, historical charm, unique color process, grainy texture, evocative mood, nostalgic aesthetic, hand-tinted appearance, artistic patina.",
        "negative_prompt": "modern color reproduction, hyperrealistic tones, sharp and clear details, digital precision, contemporary aesthetic.",
    },
    {
        "name": "MK植物标本",
        "prompt": "Herbarium drawing{prompt}. Botanical accuracy, old botanical book illustration, detailed illustrations, pressed plants, delicate and precise linework, scientific documentation, meticulous presentation, educational purpose, organic compositions, timeless aesthetic, naturalistic beauty.",
        "negative_prompt": "abstract representation, vibrant colors, artistic interpretation, chaotic compositions, fantastical elements, digital appearance.",
    },
    {
        "name": "MK朋克拼贴",
        "prompt": "punk collage style {prompt} . mixed media, papercut,textured paper, overlapping, ripped posters, safety pins, chaotic layers, graffiti-style elements, anarchy symbols, vintage photos, cut-and-paste aesthetic, bold typography, distorted images, political messages, urban decay, distressed textures, newspaper clippings, spray paint, rebellious icons, DIY spirit, vivid colors, punk band logos, edgy and raw compositions, ",
        "negative_prompt": "conventional,blurry, noisy, low contrast",
    },
    {
        "name": "MK马赛克",
        "prompt": "mosaic style {prompt} . fragmented, assembled, colorful, highly detailed",
        "negative_prompt": "whole, unbroken, monochrome",
    },
    {
        "name": "MK梵高",
        "prompt": "Oil painting by Van Gogh {prompt} . Expressive, impasto, swirling brushwork, vibrant, brush strokes, Brushstroke-heavy, Textured, Impasto, Colorful, Dynamic, Bold, Distinctive, Vibrant, Whirling, Expressive, Dramatic, Swirling, Layered, Intense, Contrastive, Atmospheric, Luminous, Textural, Evocative, SpiraledVan Gogh style",
        "negative_prompt": "realistic, photorealistic, calm, straight lines, signature, frame, text, watermark",
    },
    {
        "name": "MK涂色书",
        "prompt": "centered black and white high contrast line drawing, coloring book style,{prompt} . monochrome, blank white background",
        "negative_prompt": "greyscale, gradients,shadows,shadow, colored, Red, Blue, Yellow, Green, Orange, Purple, Pink, Brown, Gray, Beige, Turquoise, Lavender, Cyan, Magenta, Olive, Indigo, black background",
    },
    {
        "name": "MK辛格·萨金特",
        "prompt": "Oil painting by John Singer Sargent {prompt}. Elegant, refined, masterful technique,realistic portrayal, subtle play of light, captivating expression, rich details, harmonious colors, skillful composition, brush strokes, chiaroscuro.",
        "negative_prompt": "realistic, photorealistic, abstract, overly stylized, excessive contrasts, distorted,bright colors,disorder.",
    },
    {
        "name": "MK波洛克",
        "prompt": "Oil painting by Jackson Pollock {prompt}. Abstract expressionism, drip painting, chaotic composition, energetic, spontaneous, unconventional technique, dynamic, bold, distinctive, vibrant, intense, expressive, energetic, layered, non-representational, gestural.",
        "negative_prompt": "(realistic:1.5), (photorealistic:1.5), representational, calm, ordered composition, precise lines, detailed forms, subdued colors, quiet, static, traditional, figurative.",
    },
    {
        "name": "MK巴斯奎特",
        "prompt": "Artwork by Jean-Michel Basquiat {prompt}. Neo-expressionism, street art influence, graffiti-inspired, raw, energetic, bold colors, dynamic composition, chaotic, layered, textural, expressive, spontaneous, distinctive, symbolic,energetic brushstrokes.",
        "negative_prompt": "(realistic:1.5), (photorealistic:1.5), calm, precise lines, conventional composition, subdued",
    },
    {
        "name": "MK安迪·沃霍尔",
        "prompt": "Artwork in the style of Andy Warhol {prompt}. Pop art, vibrant colors, bold compositions, repetition of iconic imagery, celebrity culture, commercial aesthetics, mass production influence, stylized simplicity, cultural commentary, graphical elements, distinctive portraits.",
        "negative_prompt": "subdued colors, realistic, lack of repetition, minimalistic.",
    },
    {
        "name": "MK半色调印刷",
        "prompt": "Halftone print of {prompt}. Dot matrix pattern, grayscale tones, vintage aesthetic, newspaper print vibe, stylized dots, visual texture, black and white contrasts, retro appearance, artistic pointillism,pop culture, (Roy Lichtenstein style:1.5).",
        "negative_prompt": "smooth gradients, continuous tones, vibrant colors.",
    },
    {
        "name": "MK冈德绘画",
        "prompt": "Gond painting {prompt}. Intricate patterns, vibrant colors, detailed motifs, nature-inspired themes, tribal folklore, fine lines, intricate detailing, storytelling compositions, mystical and folkloric, cultural richness.",
        "negative_prompt": "monochromatic, abstract shapes, minimalistic.",
    },
    {
        "name": "MK蛋白印刷",
        "prompt": "Albumen print {prompt}. Sepia tones, fine details, subtle tonal gradations, delicate highlights, vintage aesthetic, soft and muted atmosphere, historical charm, rich textures, meticulous craftsmanship, classic photographic technique, vignetting.",
        "negative_prompt": "vibrant colors, high contrast, modern, digital appearance, sharp details, contemporary style.",
    },
    {
        "name": "MK蚀刻印刷",
        "prompt": "Aquatint print {prompt}. Soft tonal gradations, atmospheric effects, velvety textures, rich contrasts, fine details, etching process, delicate lines, nuanced shading, expressive and moody atmosphere, artistic depth.",
        "negative_prompt": "sharp contrasts, bold lines, minimalistic.",
    },
    {
        "name": "MK植物印刷",
        "prompt": "Anthotype print {prompt}. Monochrome dye, soft and muted colors, organic textures, ephemeral and delicate appearance, low details, watercolor canvas, low contrast, overexposed, silhouette, textured paper.",
        "negative_prompt": "vibrant synthetic dyes, bold and saturated colors.",
    },
    {
        "name": "MK因纽特雕刻",
        "prompt": "A sculpture made of ivory, {prompt} made of . Sculptures, Inuit art style, intricate carvings, natural materials, storytelling motifs, arctic wildlife themes, symbolic representations, cultural traditions, earthy tones, harmonious compositions, spiritual and mythological elements.",
        "negative_prompt": "abstract, vibrant colors.",
    },
    {
        "name": "MK溴油印刷",
        "prompt": "Bromoil print {prompt}. Painterly effects, sepia tones, textured surfaces, rich contrasts, expressive brushwork, tonal variations, vintage aesthetic, atmospheric mood, handmade quality, artistic experimentation, darkroom craftsmanship, vignetting.",
        "negative_prompt": "smooth surfaces, minimal brushwork, contemporary digital appearance.",
    },
    {
        "name": "MK卡罗印刷",
        "prompt": "Calotype print {prompt}. Soft focus, subtle tonal range, paper negative process, fine details, vintage aesthetic, artistic experimentation, atmospheric mood, early photographic charm, handmade quality, vignetting.",
        "negative_prompt": "sharp focus, bold contrasts, modern aesthetic, digital photography.",
    },
    {
        "name": "MK彩色速写",
        "prompt": "Color sketchnote {prompt}. Hand-drawn elements, vibrant colors, visual hierarchy, playful illustrations, varied typography, graphic icons, organic and dynamic layout, personalized touches, creative expression, engaging storytelling.",
        "negative_prompt": "monochromatic, geometric layout.",
    },
    {
        "name": "MK西布拉克瓷器",
        "prompt": "A sculpture made of blue pattern porcelain of {prompt}. Classic design, blue and white color scheme, intricate detailing, floral motifs, onion-shaped elements, historical charm, rococo, white ware, cobalt blue, underglaze pattern, fine craftsmanship, traditional elegance, delicate patterns, vintage aesthetic, Meissen, Blue Onion pattern, Cibulak.",
        "negative_prompt": "tea, teapot, cup, teacup,bright colors, bold and modern design, absence of intricate detailing, lack of floral motifs, non-traditional shapes.",
    },
    {
        "name": "MK酒精墨水艺术",
        "prompt": "Alcohol ink art {prompt}. Fluid and vibrant colors, unpredictable patterns, organic textures, translucent layers, abstract compositions, ethereal and dreamy effects, free-flowing movement, expressive brushstrokes, contemporary aesthetic, wet textured paper.",
        "negative_prompt": "monochromatic, controlled patterns.",
    },
    {
        "name": "MK一线艺术",
        "prompt": "One line art {prompt}. Continuous and unbroken black line, minimalistic, simplicity, economical use of space, flowing and dynamic, symbolic representations, contemporary aesthetic, evocative and abstract, white background.",
        "negative_prompt": "disjointed lines, complexity, complex detailing.",
    },
    {
        "name": "MK黑光绘画",
        "prompt": "Blacklight paint {prompt}. Fluorescent pigments, vibrant and surreal colors, ethereal glow, otherworldly effects, dynamic and psychedelic compositions, neon aesthetics, transformative in ultraviolet light, contemporary and experimental.",
        "negative_prompt": "muted colors, traditional and realistic compositions.",
    },
    {
        "name": "MK嘉年华玻璃",
        "prompt": "A sculpture made of Carnival glass, {prompt}. Iridescent surfaces, vibrant colors, intricate patterns, opalescent hues, reflective and prismatic effects, Art Nouveau and Art Deco influences, vintage charm, intricate detailing, lustrous and luminous appearance, Carnival Glass style.",
        "negative_prompt": "non-iridescent surfaces, muted colors, absence of intricate patterns, lack of opalescent hues, modern and minimalist aesthetic.",
    },
    {
        "name": "MK蓝晒印刷",
        "prompt": "Cyanotype print {prompt}. Prussian blue tones, distinctive coloration, high contrast, blueprint aesthetics, atmospheric mood, sun-exposed paper, silhouette effects, delicate details, historical charm, handmade and experimental quality.",
        "negative_prompt": "vibrant colors, low contrast, modern and polished appearance.",
    },
    {
        "name": "MK十字绣",
        "prompt": "Cross-stitching {prompt}. Intricate patterns, embroidery thread, sewing, fine details, precise stitches, textile artistry, symmetrical designs, varied color palette, traditional and contemporary motifs, handmade and crafted,canvas, nostalgic charm.",
        "negative_prompt": "paper, paint, ink, photography.",
    },
    {
        "name": "MK蜡画",
        "prompt": "Encaustic paint {prompt}. Textured surfaces, translucent layers, luminous quality, wax medium, rich color saturation, fluid and organic shapes, contemporary and historical influences, mixed media elements, atmospheric depth.",
        "negative_prompt": "flat surfaces, opaque layers, lack of wax medium, muted color palette, absence of textured surfaces, non-mixed media.",
    },
    {
        "name": "MK刺绣",
        "prompt": "Embroidery {prompt}. Intricate stitching, embroidery thread, fine details, varied thread textures, textile artistry, embellished surfaces, diverse color palette, traditional and contemporary motifs, handmade and crafted, tactile and ornate.",
        "negative_prompt": "minimalist, monochromatic.",
    },
    {
        "name": "MK鱼拓",
        "prompt": "Gyotaku {prompt}. Fish impressions, realistic details, ink rubbings, textured surfaces, traditional Japanese art form, nature-inspired compositions, artistic representation of marine life, black and white contrasts, cultural significance.",
        "negative_prompt": "photography.",
    },
    {
        "name": "MK光绘",
        "prompt": "Luminogram {prompt}. Photogram technique, ethereal and abstract effects, light and shadow interplay, luminous quality, experimental process, direct light exposure, unique and unpredictable results, artistic experimentation.",
        "negative_prompt": "",
    },
    {
        "name": "MK光点艺术",
        "prompt": "Lite Brite art {prompt}. Luminous and colorful designs, pixelated compositions, retro aesthetic, glowing effects, creative patterns, interactive and playful, nostalgic charm, vibrant and dynamic arrangements.",
        "negative_prompt": "monochromatic.",
    },
    {
        "name": "MK木目金",
        "prompt": "Mokume-gane {prompt}. Wood-grain patterns, mixed metal layers, intricate and organic designs, traditional Japanese metalwork, harmonious color combinations, artisanal craftsmanship, unique and layered textures, cultural and historical significance.",
        "negative_prompt": "uniform metal surfaces.",
    },
    {
        "name": "卵石艺术",
        "prompt": "a sculpture made of peebles, {prompt}. Pebble art style,natural materials, textured surfaces, balanced compositions, organic forms, harmonious arrangements, tactile and 3D effects, beach-inspired aesthetic, creative storytelling, artisanal craftsmanship.",
        "negative_prompt": "non-natural materials, lack of textured surfaces, imbalanced compositions, absence of organic forms, non-tactile appearance.",
    },
    {
        "name": "MK帕列赫",
        "prompt": "Palekh art {prompt}. Miniature paintings, intricate details, vivid colors, folkloric themes, lacquer finish, storytelling compositions, symbolic elements, Russian folklore influence, cultural and historical significance.",
        "negative_prompt": "large-scale paintings.",
    },
    {
        "name": "MK墨流",
        "prompt": "Suminagashi {prompt}. Floating ink patterns, marbled effects, delicate and ethereal designs, water-based ink, fluid and unpredictable compositions, meditative process, monochromatic or subtle color palette, Japanese artistic tradition.",
        "negative_prompt": "vibrant and bold color palette.",
    },
    {
        "name": "MK骨雕",
        "prompt": "A Scrimshaw engraving of {prompt}. Intricate engravings on a spermwhale's teeth, marine motifs, detailed scenes, nautical themes, black and white contrasts, historical craftsmanship, artisanal carving, storytelling compositions, maritime heritage.",
        "negative_prompt": "colorful, modern.",
    },
    {
        "name": "MK绞染",
        "prompt": "Shibori {prompt}. Textured fabric, intricate patterns, resist-dyeing technique, indigo or vibrant colors, organic and flowing designs, Japanese textile art, cultural tradition, tactile and visual interest.",
        "negative_prompt": "monochromatic.",
    },
    {
        "name": "MK珐琅",
        "prompt": "A sculpture made of Vitreous enamel {prompt}. Smooth and glossy surfaces, vibrant colors, glass-like finish, durable and resilient, intricate detailing, traditional and contemporary applications, artistic craftsmanship, jewelry and decorative objects, , Vitreous enamel, colored glass.",
        "negative_prompt": "rough surfaces, muted colors.",
    },
    {
        "name": "MK浮世绘",
        "prompt": "Ukiyo-e {prompt}. Woodblock prints, vibrant colors, intricate details, depictions of landscapes, kabuki actors, beautiful women, cultural scenes, traditional Japanese art, artistic craftsmanship, historical significance.",
        "negative_prompt": "absence of woodblock prints, muted colors, lack of intricate details, non-traditional Japanese themes, absence of cultural scenes.",
    },
    {
        "name": "MK复古航空海报",
        "prompt": "vintage airline poster {prompt} . classic aviation fonts, pastel colors, elegant aircraft illustrations, scenic destinations, distressed textures, retro travel allure",
        "negative_prompt": "modern fonts, bold colors, hyper-realistic, sleek design",
    },
    {
        "name": "MK复古旅行海报",
        "prompt": "vintage travel poster {prompt} . retro fonts, muted colors, scenic illustrations, iconic landmarks, distressed textures, nostalgic vibes",
        "negative_prompt": "modern fonts, vibrant colors, hyper-realistic, sleek design",
    },
    {
        "name": "MK包豪斯风格",
        "prompt": "Bauhaus-inspired {prompt} . minimalism, geometric precision, primary colors, sans-serif typography, asymmetry, functional design",
        "negative_prompt": "ornate, intricate, excessive detail, complex patterns, serif typography",
    },
    {
        "name": "MK非洲未来主义",
        "prompt": "Afrofuturism illustration {prompt} . vibrant colors, futuristic elements, cultural symbolism, cosmic imagery, dynamic patterns, empowering narratives",
        "negative_prompt": "monochromatic",
    },
    {
        "name": "MK原子朋克",
        "prompt": "Atompunk illustation, {prompt} . retro-futuristic, atomic age aesthetics, sleek lines, metallic textures, futuristic technology, optimism, energy",
        "negative_prompt": "organic, natural textures, rustic, dystopian",
    },
    {
        "name": "MK构成主义",
        "prompt": "Constructivism {prompt} . geometric abstraction, bold colors, industrial aesthetics, dynamic compositions, utilitarian design, revolutionary spirit",
        "negative_prompt": "organic shapes, muted colors, ornate elements, traditional",
    },
    {
        "name": "MK奇卡诺艺术",
        "prompt": "Chicano art {prompt} . bold colors, cultural symbolism, muralism, lowrider aesthetics, barrio life, political messages, social activism, Mexico",
        "negative_prompt": "monochromatic, minimalist, mainstream aesthetics",
    },
    {
        "name": "MK风格派",
        "prompt": "De Stijl Art {prompt} . neoplasticism, primary colors, geometric abstraction, horizontal and vertical lines, simplicity, harmony, utopian ideals",
        "negative_prompt": "complex patterns, muted colors, ornate elements, asymmetry",
    },
    {
        "name": "MK达雅艺术",
        "prompt": "Dayak art sculpture of {prompt} . intricate patterns, nature-inspired motifs, vibrant colors, traditional craftsmanship, cultural symbolism, storytelling",
        "negative_prompt": "minimalist, monochromatic, modern",
    },
    {
        "name": "MK法尤姆肖像",
        "prompt": "Fayum portrait {prompt} . encaustic painting, realistic facial features, warm earth tones, serene expressions, ancient Egyptian influences",
        "negative_prompt": "abstract, vibrant colors, exaggerated features, modern",
    },
    {
        "name": "MK彩绘手稿",
        "prompt": "Illuminated manuscript {prompt} . intricate calligraphy, rich colors, detailed illustrations, gold leaf accents, ornate borders, religious, historical, medieval",
        "negative_prompt": "modern typography, minimalist design, monochromatic, abstract themes",
    },
    {
        "name": "MK卡利卡特绘画",
        "prompt": "Kalighat painting {prompt} . bold lines, vibrant colors, narrative storytelling, cultural motifs, flat compositions, expressive characters",
        "negative_prompt": "subdued colors, intricate details, realistic portrayal, modern aesthetics",
    },
    {
        "name": "MK马杜巴尼绘画",
        "prompt": "Madhubani painting {prompt} . intricate patterns, vibrant colors, nature-inspired motifs, cultural storytelling, symmetry, folk art aesthetics",
        "negative_prompt": "abstract, muted colors, minimalistic design, modern aesthetics",
    },
    {
        "name": "MK画意摄影",
        "prompt": "Pictorialism illustration{prompt} . soft focus, atmospheric effects, artistic interpretation, tonality, muted colors, evocative storytelling",
        "negative_prompt": "sharp focus, high contrast, realistic depiction, vivid colors",
    },
    {
        "name": "MK皮奇瓦伊绘画",
        "prompt": "Pichwai painting {prompt} . intricate detailing, vibrant colors, religious themes, nature motifs, devotional storytelling, gold leaf accents",
        "negative_prompt": "minimalist, subdued colors, abstract design",
    },
    {
        "name": "MK帕塔奇特拉绘画",
        "prompt": "Patachitra painting {prompt} . bold outlines, vibrant colors, intricate detailing, mythological themes, storytelling, traditional craftsmanship",
        "negative_prompt": "subdued colors, minimalistic, abstract, modern aesthetics",
    },
    {
        "name": "MK萨摩亚艺术灵感",
        "prompt": "Samoan art-inspired wooden sculpture {prompt} . traditional motifs, natural elements, bold colors, cultural symbolism, storytelling, craftsmanship",
        "negative_prompt": "modern aesthetics, minimalist, abstract",
    },
    {
        "name": "MK特林吉特艺术",
        "prompt": "Tlingit art {prompt} . formline design, natural elements, animal motifs, bold colors, cultural storytelling, traditional craftsmanship, Alaska traditional art, (totem:1.5)",
        "negative_prompt": "",
    },
    {
        "name": "MK阿德纳特风格",
        "prompt": "Painting by Adnate {prompt} . realistic portraits, street art, large-scale murals, subdued color palette, social narratives",
        "negative_prompt": "abstract, vibrant colors, small-scale art",
    },
    {
        "name": "MK罗恩·英格利希风格",
        "prompt": "Painting by Ron English {prompt} . pop-surrealism, cultural subversion, iconic mash-ups, vibrant and bold colors, satirical commentary",
        "negative_prompt": "traditional, monochromatic",
    },
    {
        "name": "MK谢泼德·费尔雷风格",
        "prompt": "Painting by Shepard Fairey {prompt} . street art, political activism, iconic stencils, bold typography, high contrast, red, black, and white color palette",
        "negative_prompt": "traditional, muted colors",
    },
    {
        "name": "sai-3D模型",
        "prompt": "professional 3d model {prompt} . octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "ugly, deformed, noisy, low poly, blurry, painting",
    },
    {
        "name": "sai-模拟胶片",
        "prompt": "analog film photo {prompt} . faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "sai-动漫",
        "prompt": "anime artwork {prompt} . anime style, key visual, vibrant, studio anime, highly detailed",
        "negative_prompt": "photo, deformed, black and white, realism, disfigured, low contrast",
    },
    {
        "name": "sai-电影风格",
        "prompt": "cinematic film still {prompt} . shallow depth of field, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "sai-漫画书",
        "prompt": "comic {prompt} . graphic illustration, comic art, graphic novel art, vibrant, highly detailed",
        "negative_prompt": "photograph, deformed, glitch, noisy, realistic, stock photo",
    },
    {
        "name": "sai-手工粘土",
        "prompt": "play-doh style {prompt} . sculpture, clay art, centered composition, Claymation",
        "negative_prompt": "sloppy, messy, grainy, highly detailed, ultra textured, photo",
    },
    {
        "name": "sai-数字艺术",
        "prompt": "concept art {prompt} . digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "photo, photorealistic, realism, ugly",
    },
    {
        "name": "sai-增强",
        "prompt": "breathtaking {prompt} . award-winning, professional, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, distorted, grainy",
    },
    {
        "name": "sai-奇幻艺术",
        "prompt": "ethereal fantasy concept art of  {prompt} . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
    },
    {
        "name": "sai-等距",
        "prompt": "isometric style {prompt} . vibrant, beautiful, crisp, detailed, ultra detailed, intricate",
        "negative_prompt": "deformed, mutated, ugly, disfigured, blur, blurry, noise, noisy, realistic, photographic",
    },
    {
        "name": "sai-线条艺术",
        "prompt": "line art drawing {prompt} . professional, sleek, modern, minimalist, graphic, line art, vector graphics",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, blurry, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, mutated, realism, realistic, impressionism, expressionism, oil, acrylic",
    },
    {
        "name": "sai-低多边形",
        "prompt": "low-poly style {prompt} . low-poly game art, polygon mesh, jagged, blocky, wireframe edges, centered composition",
        "negative_prompt": "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo",
    },
    {
        "name": "sai-霓虹朋克",
        "prompt": "neonpunk style {prompt} . cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "sai-折纸",
        "prompt": "origami style {prompt} . paper art, pleated paper, folded, origami art, pleats, cut and fold, centered composition",
        "negative_prompt": "noisy, sloppy, messy, grainy, highly detailed, ultra textured, photo",
    },
    {
        "name": "sai-摄影风格",
        "prompt": "cinematic photo {prompt} . 35mm photograph, film, bokeh, professional, 8k, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
    },
    {
        "name": "sai-像素艺术",
        "prompt": "pixel-art {prompt} . low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic",
    },
    {
        "name": "sai-纹理",
        "prompt": "texture {prompt} top down close-up",
        "negative_prompt": "ugly, deformed, noisy, blurry",
    },
    {
        "name": "ads-广告",
        "prompt": "advertising poster style {prompt} . Professional, modern, product-focused, commercial, eye-catching, highly detailed",
        "negative_prompt": "noisy, blurry, amateurish, sloppy, unattractive",
    },
    {
        "name": "ads-汽车",
        "prompt": "automotive advertisement style {prompt} . sleek, dynamic, professional, commercial, vehicle-focused, high-resolution, highly detailed",
        "negative_prompt": "noisy, blurry, unattractive, sloppy, unprofessional",
    },
    {
        "name": "ads-企业",
        "prompt": "corporate branding style {prompt} . professional, clean, modern, sleek, minimalist, business-oriented, highly detailed",
        "negative_prompt": "noisy, blurry, grungy, sloppy, cluttered, disorganized",
    },
    {
        "name": "ads-时尚编辑",
        "prompt": "fashion editorial style {prompt} . high fashion, trendy, stylish, editorial, magazine style, professional, highly detailed",
        "negative_prompt": "outdated, blurry, noisy, unattractive, sloppy",
    },
    {
        "name": "ads-美食摄影",
        "prompt": "food photography style {prompt} . appetizing, professional, culinary, high-resolution, commercial, highly detailed",
        "negative_prompt": "unappetizing, sloppy, unprofessional, noisy, blurry",
    },
    {
        "name": "ads-美食摄影",
        "prompt": "gourmet food photo of {prompt} . soft natural lighting, macro details, vibrant colors, fresh ingredients, glistening textures, bokeh background, styled plating, wooden tabletop, garnished, tantalizing, editorial quality",
        "negative_prompt": "cartoon, anime, sketch, grayscale, dull, overexposed, cluttered, messy plate, deformed",
    },
    {
        "name": "ads-奢侈品",
        "prompt": "luxury product style {prompt} . elegant, sophisticated, high-end, luxurious, professional, highly detailed",
        "negative_prompt": "cheap, noisy, blurry, unattractive, amateurish",
    },
    {
        "name": "ads-房地产",
        "prompt": "real estate photography style {prompt} . professional, inviting, well-lit, high-resolution, property-focused, commercial, highly detailed",
        "negative_prompt": "dark, blurry, unappealing, noisy, unprofessional",
    },
    {
        "name": "ads-零售",
        "prompt": "retail packaging style {prompt} . vibrant, enticing, commercial, product-focused, eye-catching, professional, highly detailed",
        "negative_prompt": "noisy, blurry, amateurish, sloppy, unattractive",
    },
    {
        "name": "artstyle-抽象",
        "prompt": "abstract style {prompt} . non-representational, colors and shapes, expression of feelings, imaginative, highly detailed",
        "negative_prompt": "realistic, photographic, figurative, concrete",
    },
    {
        "name": "artstyle-抽象表现主义",
        "prompt": "abstract expressionist painting {prompt} . energetic brushwork, bold colors, abstract forms, expressive, emotional",
        "negative_prompt": "realistic, photorealistic, low contrast, plain, simple, monochrome",
    },
    {
        "name": "artstyle-装饰艺术",
        "prompt": "art deco style {prompt} . geometric shapes, bold colors, luxurious, elegant, decorative, symmetrical, ornate, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, modernist, minimalist",
    },
    {
        "name": "artstyle-新艺术",
        "prompt": "art nouveau style {prompt} . elegant, decorative, curvilinear forms, nature-inspired, ornate, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, modernist, minimalist",
    },
    {
        "name": "artstyle-构成主义",
        "prompt": "constructivist style {prompt} . geometric shapes, bold colors, dynamic composition, propaganda art style",
        "negative_prompt": "realistic, photorealistic, low contrast, plain, simple, abstract expressionism",
    },
    {
        "name": "artstyle-立体主义",
        "prompt": "cubist artwork {prompt} . geometric shapes, abstract, innovative, revolutionary",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "artstyle-表现主义",
        "prompt": "expressionist {prompt} . raw, emotional, dynamic, distortion for emotional effect, vibrant, use of unusual colors, detailed",
        "negative_prompt": "realism, symmetry, quiet, calm, photo",
    },
    {
        "name": "artstyle-涂鸦",
        "prompt": "graffiti style {prompt} . street art, vibrant, urban, detailed, tag, mural",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "artstyle-超现实主义",
        "prompt": "hyperrealistic art {prompt} . extremely high-resolution details, photographic, realism pushed to extreme, fine texture, incredibly lifelike",
        "negative_prompt": "simplified, abstract, unrealistic, impressionistic, low resolution",
    },
    {
        "name": "artstyle-印象派",
        "prompt": "impressionist painting {prompt} . loose brushwork, vibrant color, light and shadow play, captures feeling over form",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "artstyle-点彩派",
        "prompt": "pointillism style {prompt} . composed entirely of small, distinct dots of color, vibrant, highly detailed",
        "negative_prompt": "line drawing, smooth shading, large color fields, simplistic",
    },
    {
        "name": "artstyle-波普艺术",
        "prompt": "pop Art style {prompt} . bright colors, bold outlines, popular culture themes, ironic or kitsch",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, minimalist",
    },
    {
        "name": "artstyle-迷幻艺术",
        "prompt": "psychedelic style {prompt} . vibrant colors, swirling patterns, abstract forms, surreal, trippy",
        "negative_prompt": "monochrome, black and white, low contrast, realistic, photorealistic, plain, simple",
    },
    {
        "name": "artstyle-文艺复兴",
        "prompt": "renaissance style {prompt} . realistic, perspective, light and shadow, religious or mythological themes, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, modernist, minimalist, abstract",
    },
    {
        "name": "artstyle-蒸汽朋克",
        "prompt": "steampunk style {prompt} . antique, mechanical, brass and copper tones, gears, intricate, detailed",
        "negative_prompt": "deformed, glitch, noisy, low contrast, anime, photorealistic",
    },
    {
        "name": "artstyle-超现实主义",
        "prompt": "surrealist art {prompt} . dreamlike, mysterious, provocative, symbolic, intricate, detailed",
        "negative_prompt": "anime, photorealistic, realistic, deformed, glitch, noisy, low contrast",
    },
    {
        "name": "artstyle-字体设计",
        "prompt": "typographic art {prompt} . stylized, intricate, detailed, artistic, text-based",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "artstyle-水彩",
        "prompt": "watercolor painting {prompt} . vibrant, beautiful, painterly, detailed, textural, artistic",
        "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "futuristic-生物机械",
        "prompt": "biomechanical style {prompt} . blend of organic and mechanical elements, futuristic, cybernetic, detailed, intricate",
        "negative_prompt": "natural, rustic, primitive, organic, simplistic",
    },
    {
        "name": "futuristic-生物机械赛博朋克",
        "prompt": "biomechanical cyberpunk {prompt} . cybernetics, human-machine fusion, dystopian, organic meets artificial, dark, intricate, highly detailed",
        "negative_prompt": "natural, colorful, deformed, sketch, low contrast, watercolor",
    },
    {
        "name": "futuristic-赛博机械",
        "prompt": "cybernetic style {prompt} . futuristic, technological, cybernetic enhancements, robotics, artificial intelligence themes",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, historical, medieval",
    },
    {
        "name": "futuristic-赛博机械机器人",
        "prompt": "cybernetic robot {prompt} . android, AI, machine, metal, wires, tech, futuristic, highly detailed",
        "negative_prompt": "organic, natural, human, sketch, watercolor, low contrast",
    },
    {
        "name": "futuristic-赛博朋克城市景观",
        "prompt": "cyberpunk cityscape {prompt} . neon lights, dark alleys, skyscrapers, futuristic, vibrant colors, high contrast, highly detailed",
        "negative_prompt": "natural, rural, deformed, low contrast, black and white, sketch, watercolor",
    },
    {
        "name": "futuristic-未来主义",
        "prompt": "futuristic style {prompt} . sleek, modern, ultramodern, high tech, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, vintage, antique",
    },
    {
        "name": "futuristic-复古赛博朋克",
        "prompt": "retro cyberpunk {prompt} . 80's inspired, synthwave, neon, vibrant, detailed, retro futurism",
        "negative_prompt": "modern, desaturated, black and white, realism, low contrast",
    },
    {
        "name": "futuristic-复古未来主义",
        "prompt": "retro-futuristic {prompt} . vintage sci-fi, 50s and 60s style, atomic age, vibrant, highly detailed",
        "negative_prompt": "contemporary, realistic, rustic, primitive",
    },
    {
        "name": "futuristic-科幻",
        "prompt": "sci-fi style {prompt} . futuristic, technological, alien worlds, space themes, advanced civilizations",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, historical, medieval",
    },
    {
        "name": "futuristic-蒸汽波",
        "prompt": "vaporwave style {prompt} . retro aesthetic, cyberpunk, vibrant, neon colors, vintage 80s and 90s style, highly detailed",
        "negative_prompt": "monochrome, muted colors, realism, rustic, minimalist, dark",
    },
    {
        "name": "game-泡泡龙",
        "prompt": "Bubble Bobble style {prompt} . 8-bit, cute, pixelated, fantasy, vibrant, reminiscent of Bubble Bobble game",
        "negative_prompt": "realistic, modern, photorealistic, violent, horror",
    },
    {
        "name": "game-赛博朋克游戏",
        "prompt": "cyberpunk game style {prompt} . neon, dystopian, futuristic, digital, vibrant, detailed, high contrast, reminiscent of cyberpunk genre video games",
        "negative_prompt": "historical, natural, rustic, low detailed",
    },
    {
        "name": "game-格斗游戏",
        "prompt": "fighting game style {prompt} . dynamic, vibrant, action-packed, detailed character design, reminiscent of fighting video games",
        "negative_prompt": "peaceful, calm, minimalist, photorealistic",
    },
    {
        "name": "game-GTA",
        "prompt": "GTA-style artwork {prompt} . satirical, exaggerated, pop art style, vibrant colors, iconic characters, action-packed",
        "negative_prompt": "realistic, black and white, low contrast, impressionist, cubist, noisy, blurry, deformed",
    },
    {
        "name": "game-马里奥",
        "prompt": "Super Mario style {prompt} . vibrant, cute, cartoony, fantasy, playful, reminiscent of Super Mario series",
        "negative_prompt": "realistic, modern, horror, dystopian, violent",
    },
    {
        "name": "game-我的世界",
        "prompt": "Minecraft style {prompt} . blocky, pixelated, vibrant colors, recognizable characters and objects, game assets",
        "negative_prompt": "smooth, realistic, detailed, photorealistic, noise, blurry, deformed",
    },
    {
        "name": "game-宝可梦",
        "prompt": "Pokémon style {prompt} . vibrant, cute, anime, fantasy, reminiscent of Pokémon series",
        "negative_prompt": "realistic, modern, horror, dystopian, violent",
    },
    {
        "name": "game-复古街机",
        "prompt": "retro arcade style {prompt} . 8-bit, pixelated, vibrant, classic video game, old school gaming, reminiscent of 80s and 90s arcade games",
        "negative_prompt": "modern, ultra-high resolution, photorealistic, 3D",
    },
    {
        "name": "game-复古游戏",
        "prompt": "retro game art {prompt} . 16-bit, vibrant colors, pixelated, nostalgic, charming, fun",
        "negative_prompt": "realistic, photorealistic, 35mm film, deformed, glitch, low contrast, noisy",
    },
    {
        "name": "game-RPG奇幻游戏",
        "prompt": "role-playing game (RPG) style fantasy {prompt} . detailed, vibrant, immersive, reminiscent of high fantasy RPG games",
        "negative_prompt": "sci-fi, modern, urban, futuristic, low detailed",
    },
    {
        "name": "game-策略游戏",
        "prompt": "strategy game style {prompt} . overhead view, detailed map, units, reminiscent of real-time strategy video games",
        "negative_prompt": "first-person view, modern, photorealistic",
    },
    {
        "name": "game-街头霸王",
        "prompt": "Street Fighter style {prompt} . vibrant, dynamic, arcade, 2D fighting game, highly detailed, reminiscent of Street Fighter series",
        "negative_prompt": "3D, realistic, modern, photorealistic, turn-based strategy",
    },
    {
        "name": "game-塞尔达传说",
        "prompt": "Legend of Zelda style {prompt} . vibrant, fantasy, detailed, epic, heroic, reminiscent of The Legend of Zelda series",
        "negative_prompt": "sci-fi, modern, realistic, horror",
    },
    {
        "name": "misc-建筑",
        "prompt": "architectural style {prompt} . clean lines, geometric shapes, minimalist, modern, architectural drawing, highly detailed",
        "negative_prompt": "curved lines, ornate, baroque, abstract, grunge",
    },
    {
        "name": "misc-迪斯科",
        "prompt": "disco-themed {prompt} . vibrant, groovy, retro 70s style, shiny disco balls, neon lights, dance floor, highly detailed",
        "negative_prompt": "minimalist, rustic, monochrome, contemporary, simplistic",
    },
    {
        "name": "misc-梦境",
        "prompt": "dreamscape {prompt} . surreal, ethereal, dreamy, mysterious, fantasy, highly detailed",
        "negative_prompt": "realistic, concrete, ordinary, mundane",
    },
    {
        "name": "misc-反乌托邦",
        "prompt": "dystopian style {prompt} . bleak, post-apocalyptic, somber, dramatic, highly detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, cheerful, optimistic, vibrant, colorful",
    },
    {
        "name": "misc-童话",
        "prompt": "fairy tale {prompt} . magical, fantastical, enchanting, storybook style, highly detailed",
        "negative_prompt": "realistic, modern, ordinary, mundane",
    },
    {
        "name": "misc-哥特",
        "prompt": "gothic style {prompt} . dark, mysterious, haunting, dramatic, ornate, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, cheerful, optimistic",
    },
    {
        "name": "misc-垃圾摇滚",
        "prompt": "grunge style {prompt} . textured, distressed, vintage, edgy, punk rock vibe, dirty, noisy",
        "negative_prompt": "smooth, clean, minimalist, sleek, modern, photorealistic",
    },
    {
        "name": "misc-恐怖",
        "prompt": "horror-themed {prompt} . eerie, unsettling, dark, spooky, suspenseful, grim, highly detailed",
        "negative_prompt": "cheerful, bright, vibrant, light-hearted, cute",
    },
    {
        "name": "misc-可爱",
        "prompt": "kawaii style {prompt} . cute, adorable, brightly colored, cheerful, anime influence, highly detailed",
        "negative_prompt": "dark, scary, realistic, monochrome, abstract",
    },
    {
        "name": "misc-洛夫克拉夫特",
        "prompt": "lovecraftian horror {prompt} . eldritch, cosmic horror, unknown, mysterious, surreal, highly detailed",
        "negative_prompt": "light-hearted, mundane, familiar, simplistic, realistic",
    },
    {
        "name": "misc-恐怖",
        "prompt": "macabre style {prompt} . dark, gothic, grim, haunting, highly detailed",
        "negative_prompt": "bright, cheerful, light-hearted, cartoonish, cute",
    },
    {
        "name": "misc-漫画",
        "prompt": "manga style {prompt} . vibrant, high-energy, detailed, iconic, Japanese comic style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, Western comic style",
    },
    {
        "name": "misc-大都市",
        "prompt": "metropolis-themed {prompt} . urban, cityscape, skyscrapers, modern, futuristic, highly detailed",
        "negative_prompt": "rural, natural, rustic, historical, simple",
    },
    {
        "name": "misc-极简主义",
        "prompt": "minimalist style {prompt} . simple, clean, uncluttered, modern, elegant",
        "negative_prompt": "ornate, complicated, highly detailed, cluttered, disordered, messy, noisy",
    },
    {
        "name": "misc-单色",
        "prompt": "monochrome {prompt} . black and white, contrast, tone, texture, detailed",
        "negative_prompt": "colorful, vibrant, noisy, blurry, deformed",
    },
    {
        "name": "misc-航海",
        "prompt": "nautical-themed {prompt} . sea, ocean, ships, maritime, beach, marine life, highly detailed",
        "negative_prompt": "landlocked, desert, mountains, urban, rustic",
    },
    {
        "name": "misc-太空",
        "prompt": "space-themed {prompt} . cosmic, celestial, stars, galaxies, nebulas, planets, science fiction, highly detailed",
        "negative_prompt": "earthly, mundane, ground-based, realism",
    },
    {
        "name": "misc-彩色玻璃",
        "prompt": "stained glass style {prompt} . vibrant, beautiful, translucent, intricate, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "misc-科技时尚",
        "prompt": "techwear fashion {prompt} . futuristic, cyberpunk, urban, tactical, sleek, dark, highly detailed",
        "negative_prompt": "vintage, rural, colorful, low contrast, realism, sketch, watercolor",
    },
    {
        "name": "misc-部落",
        "prompt": "tribal style {prompt} . indigenous, ethnic, traditional patterns, bold, natural colors, highly detailed",
        "negative_prompt": "modern, futuristic, minimalist, pastel",
    },
    {
        "name": "misc-禅绕画",
        "prompt": "zentangle {prompt} . intricate, abstract, monochrome, patterns, meditative, highly detailed",
        "negative_prompt": "colorful, representative, simplistic, large fields of color",
    },
    {
        "name": "papercraft-拼贴",
        "prompt": "collage style {prompt} . mixed media, layered, textural, detailed, artistic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "papercraft-平面剪纸",
        "prompt": "flat papercut style {prompt} . silhouette, clean cuts, paper, sharp edges, minimalist, color block",
        "negative_prompt": "3D, high detail, noise, grainy, blurry, painting, drawing, photo, disfigured",
    },
    {
        "name": "papercraft-剪纸艺术",
        "prompt": "kirigami representation of {prompt} . 3D, paper folding, paper cutting, Japanese, intricate, symmetrical, precision, clean lines",
        "negative_prompt": "painting, drawing, 2D, noisy, blurry, deformed",
    },
    {
        "name": "papercraft-纸浆",
        "prompt": "paper mache representation of {prompt} . 3D, sculptural, textured, handmade, vibrant, fun",
        "negative_prompt": "2D, flat, photo, sketch, digital art, deformed, noisy, blurry",
    },
    {
        "name": "papercraft-纸卷",
        "prompt": "paper quilling art of {prompt} . intricate, delicate, curling, rolling, shaping, coiling, loops, 3D, dimensional, ornamental",
        "negative_prompt": "photo, painting, drawing, 2D, flat, deformed, noisy, blurry",
    },
    {
        "name": "papercraft-剪纸拼贴",
        "prompt": "papercut collage of {prompt} . mixed media, textured paper, overlapping, asymmetrical, abstract, vibrant",
        "negative_prompt": "photo, 3D, realistic, drawing, painting, high detail, disfigured",
    },
    {
        "name": "papercraft-剪纸阴影盒",
        "prompt": "3D papercut shadow box of {prompt} . layered, dimensional, depth, silhouette, shadow, papercut, handmade, high contrast",
        "negative_prompt": "painting, drawing, photo, 2D, flat, high detail, blurry, noisy, disfigured",
    },
    {
        "name": "papercraft-堆叠剪纸",
        "prompt": "stacked papercut art of {prompt} . 3D, layered, dimensional, depth, precision cut, stacked layers, papercut, high contrast",
        "negative_prompt": "2D, flat, noisy, blurry, painting, drawing, photo, deformed",
    },
    {
        "name": "papercraft-厚层剪纸",
        "prompt": "thick layered papercut art of {prompt} . deep 3D, volumetric, dimensional, depth, thick paper, high stack, heavy texture, tangible layers",
        "negative_prompt": "2D, flat, thin paper, low stack, smooth texture, painting, drawing, photo, deformed",
    },
    {
        "name": "photo-外星人",
        "prompt": "alien-themed {prompt} . extraterrestrial, cosmic, otherworldly, mysterious, sci-fi, highly detailed",
        "negative_prompt": "earthly, mundane, common, realistic, simple",
    },
    {
        "name": "photo-黑色电影",
        "prompt": "film noir style {prompt} . monochrome, high contrast, dramatic shadows, 1940s style, mysterious, cinematic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, vibrant, colorful",
    },
    {
        "name": "photo-魅力",
        "prompt": "glamorous photo {prompt} . high fashion, luxurious, extravagant, stylish, sensual, opulent, elegance, stunning beauty, professional, high contrast, detailed",
        "negative_prompt": "ugly, deformed, noisy, blurry, distorted, grainy, sketch, low contrast, dull, plain, modest",
    },
    {
        "name": "photo-HDR",
        "prompt": "HDR photo of {prompt} . High dynamic range, vivid, rich details, clear shadows and highlights, realistic, intense, enhanced contrast, highly detailed",
        "negative_prompt": "flat, low contrast, oversaturated, underexposed, overexposed, blurred, noisy",
    },
    {
        "name": "photo-手机摄影",
        "prompt": "iphone photo {prompt} . large depth of field, deep depth of field, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly, shallow depth of field, bokeh",
    },
    {
        "name": "photo-长时间曝光",
        "prompt": "long exposure photo of {prompt} . Blurred motion, streaks of light, surreal, dreamy, ghosting effect, highly detailed",
        "negative_prompt": "static, noisy, deformed, shaky, abrupt, flat, low contrast",
    },
    {
        "name": "photo-霓虹黑色",
        "prompt": "neon noir {prompt} . cyberpunk, dark, rainy streets, neon signs, high contrast, low light, vibrant, highly detailed",
        "negative_prompt": "bright, sunny, daytime, low contrast, black and white, sketch, watercolor",
    },
    {
        "name": "photo-剪影",
        "prompt": "silhouette style {prompt} . high contrast, minimalistic, black and white, stark, dramatic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, color, realism, photorealistic",
    },
    {
        "name": "photo-倾斜移位",
        "prompt": "tilt-shift photo of {prompt} . selective focus, miniature effect, blurred background, highly detailed, vibrant, perspective control",
        "negative_prompt": "blurry, noisy, deformed, flat, low contrast, unrealistic, oversaturated, underexposed",
    },
    {
        "name": "cinematic-天后",
        "prompt": "UHD, 8K, ultra detailed, a cinematic photograph of {prompt}, beautiful lighting, great composition",
        "negative_prompt": "ugly, deformed, noisy, blurry, NSFW",
    },
    {
        "name": "抽象表现主义",
        "prompt": "Abstract Expressionism Art, {prompt}, High contrast, minimalistic, colorful, stark, dramatic, expressionism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic",
    },
    {
        "name": "学院派",
        "prompt": "Academia, {prompt}, preppy Ivy League style, stark, dramatic, chic boarding school, academia",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, grunge, sloppy, unkempt",
    },
    {
        "name": "动作人偶",
        "prompt": "Action Figure, {prompt}, plastic collectable action figure, collectable toy action figure",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "可爱3D角色",
        "prompt": "Adorable 3D Character, {prompt}, 3D render, adorable character, 3D art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, grunge, sloppy, unkempt, photograph, photo, realistic",
    },
    {
        "name": "可爱卡哇伊",
        "prompt": "Adorable Kawaii, {prompt}, pretty, cute, adorable, kawaii",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, gothic, dark, moody, monochromatic",
    },
    {
        "name": "装饰艺术",
        "prompt": "Art Deco, {prompt}, sleek, geometric forms, art deco style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "新艺术",
        "prompt": "Art Nouveau, beautiful art, {prompt}, sleek, organic forms, long, sinuous, art nouveau style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, industrial, mechanical",
    },
    {
        "name": "星空气氛",
        "prompt": "Astral Aura, {prompt}, astral, colorful aura, vibrant energy",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "前卫",
        "prompt": "Avant-garde, {prompt}, unusual, experimental, avant-garde art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "巴洛克",
        "prompt": "Baroque, {prompt}, dramatic, exuberant, grandeur, baroque art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "包豪斯风格海报",
        "prompt": "Bauhaus-Style Poster, {prompt}, simple geometric shapes, clean lines, primary colors, Bauhaus-Style Poster",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "蓝图示意图",
        "prompt": "Blueprint Schematic Drawing, {prompt}, technical drawing, blueprint, schematic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "漫画",
        "prompt": "Caricature, {prompt}, exaggerated, comical, caricature",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realistic",
    },
    {
        "name": "卡通渲染艺术",
        "prompt": "Cel Shaded Art, {prompt}, 2D, flat color, toon shading, cel shaded style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "角色设计表",
        "prompt": "Character Design Sheet, {prompt}, character reference sheet, character turn around",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "古典艺术",
        "prompt": "Classicism Art, {prompt}, inspired by Roman and Greek culture, clarity, harmonious, classicism art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "色域绘画",
        "prompt": "Color Field Painting, {prompt}, abstract, simple, geometic, color field painting style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "彩色铅笔艺术",
        "prompt": "Colored Pencil Art, {prompt}, colored pencil strokes, light color, visible paper texture, colored pencil art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "概念艺术",
        "prompt": "Conceptual Art, {prompt}, concept art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "构成主义",
        "prompt": "Constructivism Art, {prompt}, minimalistic, geometric forms, constructivism art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "立体主义",
        "prompt": "Cubism Art, {prompt}, flat geometric forms, cubism art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "达达主义",
        "prompt": "Dadaism Art, {prompt}, satirical, nonsensical, dadaism art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "黑暗奇幻",
        "prompt": "Dark Fantasy Art, {prompt}, dark, moody, dark fantasy style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, bright, sunny",
    },
    {
        "name": "黑暗氛围",
        "prompt": "Dark Moody Atmosphere, {prompt}, dramatic, mysterious, dark moody atmosphere",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, vibrant, colorful, bright",
    },
    {
        "name": "DMT艺术风格",
        "prompt": "DMT Art Style, {prompt}, bright colors, surreal visuals, swirling patterns, DMT art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "涂鸦艺术",
        "prompt": "Doodle Art Style, {prompt}, drawing, freeform, swirling patterns, doodle art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "双重曝光",
        "prompt": "Double Exposure Style, {prompt}, double image ghost effect, image combination, double exposure style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "滴漆艺术",
        "prompt": "Dripping Paint Splatter Art, {prompt}, dramatic, paint drips, splatters, dripping paint",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "表现主义",
        "prompt": "Expressionism Art Style, {prompt}, movement, contrast, emotional, exaggerated forms, expressionism art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "褪色宝丽来照片",
        "prompt": "Faded Polaroid Photo, {prompt}, analog, old faded photo, old polaroid",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, vibrant, colorful",
    },
    {
        "name": "野兽派",
        "prompt": "Fauvism Art, {prompt}, painterly, bold colors, textured brushwork, fauvism art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "平面2D艺术",
        "prompt": "Flat 2D Art, {prompt}, simple flat color, 2-dimensional, Flat 2D Art Style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, 3D, photo, realistic",
    },
    {
        "name": "堡垒之夜艺术风格",
        "prompt": "Fortnite Art Style, {prompt}, 3D cartoon, colorful, Fortnite Art Style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, photo, realistic",
    },
    {
        "name": "未来主义",
        "prompt": "Futurism Art Style, {prompt}, dynamic, dramatic, Futurism Art Style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "故障艺术",
        "prompt": "Glitchcore Art Style, {prompt}, dynamic, dramatic, distorted, vibrant colors, glitchcore art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "低保真",
        "prompt": "Glo-fi Art Style, {prompt}, dynamic, dramatic, vibrant colors, glo-fi art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "古奇艺术风格",
        "prompt": "Googie Art Style, {prompt}, dynamic, dramatic, 1950's futurism, bold boomerang angles, Googie art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "涂鸦艺术",
        "prompt": "Graffiti Art Style, {prompt}, dynamic, dramatic, vibrant colors, graffiti art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "哈莱姆文艺复兴艺术",
        "prompt": "Harlem Renaissance Art Style, {prompt}, dynamic, dramatic, 1920s African American culture, Harlem Renaissance art style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "高级时尚",
        "prompt": "High Fashion, {prompt}, dynamic, dramatic, haute couture, elegant, ornate clothing, High Fashion",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "田园诗",
        "prompt": "Idyllic, {prompt}, peaceful, happy, pleasant, happy, harmonious, picturesque, charming",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "印象派",
        "prompt": "Impressionism, {prompt}, painterly, small brushstrokes, visible brushstrokes, impressionistic style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "信息图绘制",
        "prompt": "Infographic Drawing, {prompt}, diagram, infographic",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "墨水滴画",
        "prompt": "Ink Dripping Drawing, {prompt}, ink drawing, dripping ink",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, colorful, vibrant",
    },
    {
        "name": "日本水墨画",
        "prompt": "Japanese Ink Drawing, {prompt}, ink drawing, inkwash, Japanese Ink Drawing",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, colorful, vibrant",
    },
    {
        "name": "排列摄影",
        "prompt": "Knolling Photography, {prompt}, flat lay photography, object arrangment, knolling photography",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "轻松愉快的氛围",
        "prompt": "Light Cheery Atmosphere, {prompt}, happy, joyful, cheerful, carefree, gleeful, lighthearted, pleasant atmosphere",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, monochromatic, dark, moody",
    },
    {
        "name": "标志设计",
        "prompt": "Logo Design, {prompt}, dynamic graphic art, vector art, minimalist, professional logo design",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "奢华优雅",
        "prompt": "Luxurious Elegance, {prompt}, extravagant, ornate, designer, opulent, picturesque, lavish",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "微距摄影",
        "prompt": "Macro Photography, {prompt}, close-up, macro 100mm, macro photography",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "曼陀罗艺术",
        "prompt": "Mandola art style, {prompt}, complex, circular design, mandola",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "马克笔画",
        "prompt": "Marker Drawing, {prompt}, bold marker lines, visibile paper texture, marker drawing",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, photograph, realistic",
    },
    {
        "name": "中世纪主义",
        "prompt": "Medievalism, {prompt}, inspired by The Middle Ages, medieval art, elaborate patterns and decoration, Medievalism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "极简主义",
        "prompt": "Minimalism, {prompt}, abstract, simple geometic shapes, hard edges, sleek contours, Minimalism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "新巴洛克",
        "prompt": "Neo-Baroque, {prompt}, ornate and elaborate, dynaimc, Neo-Baroque",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "新拜占庭",
        "prompt": "Neo-Byzantine, {prompt}, grand decorative religious style, Orthodox Christian inspired, Neo-Byzantine",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "新未来主义",
        "prompt": "Neo-Futurism, {prompt}, high-tech, curves, spirals, flowing lines, idealistic future, Neo-Futurism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "新印象派",
        "prompt": "Neo-Impressionism, {prompt}, tiny dabs of color, Pointillism, painterly, Neo-Impressionism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, photograph, realistic",
    },
    {
        "name": "新洛可可",
        "prompt": "Neo-Rococo, {prompt}, curved forms, naturalistic ornamentation, elaborate, decorative, gaudy, Neo-Rococo",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "新古典主义",
        "prompt": "Neoclassicism, {prompt}, ancient Rome and Greece inspired, idealic, sober colors, Neoclassicism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "欧普艺术",
        "prompt": "Op Art, {prompt}, optical illusion, abstract, geometric pattern, impression of movement, Op Art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "华丽复杂",
        "prompt": "Ornate and Intricate, {prompt}, decorative, highly detailed, elaborate, ornate, intricate",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "铅笔素描",
        "prompt": "Pencil Sketch Drawing, {prompt}, black and white drawing, graphite drawing",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "波普艺术2",
        "prompt": "Pop Art, {prompt}, vivid colors, flat color, 2D, strong lines, Pop Art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, photo, realistic",
    },
    {
        "name": "洛可可",
        "prompt": "Rococo, {prompt}, flamboyant, pastel colors, curved lines, elaborate detail, Rococo",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "剪影艺术",
        "prompt": "Silhouette Art, {prompt}, high contrast, well defined, Silhouette Art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "简单矢量艺术",
        "prompt": "Simple Vector Art, {prompt}, 2D flat, simple shapes, minimalistic, professional graphic, flat color, high contrast, Simple Vector Art",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, 3D, photo, realistic",
    },
    {
        "name": "草图大师",
        "prompt": "Sketchup, {prompt}, CAD, professional design, Sketchup",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, photo, photograph",
    },
    {
        "name": "蒸汽朋克2",
        "prompt": "Steampunk, {prompt}, retrofuturistic science fantasy, steam-powered tech, vintage industry, gears, neo-victorian, steampunk",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "超现实主义",
        "prompt": "Surrealism, {prompt}, expressive, dramatic, organic lines and forms, dreamlike and mysterious, Surrealism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realistic",
    },
    {
        "name": "至上主义",
        "prompt": "Suprematism, {prompt}, abstract, limited color palette, geometric forms, Suprematism",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realistic",
    },
    {
        "name": "地形生成",
        "prompt": "Terragen, {prompt}, beautiful massive landscape, epic scenery, Terragen",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "宁静放松的氛围",
        "prompt": "Tranquil Relaxing Atmosphere, {prompt}, calming style, soothing colors, peaceful, idealic, Tranquil Relaxing Atmosphere",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, oversaturated",
    },
    {
        "name": "贴纸设计",
        "prompt": "Vector Art Stickers, {prompt}, professional vector design, sticker designs, Sticker Sheet",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "鲜艳边缘光",
        "prompt": "Vibrant Rim Light, {prompt}, bright rim light, high contrast, bold edge light",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "体积光",
        "prompt": "Volumetric Lighting, {prompt}, light depth, dramatic atmospheric lighting, Volumetric Lighting",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast",
    },
    {
        "name": "水彩2",
        "prompt": "Watercolor style painting, {prompt}, visible paper texture, colorwash, watercolor",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, photo, realistic",
    },
    {
        "name": "异想天开又好玩",
        "prompt": "Whimsical and Playful, {prompt}, imaginative, fantastical, bight colors, stylized, happy, Whimsical and Playful",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, drab, boring, moody",
    },
    {
        "name": "Fooocus增强",
        "prompt": "{prompt}",
        "negative_prompt": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D ,3D Game, 3D Game Scene, 3D Character:1.1), (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3)",
    },
    {
        "name": "Fooocus半写实",
        "prompt": "{prompt} .",
        "negative_prompt": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, mutilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (bad hands, bad anatomy, bad body, bad face, bad teeth, bad arms, bad legs, deformities:1.3)",
    },
    {
        "name": "Fooocus锐利",
        "prompt": "cinematic still {prompt} . emotional, harmonious, vignette, 8k epic detailed, shot on kodak, 35mm photo, sharp focus, high budget, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, (blur, blurry, bokeh), text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "Fooocus杰作",
        "prompt": "(masterpiece), (best quality), (ultra-detailed), {prompt}, illustration, disheveled hair, detailed eyes, perfect composition, moist skin, intricate details, earrings",
        "negative_prompt": "longbody, lowres, bad anatomy, bad hands, missing fingers, pubic hair,extra digit, fewer digits, cropped, worst quality, low quality",
    },
    {
        "name": "Fooocus摄影",
        "prompt": "photograph {prompt}, 50mm . cinematic 8k epic detailed 8k epic detailed photograph shot on kodak detailed cinematic hbo dark moody, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage",
        "negative_prompt": "Brad Pitt, bokeh, depth of field, blurry, cropped, regular face, saturated, contrast, deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck",
    },
    {
        "name": "Fooocus负片",
        "prompt": "{prompt} .",
        "negative_prompt": "deformed, bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet, abnormal fingers, drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly, anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch",
    },
    {
        "name": "Fooocus电影风格",
        "prompt": "cinematic still {prompt} . emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "Cosplay - 赛车女郎 (Race Queen)",
        "prompt": "{prompt}, race queen costume, shiny vinyl outfit, holding a parasol, f1 circuit background, sponsors logos, high heel boots, sleek and sporty, vibrant colors, outdoor daylight, grandstand in background, professional gravure photography",
        "negative_prompt": "dirty, rusty, dark, casual clothes, indoor",
    },
    {
        "name": "Cosplay - 机械女仆 (Cyber Maid)",
        "prompt": "{prompt}, cyberpunk maid, mechanical joints, glowing neon accents, futuristic cafe interior, metallic textures, latex dress, holographic interface, night city outside window, sci-fi aesthetic, cool color temperature",
        "negative_prompt": "vintage, rustic, natural nature, warm lighting",
    },
    {
        "name": "Cosplay - 兔女郎 (Glossy Bunny)",
        "prompt": "{prompt}, playboy bunny style, black glossy bodysuit, fishnet tights, bunny ears, cuffs and collar, luxury casino background, dim warm lighting, bokeh lights, classy sexy, velvet texture",
        "negative_prompt": "cheap fabric, daylight, outdoor, messy",
    },
    {
        "name": "Cosplay - 战斗修女 (Battle Nun)",
        "prompt": "{prompt}, gothic battle nun, torn habit, holding a weapon (rosary or gun), ruined church background, dramatic volumetric lighting, god rays, dust particles, dark fantasy, intense expression, dynamic angle",
        "negative_prompt": "peaceful, bright, clean, modern building",
    },
    {
        "name": "Cosplay - 巫女 (Shrine Maiden)",
        "prompt": "{prompt}, traditional japanese miko outfit, hakama pants, white kimono top, holding a gohei, shinto shrine background, cherry blossoms falling, serene atmosphere, soft natural light, film photography style",
        "negative_prompt": "neon, modern city, sci-fi, latex",
    },
    {
        "name": "Cosplay - 中华娘 (China Dress)",
        "prompt": "{prompt}, cheongsam china dress, high slit, silk texture with embroidery, bun hairstyles (odango), chinatown neon lights background, wong kar wai style lighting, moody and atmospheric, cinematic bokeh",
        "negative_prompt": "western architecture, plain background, flat lighting",
    },
    {
        "name": "Cosplay - 护士 (Pink Nurse)",
        "prompt": "{prompt}, stylized nurse outfit, pink and white theme, holding a giant syringe prop, pastel hospital studio set, cute aesthetic, soft focus, dreamlike, yami-kawaii vibe",
        "negative_prompt": "bloody, horror, realistic hospital, gritty",
    },
    {
        "name": "Cosplay - 魅魔 (Succubus)",
        "prompt": "{prompt}, succubus cosplay, small bat wings, heart shaped tail, gothic lolita influence, dark studio background with purple rim light, mysterious mist, seductive gaze, vampire aesthetic",
        "negative_prompt": "daylight, sun, holy, angel",
    },
    {
        "name": "Cosplay - 忍者 (Kunoichi)",
        "prompt": "{prompt}, kunoichi ninja costume, fishnet mesh, face mask pulled down, bamboo forest at night, moonlight, dynamic pose, katana on back, japanese historical fantasy",
        "negative_prompt": "modern city, guns, western clothing",
    },
    {
        "name": "Cosplay - 魔法少女 (Magical Girl)",
        "prompt": "{prompt}, magical girl transformation sequence, floating ribbons, glowing staff, sparkles and glitter effects, starry sky background, anime vivid colors, dynamic composition, low angle shot",
        "negative_prompt": "realistic, dull colors, static",
    },
    {
        "name": "Cosplay - 蒸汽朋克 (Steampunk)",
        "prompt": "{prompt}, steampunk aviator, brass goggles, corset, leather gears, airship deck background, sepia tone, clouds and blue sky, adventure vibe, detailed mechanical accessories",
        "negative_prompt": "cyberpunk, neon, modern technology",
    },
    {
        "name": "Cosplay - 异世界精灵 (Elf Archer)",
        "prompt": "{prompt}, fantasy elf, pointed ears, green and brown leather armor, ancient forest background, magical fireflies, ethereal lighting, nature fantasy, detailed vegetation",
        "negative_prompt": "urban, concrete, sci-fi, indoors",
    },
    {
        "name": "Cosplay - 绝地求生 (Tactical Gear)",
        "prompt": "{prompt}, tactical military gear, bulletproof vest, cropped top, cargo pants, abandoned warehouse, cinematic action lighting, dust in air, tough but cute, survival game aesthetic",
        "negative_prompt": "clean studio, fantasy, dress, heels",
    },
    {
        "name": "Cosplay - 体育服 (Bloomers)",
        "prompt": "{prompt}, retro japanese gym uniform, bloomers, white t-shirt, school gymnasium background, wooden floor, volleyball net, sweaty skin texture, afternoon sunlight, youth vibe",
        "negative_prompt": "dark, night, outdoor, fancy dress",
    },
    {
        "name": "Cosplay - 僵尸新娘 (Ghost Bride)",
        "prompt": "{prompt}, tattered wedding dress, pale skin, blue roses, spooky graveyard background, fog, moonlight, tim burton aesthetic, gothic romance, melancholy expression",
        "negative_prompt": "sunny, happy, colorful, modern",
    },
    {
        "name": "Cosplay - 圣诞装 (Santa Girl)",
        "prompt": "{prompt}, santa claus bikini dress, white fur trim, holding a gift box, christmas tree background with bokeh lights, festive atmosphere, winter night, warm cozy lighting",
        "negative_prompt": "summer, beach, tropical, green grass",
    },
    {
        "name": "Cosplay - 万圣节魔女 (Halloween Witch)",
        "prompt": "{prompt}, cute witch costume, large pointed hat, holding a pumpkin lantern, orange and purple lights, halloween decorations, playful expression, fantasy night",
        "negative_prompt": "scary, horror, gore, realistic",
    },
    {
        "name": "Cosplay - 办公室OL (Office Lady)",
        "prompt": "{prompt}, tight pencil skirt, white blouse, glasses, office background with city view, holding documents, professional look, soft office lighting, confident pose",
        "negative_prompt": "fantasy, armor, swimsuit, messy",
    },
    {
        "name": "Cosplay - 兽耳娘 (Catgirl)",
        "prompt": "{prompt}, nekomimi catgirl, fluffy cat ears, paw gloves, oversized bell collar, cozy room background, playful pose, whiskers makeup, kawaii animal theme",
        "negative_prompt": "serious, human ears only, realistic animal",
    },
    {
        "name": "Cosplay - 摄影会现场 (Studio Session)",
        "prompt": "{prompt}, sitting on a white cube, professional photo studio, softboxes and umbrellas visible in background, plain white cyclorama, fashion model pose, clean lighting, behind the scenes vibe",
        "negative_prompt": "outdoor, complex background, dark",
    },
    {
        "name": "Cosplay - 圣骑士 (Paladin)",
        "prompt": "{prompt}, silver plate armor with gold trim, white cape, holding a sword, fantasy castle courtyard background, lens flare, holy atmosphere, majestic pose, metallic texture, knight commander",
        "negative_prompt": "rust, dirty, dark, casual clothes",
    },
    {
        "name": "Cosplay - 暗夜精灵 (Dark Elf)",
        "prompt": "{prompt}, dark elf skin tone option, silver long hair, purple leather armor, glowing magical runes, underground cavern background with bioluminescent plants, mysterious, mystical atmosphere",
        "negative_prompt": "sunlight, human ears, bright day",
    },
    {
        "name": "Cosplay - 龙娘 (Dragon Girl)",
        "prompt": "{prompt}, dragon horns, scales on skin patches, chinese style dress with slits, mountain peak background, clouds swirling, fantasy martial arts pose, mythical aura, sharp eyes",
        "negative_prompt": "western armor, modern city, wings obstructing face",
    },
    {
        "name": "Cosplay - 炼金术士 (Alchemist)",
        "prompt": "{prompt}, steampunk fantasy robe, holding bubbling potion flask, library filled with scrolls background, magical smoke, messy desk, curious expression, detailed glass texture",
        "negative_prompt": "empty room, sci-fi, digital",
    },
    {
        "name": "Cosplay - 森林射手 (Archer)",
        "prompt": "{prompt}, green hooded cloak, leather corset, holding a longbow, dense forest background, sunbeams through leaves (tyndall effect), focused gaze, nature particles",
        "negative_prompt": "gun, urban, indoor, neon",
    },
    {
        "name": "Cosplay - 堕天使 (Fallen Angel)",
        "prompt": "{prompt}, black feathered wings, tattered black dress, chains, gothic cathedral ruins background, dark stormy sky, melancholic expression, dramatic lighting, feathers falling",
        "negative_prompt": "white wings, happy, sunny, clean",
    },
    {
        "name": "Cosplay - 维京女战士 (Viking)",
        "prompt": "{prompt}, fur-lined leather armor, war paint on face, snowy fjord background, holding a round shield, cold breath vapor, fierce but beautiful, nordic aesthetic",
        "negative_prompt": "tropical, delicate, silk, modern",
    },
    {
        "name": "Cosplay - 阿拉伯舞娘 (Dancer)",
        "prompt": "{prompt}, belly dancer outfit, sheer veils, gold jewelry, desert oasis background at sunset, warm golden lighting, intricate henna tattoos, exotic atmosphere",
        "negative_prompt": "cold, snow, heavy armor, office",
    },
    {
        "name": "Cosplay - 海盗船长 (Pirate)",
        "prompt": "{prompt}, tricorn hat, pirate captain coat, holding a flintlock pistol, ship deck background, ocean horizon, adventure vibe, wind blowing coat, cinematic",
        "negative_prompt": "modern ship, navy uniform, clean studio",
    },
    {
        "name": "Cosplay - 阴阳师 (Onmyoji)",
        "prompt": "{prompt}, traditional heian period clothing, tall hat, holding paper talismans (ofuda), mystical japanese temple background, blue spiritual fire, supernatural atmosphere",
        "negative_prompt": "western magic, wand, medieval europe",
    },
    {
        "name": "Cosplay - 太空驾驶员 (Plugsuit)",
        "prompt": "{prompt}, tight latex sci-fi plugsuit, glossy texture, interface headset, inside mech cockpit, holographic displays, neon rim lights, evangelion style aesthetic, futuristic",
        "negative_prompt": "fabric, loose clothes, fantasy, nature",
    },
    {
        "name": "Cosplay - 仿生人 (Android)",
        "prompt": "{prompt}, android with visible ball joints, porcelain skin texture, data cables background, server room, cold blue lighting, emotionless expression, sci-fi doll",
        "negative_prompt": "human skin texture, messy, warm lights",
    },
    {
        "name": "Cosplay - 赛博忍者 (Cyber Ninja)",
        "prompt": "{prompt}, high-tech ninja suit, carbon fiber texture, glowing katana, neo-tokyo rooftop background, rain, cyberpunk city lights, dynamic crouching pose",
        "negative_prompt": "historical, traditional, daylight",
    },
    {
        "name": "Cosplay - 废土生存 (Wasteland)",
        "prompt": "{prompt}, mad max style gear, goggles, dust mask hanging on neck, desert ruins background, rusty metal, gritty texture, sunset backlight, tough survivalist",
        "negative_prompt": "clean, shiny, luxury, indoor",
    },
    {
        "name": "Cosplay - 银河歌姬 (Space Idol)",
        "prompt": "{prompt}, holographic dress, floating crystals, space stage background with stars and planets, singing into sci-fi mic, vibrant nebula colors, macross style",
        "negative_prompt": "earth, street, plain background",
    },
    {
        "name": "Cosplay - 特工 (Secret Agent)",
        "prompt": "{prompt}, black tactical catsuit, harness, night cityscape background, holding a silenced pistol, cool attitude, action movie poster style, sleek hair",
        "negative_prompt": "colorful, cute, frilly, daylight",
    },
    {
        "name": "Cosplay - 实验室少女 (Subject Zero)",
        "prompt": "{prompt}, wearing white hospital gown or bandages, cables attached to body, sterile white laboratory background, floating in water tank style, ethereal, mysterious sci-fi",
        "negative_prompt": "dirty, dark, warm, bedroom",
    },
    {
        "name": "Cosplay - 宇航员便服 (Space Casual)",
        "prompt": "{prompt}, futuristic casual wear, transparent plastic jacket, spaceship corridor background, zero gravity hair effect, floating objects, clean sci-fi aesthetic",
        "negative_prompt": "dirty, retro, earth gravity",
    },
    {
        "name": "Cosplay - 虚拟玩家 (VR Gamer)",
        "prompt": "{prompt}, wearing futuristic VR headset (visor up), glowing headphones, gaming room background with RGB lights, cyber fashion, digital glitch effects, gamer girl vibe",
        "negative_prompt": "traditional, nature, rustic",
    },
    {
        "name": "Cosplay - 激光女警 (Future Police)",
        "prompt": "{prompt}, futuristic police uniform, armored vest, visor, flying patrol car background, blue and red sirens light, cyberpunk law enforcement, authoritarian but cute",
        "negative_prompt": "retro police, current day, regular car",
    },
    {
        "name": "Cosplay - 空姐 (Stewardess)",
        "prompt": "{prompt}, retro pan-am style flight attendant uniform, pillbox hat, airport runway background, pulling a suitcase, wind blowing scarf, elegant travel vibe, professional smile",
        "negative_prompt": "messy, inside plane, casual",
    },
    {
        "name": "Cosplay - 女仆 (Classic Maid)",
        "prompt": "{prompt}, victorian maid outfit, long skirt, white apron, holding a silver tray with tea set, european mansion interior, elegant posture, afternoon tea time",
        "negative_prompt": "short skirt, latex, neon, cafe",
    },
    {
        "name": "Cosplay - 啦啦队 (Cheerleader)",
        "prompt": "{prompt}, american style cheerleader uniform, crop top, pleated skirt, holding pompoms, stadium background with bright lights, energetic jump or pose, youthful vibe",
        "negative_prompt": "dark, serious, indoor, formal",
    },
    {
        "name": "Cosplay - 女警官 (Police)",
        "prompt": "{prompt}, stylized police uniform, miniskirt, handcuffs on belt, leaning on a police car, city street background, sunglasses, authoritative stance, cool beauty",
        "negative_prompt": "bloody, horror, fantasy, swim",
    },
    {
        "name": "Cosplay - 教师 (Teacher)",
        "prompt": "{prompt}, tight pencil skirt, white shirt, glasses, holding a pointer, classroom blackboard background with chalk writing, serious but sexy expression, office lady vibe",
        "negative_prompt": "outdoor, fantasy, child, student",
    },
    {
        "name": "Cosplay - 网球手 (Tennis)",
        "prompt": "{prompt}, white tennis dress, visor, holding tennis racket, sunny tennis court background, sweat on skin, dynamic sports photography, healthy sexy",
        "negative_prompt": "night, indoor, rain, dress shoes",
    },
    {
        "name": "Cosplay - 餐厅服务员 (American Diner)",
        "prompt": "{prompt}, retro 50s diner waitress, striped dress, apron, holding a milkshake, roller skates (optional), neon diner sign background, colorful pop aesthetic",
        "negative_prompt": "dark, modern, gothic, japanese",
    },
    {
        "name": "Cosplay - 修女 (Nun)",
        "prompt": "{prompt}, traditional nun habit, rosary beads, stained glass window background, sun rays, praying pose, serene and holy atmosphere, forbidden beauty",
        "negative_prompt": "battle, weapon, torn clothes, dark",
    },
    {
        "name": "Cosplay - 军装指挥官 (Military)",
        "prompt": "{prompt}, military dress uniform, peaked cap, cape over shoulders, medals, war room map background, stern expression, anime military aesthetic",
        "negative_prompt": "camouflage, dirty, field battle, casual",
    },
    {
        "name": "Cosplay - 芭蕾舞者 (Ballerina)",
        "prompt": "{prompt}, white ballet tutu, satin pointe shoes, theater stage with spotlight, graceful pose, elegant atmosphere, swan lake vibe, artistic photography",
        "negative_prompt": "street, sporty, rough, dark",
    },
    {
        "name": "Cosplay - 花魁 (Oiran)",
        "prompt": "{prompt}, elaborate oiran kimono, many hairpins, holding a long pipe (kiseru), red tatami room background, gold leaf screen, luxurious and seductive, vibrant red and gold colors",
        "negative_prompt": "simple kimono, outdoor, daylight, modern",
    },
    {
        "name": "Cosplay - 哥特萝莉 (Gothic Lolita)",
        "prompt": "{prompt}, black frilly lolita dress, lace parasol, bonnet, rose garden background, cloudy sky, doll-like makeup, elegant gothic aesthetic",
        "negative_prompt": "sweet colors, sunny, casual, sporty",
    },
    {
        "name": "Cosplay - 不良少女 (Sukeban)",
        "prompt": "{prompt}, long skirt school uniform, sailor collar, holding a wooden sword or bat, graffiti wall background, defiant expression, retro 80s delinquent vibe",
        "negative_prompt": "short skirt, cute, happy, clean",
    },
    {
        "name": "Cosplay - 昭和偶像 (Retro Idol)",
        "prompt": "{prompt}, 80s hairstyle, puffy sleeve dress, holding a retro microphone, vintage stage background, soft hazy filter, city pop album cover style, nostalgic",
        "negative_prompt": "modern, hd, sharp, neon",
    },
    {
        "name": "Cosplay - 浴衣约会 (Yukata Date)",
        "prompt": "{prompt}, wearing colorful yukata, holding a fan and festival pouch, summer festival background with lanterns, fireworks in sky, looking back, romantic night",
        "negative_prompt": "winter, cold, swimsuit, indoor",
    },
    {
        "name": "Cosplay - 剑道少女 (Kendo)",
        "prompt": "{prompt}, wearing hakama and bogu (chest armor), holding bamboo sword (shinai), traditional dojo background, sunlight dust motes, sweat, focused martial arts vibe",
        "negative_prompt": "fantasy sword, outdoor, western armor",
    },
    {
        "name": "Cosplay - 视觉系 (Visual Kei)",
        "prompt": "{prompt}, elaborate rock costume, leather and lace, heavy makeup, chains, concert backstage background, edgy and cool, j-rock aesthetic",
        "negative_prompt": "natural, sweet, pastel, plain",
    },
    {
        "name": "Cosplay - 幽灵少女 (Yurei)",
        "prompt": "{prompt}, white burial kimono, long black hair covering part of face, old japanese house background, blue spirit orbs, eerie but beautiful, horror romance",
        "negative_prompt": "zombie, blood, gore, western ghost",
    },
    {
        "name": "Cosplay - 狐妖 (Kitsune)",
        "prompt": "{prompt}, fox ears and nine tails, shrine maiden outfit modified, torii gate pathway background, mystical fog, mask on side of head, supernatural beauty",
        "negative_prompt": "western fox, furry, realistic animal",
    },
    {
        "name": "Cosplay - 女文豪 (Taisho Romance)",
        "prompt": "{prompt}, taisho era hakama outfit, boots, big ribbon in hair, old coffee shop background, reading a book, retro japanese aesthetic, intellectual vibe",
        "negative_prompt": "modern, sci-fi, swimsuit, armor",
    },
    {
        "name": "Cosplay - 史莱姆娘 (Slime Girl)",
        "prompt": "{prompt}, translucent blue skin parts, liquid texture clothes, dungeon background, glowing from within, fantasy monster girl, gooey aesthetic, magical",
        "negative_prompt": "solid, opaque, human skin only, dry",
    },
    {
        "name": "Cosplay - 绷带装 (Bandage)",
        "prompt": "{prompt}, body wrapped in white bandages, torn fabrics, abandoned hospital background, dramatic shadows, fragile beauty, edgy fashion",
        "negative_prompt": "mummy, horror, gore, clean",
    },
    {
        "name": "Cosplay - 湿身衬衫 (Wet Shirt)",
        "prompt": "{prompt}, wearing oversized white shirt, wet and translucent sticking to skin, rain or pool background, hair wet, cinematic lighting, vulnerable vibe",
        "negative_prompt": "dry, thick fabric, nudity, cartoon",
    },
    {
        "name": "Cosplay - 礼品丝带 (Ribbon Wrapped)",
        "prompt": "{prompt}, body wrapped in red satin ribbons, large bow, white studio background, high key lighting, gift concept, playful and cute, fashion editorial style",
        "negative_prompt": "bondage, dark, scary, messy",
    },
    {
        "name": "Cosplay - 水晶裙 (Crystal)",
        "prompt": "{prompt}, dress made of crystals and glass, refraction effects, prism rainbow lights, abstract background, ethereal fantasy, high fashion, shiny",
        "negative_prompt": "cloth, cotton, dull, matte",
    },
    {
        "name": "Cosplay - 胶衣猫女 (Latex Cat)",
        "prompt": "{prompt}, full body black latex suit, cat mask, whip, rooftop night background, moon, shiny texture highlights, seductive thief",
        "negative_prompt": "fabric, matte, day, cute",
    },
    {
        "name": "Cosplay - 鲜花裙 (Flower Fairy)",
        "prompt": "{prompt}, dress made of real petals and flowers, macro photography perspective (small size), garden background blurred, morning dew, fantasy fairy aesthetic",
        "negative_prompt": "artificial flowers, plastic, urban",
    },
    {
        "name": "Cosplay - 扑克女王 (Queen of Hearts)",
        "prompt": "{prompt}, red and black heart theme dress, holding playing cards, wonderland background, surreal perspective, royal attitude, fantasy costume",
        "negative_prompt": "casino, realistic, modern",
    },
    {
        "name": "Cosplay - 婚纱战损 (Ruined Bride)",
        "prompt": "{prompt}, elaborate white wedding dress, torn and dirty at hem, holding a weapon, battlefield ruins background, sunset smoke, tragic beauty, cinematic contrast",
        "negative_prompt": "clean wedding, church, happy, party",
    },
    {
        "name": "Cosplay - 赛博格半身 (Cyborg)",
        "prompt": "{prompt}, half human half machine, metallic skin parts, glowing lines, futuristic city background, sorrowful expression, ghost in the shell vibe",
        "negative_prompt": "full robot, full human, messy",
    },
    {
        "name": "网红 - 对镜自拍 (Mirror Selfie)",
        "prompt": "{prompt}, mirror selfie shot, holding smartphone, bedroom background, messy bed, casual loungewear, flash photography reflection, authentic influencer vibe, slightly tilted angle, cute phone case",
        "negative_prompt": "professional camera, studio lighting, third person view, tripod",
    },
    {
        "name": "网红 - 咖啡探店 (Cafe Date)",
        "prompt": "{prompt}, sitting at a cafe table, holding a latte art coffee, window seat with city street view, natural daylight, date pov, trendy fashion, relaxed atmosphere, candid shot",
        "negative_prompt": "dark, night, studio, looking at camera",
    },
    {
        "name": "网红 - 温泉旅行 (Onsen Trip)",
        "prompt": "{prompt}, wearing a yukata, japanese ryokan interior, tatami mats, onsen town street at night, holding a wooden bucket, steam, warm orange lighting, traditional vibe, blushing cheeks",
        "negative_prompt": "modern hotel, western clothes, swimsuit, cold colors",
    },
    {
        "name": "网红 - 迪士尼乐园 (Theme Park)",
        "prompt": "{prompt}, wearing mickey mouse ear headband, holding a churro, theme park castle background, crowded but blurred, sunset golden hour, colorful balloons, happy smile, tourist photo",
        "negative_prompt": "empty, dark, horror, serious face",
    },
    {
        "name": "网红 - 晨间苏醒 (Morning Bedhead)",
        "prompt": "{prompt}, lying in bed, white sheets, messy hair, oversized white t-shirt, morning sunlight streaming through curtains, POV shot, intimate atmosphere, sleepy eyes, no makeup look",
        "negative_prompt": "heavy makeup, night, party, outdoor",
    },
    {
        "name": "网红 - 夜跑/健身 (Night Gym)",
        "prompt": "{prompt}, wearing yoga pants and sports bra, gym mirror background or night running track, sweat on skin, ponytail, holding water bottle, fitness influencer, energetic, neon city lights in distance",
        "negative_prompt": "lazy, dress, high heels, eating",
    },
    {
        "name": "网红 - 豪车副驾 (Car Passenger)",
        "prompt": "{prompt}, sitting in passenger seat of luxury car, wearing seatbelt, sunlight coming through windshield, dashboard visible, travel vibe, sunglasses on head, leather seats texture",
        "negative_prompt": "driving, bus, train, outside car",
    },
    {
        "name": "网红 - 街头抓拍 (Harajuku Street)",
        "prompt": "{prompt}, walking on harajuku street, fashionable streetwear, looking back at camera, crowded japanese street background, colorful signs, motion blur on background people, paparazzi style snapshot",
        "negative_prompt": "studio, posed, static, empty street",
    },
    {
        "name": "网红 - 海边夕阳 (Beach Sunset)",
        "prompt": "{prompt}, walking on the beach, summer sundress (not bikini), wind blowing hair, golden sunset horizon, lens flare, romantic atmosphere, silhouette effect, warm colors",
        "negative_prompt": "midday, harsh shadows, snow, studio",
    },
    {
        "name": "网红 - 便利店深夜 (Konbini Night)",
        "prompt": "{prompt}, standing in front of japanese convenience store shelves, holding snacks and drink, fluorescent lighting, late night vibe, casual hoodie, glass reflection, candid everyday moment",
        "negative_prompt": "luxury, daylight, nature, historical",
    },
    {
        "name": "网红 - 补妆特写 (Makeup Touch-up)",
        "prompt": "{prompt}, extreme close-up of face, applying lipstick or mascara, holding a compact mirror, ring light reflection in eyes, flawless skin texture, beauty influencer style, macro photography",
        "negative_prompt": "full body, wide shot, blurry, low res",
    },
    {
        "name": "网红 - 公园野餐 (Park Picnic)",
        "prompt": "{prompt}, lying on picnic mat, green grass, picnic basket and fruits, top-down view or low angle, spring cherry blossoms, dappled sunlight, pastel colors, soft dreamy vibe",
        "negative_prompt": "winter, rain, concrete, dark",
    },
    {
        "name": "网红 - 图书馆学习 (Study Vibes)",
        "prompt": "{prompt}, wearing round glasses, library background with bookshelves, holding a pen and notebook, whisper quiet atmosphere, academia aesthetic, soft indoor lighting, focused expression",
        "negative_prompt": "loud, party, sport, outdoor",
    },
    {
        "name": "网红 - 电车通勤 (Train Commute)",
        "prompt": "{prompt}, standing in japanese train, holding hand strap, window reflection, blurred scenery moving outside, rush hour but focused on subject, melancholic urban vibe, cinematic color grading",
        "negative_prompt": "empty train, fantasy, medieval, studio",
    },
    {
        "name": "网红 - 居酒屋 (Izakaya Night)",
        "prompt": "{prompt}, holding a glass of beer or highball, izakaya background with red lanterns, wooden interior, lively atmosphere, blurred customers, tipsy blush, warm yellow lighting",
        "negative_prompt": "fancy restaurant, western food, morning, sterile",
    },
    {
        "name": "网红 - 机场出发 (Airport Travel)",
        "prompt": "{prompt}, sitting on suitcase, airport terminal background, holding passport and ticket, departure board, travel fashion, wide angle, excitement for trip, clean modern architecture",
        "negative_prompt": "home, messy, dirty, old",
    },
    {
        "name": "网红 - 楼顶天台 (Rooftop View)",
        "prompt": "{prompt}, standing on building rooftop, leaning on railing, city skyline in background, blue hour (twilight), wind in hair, urban melancholy, cinematic wide shot",
        "negative_prompt": "ground level, indoor, forest, claustrophobic",
    },
    {
        "name": "网红 - 雨天撑伞 (Rainy Day)",
        "prompt": "{prompt}, holding a clear plastic umbrella, rain falling, wet asphalt street reflecting neon lights, transparent raincoat, moody atmosphere, blade runner vibe but casual",
        "negative_prompt": "sunny, dry, desert, happy bright",
    },
    {
        "name": "网红 - 被窝私房 (Cozy Bedroom)",
        "prompt": "{prompt}, wrapped in fluffy blanket, only face and shoulders visible, cozy bedroom at night, fairy lights in background, warm color palette, intimate girlfriend POV, soft focus",
        "negative_prompt": "cold, outdoor, public place, sharp",
    },
    {
        "name": "网红 - 撸猫/狗 (Pet Lover)",
        "prompt": "{prompt}, holding a cute cat or dog close to face, home living room background, natural smile, soft window light, wholesome vibe, authentic texture",
        "negative_prompt": "scary animal, zoo, outdoor, studio",
    },
]


class StyleSelectorNodeZhex:
    """
    一个自定义节点，它提供一个下拉菜单来选择一个风格，
    并将输入的文本应用到所选风格的提示词模板中。
    当 "random_style" 开启时，每次生成都会自动随机选择一个新风格。
    """

    style_names = [style["name"] for style in style_list]

    @classmethod
    def INPUT_TYPES(cls):
        """
        定义节点的输入。
        我们不再需要 seed 输入框了。
        """
        return {
            "required": {
                "prompt1": ("STRING", {"multiline": True, "default": "一个可爱日本女团成员,圆脸,软软的面颊,婴儿肥,可爱,柔和五官,无辜感,淡妆,微胖的脸"}),
                "prompt2": ("STRING", {"multiline": True, "default": ""}),
                "style_name": (cls.style_names,),
                "random_style": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive_prompt", "negative_prompt")
    FUNCTION = "apply_style"
    CATEGORY = "Utilities/Text"

    @classmethod
    def IS_CHANGED(cls, prompt1, prompt2, style_name, random_style):
        """
        这个方法是实现自动随机的关键。
        """
        if random_style:
            # 如果随机开关打开，我们返回一个纳秒级的时间戳。
            # 这个值每次都保证是不同的，从而强制ComfyUI重新运行此节点。
            return time.time_ns()
        else:
            # 如果随机开关关闭，我们返回一个固定的值。
            # 这样ComfyUI就可以正常使用缓存。
            return None

    def apply_style(
        self, prompt1, prompt2, style_name, random_style
    ):  # 不再需要 seed 参数
        """
        节点的核心逻辑。
        """
        prompt = prompt1 + prompt2
        selected_style = None

        if random_style:
            # 过滤掉 '(None)' 风格
            eligible_styles = [s for s in style_list if s["name"] != "(None)"]

            if not eligible_styles:
                selected_style = next(
                    (style for style in style_list if style["name"] == "(None)"), None
                )
            else:
                selected_style = random.choice(eligible_styles)

            if selected_style:
                # 在控制台打印，方便调试和确认
                print(
                    f"[StyleSelectorNode] Auto-randomly selected style: {selected_style['name']}"
                )

        else:
            # 如果不使用随机，则执行原始逻辑
            selected_style = next(
                (style for style in style_list if style["name"] == style_name), None
            )

        if selected_style:
            prompt_template = selected_style["prompt"]
            negative_prompt_template = selected_style["negative_prompt"]

            positive_prompt_out = prompt_template.replace("{prompt}", prompt)
            negative_prompt_out = negative_prompt_template.replace("{prompt}", prompt)

            return (positive_prompt_out, negative_prompt_out)
        else:
            return (prompt, "")


# -----------------------------------------------------------------
#  ComfyUI 必须的映射字典
#  这告诉ComfyUI如何加载和显示这个节点
# -----------------------------------------------------------------
NODE_CLASS_MAPPINGS = {"StyleSelectorNodeZhex": StyleSelectorNodeZhex}

NODE_DISPLAY_NAME_MAPPINGS = {"StyleSelectorNodeZhex": "风格选择器扩展版"}
