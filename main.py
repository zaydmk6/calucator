import telebot
import random
import json
import requests
import datetime
from deep_translator import GoogleTranslator  

BOT_TOKEN = "7366679163:AAF5v6XdSMvi8_OGEua2giZIJxruM3oWTi0"
bot = telebot.TeleBot(BOT_TOKEN)

# قائمة الكلمات المرفوضة
BANNED_WORDS = [
    "كسمك", "كسك", "مص زبي", "كسختك", "ابن الحرام", "ابن الكلب", "ابن القحبة",  
    "يا عرص", "زبي", "شرموط", "منايك", "قحبة", "متناك", "خول", "زامل",  
    "عاهرة", "اللعنة عليك", "اللعنة على اهلك", "حمار", "كلب", "كس امك",  
    "عرص", "متناك ابن المتناك", "يا خرا", "خرا عليك", "كسمك يا ابن المتناك",  
    "قحب", "زبك", "متناك ابن الوسخة", "يلعن شرفك", "يلعن أمك", "ابن المتناكة",  
    "زبي فيك", "على زبي", "يا زب", "يلعن عرضك", "كس امك وام اهلك", "يا قحب",  
    "زب أمك", "نكح أمك", "أخو القحبة", "يلعن دينك", "كسمينك", "يلعن اصلك",  
    "قحباء", "بنت القحبة", "ابن العاهرة", "يا مخنث", "يا لوطي", "منيوك",  
    "يلعن تربيتك", "يا وسخ", "يا نجس", "يا متناك", "يلعن أصلك", "يلعن عرضك",  
    "يا زامل", "أبوك متناك", "أمك شرموطة", "أبوك شرموط", "ابن الوسخة",  
    "زبي في وجهك", "اغتصبك", "كس أختك", "ابن الزنا", "يلعن روحك", "يلعن ميتينك",  
    "حيوان", "يا متخلف", "خنيث", "منحط", "يا ساقط", "يلعن شرف أمك",  
    "يا زبالة", "زبك في عينك", "يلعن أصلك وفصلك", "ابن الشوارع", "يا لقيط",  
    "يا متسول", "يا واطي", "زب أبوك", "يلعن قفاك", "زبي في شرفك",  
    "يا نغل", "يا زفت", "يا تيس", "يا حمار ابن الحمار", "يا ضبع", "يا خنزير",  
    "أمك قحبة", "أبوك عرص", "يا ابن الميتين", "يا جرذ", "يا كلب ابن كلب",  
    "يلعن نسلك", "يلعن تربيتك الوسخة", "قحبة الشارع", "زامل ابن زامل",  
    "ابن المومس", "أمك في الشارع", "يا معرص", "زبي في أهلك", "أمك في الدعارة",  
    "يلعن دمك", "يلعن مذهبك", "يا مقمل", "يا قواد", "يا متعري",  
    "أبوك مشبوه", "أمك عاهرة", "يا صرصور", "يا بعوضة", "يا جرادة", "يا فاشل",  
    "يا مهزوم", "يا بلا أصل", "يا لعين", "يا مقرف", "يا كريه", "يا سافل",  
    "يلعن أصلك يا واطي", "يا منيك", "يا زبي", "ابن الحيونة", "يا زبالة المجتمع",  
    "أنت وصمة عار", "يلعن كرامتك", "انت من سلالة الكلاب", "مخنث", "ناقص رجولة",  
    "يا وغد", "يا غبي", "يا ديوث", "أبوك متخلف", "أمك ناقصة شرف",  
    "يا تافه", "يا حثالة", "زبك في عين أمك", "انت مجرد حشرة",  
    "انت وصمة عار على البشرية", "يا فاشل اجتماعياً", "انت لا شيء",  
    "يا زب أمك", "يا ابن الحرام والحرامية", "أبوك ابن زانية", "يلعن جدك"
]


EXTRA_QUOTES = [
    "و أتمنى مِن الله أن نكون مِن المجبرين قريبًا أن ينتهي تعبنا وتبدأ أيام فرحنا أن يستجب و يقول لأمرنا كن فيكون 🤎.",
    "(وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَى) ويأتيك عوض الله وكأنك لم تخسر شيئًا.",
    "اللهمَّ إني أحسنتُ بكَ الظَّن فاجبُرني 🌷.",
    "الحمد لله الذي لا تُحصى نعمه، ولا يُحجب وجهه، ولا يُستغنى عن فضله...",
    "اللهم بلغنا رمضان ، بلاغ قبول وتوفيق ونحن وجميع أهلنا وأحبتنا في أحسن حال 🤎.",
    "رُبَّما الأسبابُ هُيِّئَت، والجَبرُ قَرِيبٌ ❤️‍🩹.",
    "اللهم بلغنا رمضان ونحن مجبورين 😭"
]

# معالج العبارات
@bot.message_handler(func=lambda message: "عبارات" in message.text.lower())
def send_extra_quotes(message):
    try:
        bot.reply_to(message, random.choice(EXTRA_QUOTES))
    except telebot.apihelper.ApiTelegramException as e:
        print(f"خطأ أثناء إرسال العبارات: {e}")
  
# كلمات رداً على المستخدم
KEYWORDS_RESPONSES = {
    
    "مرحبا": "مرحباً! كيف يمكنني مساعدتك اليوم؟",
    "أنت بخير؟": "نعم، أنا بخير! شكراً لسؤالك 😊",
    "كيف حالك؟": "أنا بخير! شكراً على السؤال 🙏",
    "وداعاً": "وداعاً! أراك لاحقاً 👋"
}

# قائمة الأذكار
ADHKAR = [
    "اللهم اجعلنا من أهل الجنة.",
    "سبحان الله وبحمده، سبحان الله العظيم.",
    "اللهم استرنا فوق الأرض، واسترنا تحت الأرض، واسترنا يوم العرض.",
    "اللهم إني أعوذ بك من شر نفسي ومن شر الشيطان وشركه.",
    "اللهم اجعل القرآن ربيع قلوبنا."
]

# بعض الآيات العشوائية
QURAN_VERSES = [
    "بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ - (الفاتحة 1)",
    "قُلْ هُوَ اللَّهُ أَحَدٌ - (الإخلاص 1)",
    "اللَّهُ لَا إِلٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ - (آل عمران 2)",
    "وَإِنَّكَ لَعَلَىٰ خُلُقٍ عَظِيمٍ - (القلم 4)",
    "وَقُلْ رَبِّ زِدْنِي عِلْمًا - (طه 114)"
]

# مميزات عشوائية
RANDOM_FEATURES = [
    "هل تعلم؟ أن متوسط عمر الإنسان في اليابان هو 84 سنة.",
    "هل تعلم؟ أن دلافين البحر تُعتبر واحدة من أذكى الحيوانات في العالم.",
    "هل تعلم؟ أن الفيل يمكنه أن يعيش حتى 70 عامًا.",
    "هل تعلم؟ أن أول كاميرا فوتوغرافية اخترعت في عام 1816!"
]

# صورة افتراضية عشوائية
AVATAR_IMAGES = [
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/women/4.jpg"
]

# معالج الكلمات المفتاحية
@bot.message_handler(func=lambda message: "اذكار" in message.text.lower())
def send_adhkar(message):
    try:
        bot.reply_to(message, random.choice(ADHKAR))
    except telebot.apihelper.ApiTelegramException as e:
        print(f"خطأ أثناء إرسال الأذكار: {e}")

# معالج آية عشوائية
@bot.message_handler(func=lambda message: "قران" in message.text.lower())
def send_quran(message):
    try:
        bot.reply_to(message, random.choice(QURAN_VERSES))
    except telebot.apihelper.ApiTelegramException as e:
        print(f"خطأ أثناء إرسال الآية: {e}")

# معالج الميزة العشوائية
@bot.message_handler(func=lambda message: "ميزة" in message.text.lower())
def send_random_feature(message):
    try:
        bot.reply_to(message, random.choice(RANDOM_FEATURES))
    except telebot.apihelper.ApiTelegramException as e:
        print(f"خطأ أثناء إرسال الميزة العشوائية: {e}")

{e}")

# معالج صورة عشوائية
@bot.message_handler(func=lambda message: "افتار" in message.text.lower())
def send_avatar(message):
    try:
        bot.send_photo(message.chat.id, random.choice(AVATAR_IMAGES))
    except telebot.apihelper.ApiTelegramException as e:
        print(f"خطأ أثناء إرسال صورة عشوائية: {e}")

# معالج الكلمات المفتاحية الأخرى
@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in KEYWORDS_RESPONSES))
def reply_keywords(message):
    try:
        response = KEYWORDS_RESPONSES.get(message.text.strip(), "عذراً، لم أفهم ما قلته.")
        bot.reply_to(message, response)
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == "Forbidden: bot was blocked by the user":
            print(f"تم حظر البوت من قبل المستخدم: {message.chat.id}")

# معالج إرسال رسائل غير مرغوب فيها
@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in BANNED_WORDS))
def delete_bad_words(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.reply_to(message, "🚫 ممنوع استخدام الألفاظ المسيئة!", parse_mode="Markdown")
    except telebot.apihelper.ApiTelegramException as e:
        if e.result_json['description'] == "Forbidden: bot was blocked by the user":
            print(f"تم حظر البوت من قبل المستخدم: {message.chat.id}")

bot.polling(none_stop=True, interval=0, timeout=20)
