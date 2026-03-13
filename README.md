# 🎬 YouTube Telegram Bot

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python" alt="Python 3.14">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram Bot">
  <img src="https://img.shields.io/badge/YouTube-API-FF0000?style=for-the-badge&logo=youtube" alt="YouTube API">
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render" alt="Deployed on Render">
  <img src="https://img.shields.io/badge/Version-3.0-success?style=for-the-badge" alt="Version 3.0">
</div>

<p align="center">
  <b>🤖 بوت تلجرام احترافي لاستخراج جميع روابط وعناوين الفيديوهات من يوتيوب</b>
</p>

<p align="center">
  <b>📌 البوت المباشر:</b> <a href="https://t.me/YouTube_Playlist_Extractor_bot">@YouTube_Playlist_Extractor_bot</a>
</p>

---

## ✨ المميزات

- ✅ **استخراج جميع روابط قوائم التشغيل** مهما كان حجمها
- ✅ **جلب جميع فيديوهات أي قناة** (حتى 20,000 فيديو!)
- ✅ **عرض عناوين الفيديوهات** مع الروابط بشكل مرتب
- ✅ **إرسال ملف نصي منظم** بجميع البيانات
- ✅ **دعم كامل للغة العربية** والأحرف الخاصة
- ✅ **معالجة سريعة** للقوائم الضخمة

---

## 📋 الأوامر المتاحة

| الأمر | الوصف |
|-------|-------|
| `/start` | بدء استخدام البوت وعرض التعليمات |
| `/help` | عرض المساعدة والأوامر المتاحة |
| `/about` | معلومات عن البوت والمطور |
| `/channel @username` | استخراج جميع فيديوهات قناة |

---

## 🚀 طريقة الاستخدام

### لقائمة تشغيل:
```
أرسل رابط القائمة مباشرة:
https://youtube.com/playlist?list=PLi_EiiLGa6lO4DZ2mSZax00FsN2J9M3hp
```

### لقناة يوتيوب:
```
أرسل اسم القناة مع @:
@AlJazeera
```
أو استخدم الأمر المباشر:
```
/channel @AlJazeera
```

---

## 🛠️ التقنيات المستخدمة

- **لغة البرمجة:** Python 3.14
- **المكتبات الرئيسية:**
  - `google-api-python-client` - للتعامل مع YouTube API
  - `python-telegram-bot` - للتفاعل مع تلجرام
- **الاستضافة:** Render (Web Service)
- **إدارة الحالة:** UptimeRobot للحفاظ على نشاط البوت

---

## 📦 متطلبات التثبيت (requirements.txt)

```txt
google-api-python-client
python-telegram-bot
```

---

## 🔧 التثبيت والتشغيل المحلي

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. إعداد المفاتيح
- احصل على مفتاح YouTube API من [Google Cloud Console](https://console.cloud.google.com)
- احصل على توكن بوت من [@BotFather](https://t.me/botfather)

### 3. تشغيل البوت محلياً
```bash
python telegram_bot.py
```

---

## 🌐 النشر على Render

1. ارفع المشروع على GitHub
2. أنشئ Web Service جديد على [Render](https://render.com)
3. اربط المستودع
4. أضف المتغيرات البيئية:
   - `TELEGRAM_TOKEN`
   - `YOUTUBE_API_KEY`
5. أمر التشغيل: `python telegram_bot.py`
6. شغّل الخدمة

---

## 👨‍💻 المطور

- **الاسم:** Ebrahim Alshabany
- **البريد الإلكتروني:** central.app.ye@gmail.com
- **إنستغرام:** [@ebrahim_alshabany](https://www.instagram.com/ebrahim_alshabany?igsh=MXRtOTN1bnpibHozNA==)
- **البوت المباشر:** [@YouTube_Playlist_Extractor_bot](https://t.me/YouTube_Playlist_Extractor_bot)

---

## 📱 تابعني على إنستغرام

[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/ebrahim_alshabany?igsh=MXRtOTN1bnpibHozNA==)

---

## 🤝 المساهمة في المشروع

نرحب بمساهماتكم! للمساهمة:

1. Fork المشروع
2. أنشئ فرعاً جديداً (`git checkout -b feature/AmazingFeature`)
3. commit التغييرات (`git commit -m 'إضافة ميزة جديدة'`)
4. Push إلى الفرع (`git push origin feature/AmazingFeature`)
5. افتح Pull Request

---

## 📜 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

<div align="center">
  <b>⭐ إذا أعجبك المشروع، لا تنسى وضع نجمة على GitHub! ⭐</b>
  <br><br>
  <b>🚀 تم التطوير بواسطة Ebrahim Alshabany | 2026</b>
  <br>
  <b>📧 central.app.ye@gmail.com</b>
  <br>
  <b>🤖 @YouTube_Playlist_Extractor_bot</b>
</div>

