# -*- coding: utf-8 -*-
import os
import logging
import googleapiclient.discovery
import urllib.parse
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- تم وضع التوكن الجديد هنا ---
TELEGRAM_TOKEN = '8501521808:AAGzyCcrcFF4iKKUC--meWT_GKVT_s0s26M'  # ✅ التوكن الجديد
YOUTUBE_API_KEY = 'AIzaSyDbSRy8bF22VMmvytE1Z2qFJDu2e-RRBrU'  # مفتاح يوتيوب الخاص بك

# إعدادات logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة استخراج روابط وعناوين قائمة التشغيل
async def get_playlist_videos(playlist_id):
    """دالة لجلب روابط وعناوين جميع الفيديوهات من معرف قائمة التشغيل."""
    
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', 
        developerKey=YOUTUBE_API_KEY)

    videos = []  # قائمة تحتوي على tuples (العنوان, الرابط)
    next_page_token = None

    try:
        while True:
            request = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                videos.append((video_title, video_url))

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos, None
    except Exception as e:
        return None, str(e)

# دالة استخراج روابط وعناوين قناة كاملة
async def get_channel_videos(channel_username):
    """دالة لجلب روابط وعناوين جميع فيديوهات قناة يوتيوب."""
    
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', 
        developerKey=YOUTUBE_API_KEY)

    try:
        # الخطوة 1: البحث عن معرف القناة باستخدام اسم المستخدم
        if channel_username.startswith('@'):
            channel_username = channel_username[1:]  # إزالة @
        
        channels_response = youtube.search().list(
            part='snippet',
            q=channel_username,
            type='channel',
            maxResults=1
        ).execute()
        
        if not channels_response['items']:
            return None, "لم أتمكن من العثور على القناة. تأكد من اسم المستخدم."
        
        channel_id = channels_response['items'][0]['snippet']['channelId']
        channel_title = channels_response['items'][0]['snippet']['title']
        
        # الخطوة 2: الحصول على قائمة تشغيل الرفع (Uploads) الخاصة بالقناة
        channels_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        
        uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # الخطوة 3: جلب جميع الفيديوهات من قائمة تشغيل الرفع
        videos = []
        next_page_token = None
        
        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_title = item['snippet']['title']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                videos.append((video_title, video_url))
            
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos, channel_title, None
        
    except Exception as e:
        return None, None, str(e)

# أمر /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ترحيب بالمستخدم وإرسال التعليمات"""
    welcome_message = (
        "🎬 **مرحباً بك في بوت استخراج روابط قوائم يوتيوب المطور!**\n\n"
        "📌 **الأوامر المتاحة:**\n"
        "🔹 أرسل **رابط قائمة تشغيل** لاستخراج روابطها\n"
        "🔹 أرسل **@username** لاستخراج جميع فيديوهات قناة\n"
        "🔹 `/channel @username` لاستخراج فيديوهات قناة\n\n"
        "✅ **أمثلة:**\n"
        "`https://youtube.com/playlist?list=PLi_EiiLGa6lO4DZ2mSZax00FsN2J9M3hp`\n"
        "`@MohamedHamed`\n"
        "`/channel @AlJazeeraChannel`\n\n"
        "🚀 أرسل الرابط أو اسم القناة وسأبدأ العمل!"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

# أمر /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال تعليمات المساعدة"""
    help_message = (
        "🆘 **المساعدة**\n\n"
        "**استخراج قائمة تشغيل:**\n"
        "• أرسل رابط قائمة التشغيل مباشرة\n\n"
        "**استخراج قناة كاملة:**\n"
        "• أرسل اسم القناة مع @ (مثال: `@AlJazeera`)\n"
        "• أو استخدم الأمر `/channel @username`\n\n"
        "⚡ **ملاحظة:** القوائم الكبيرة جداً قد تستغرق وقتاً أطول."
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')

# أمر /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إرسال معلومات عن البوت"""
    about_message = (
        "🔴 **بوت استخراج روابط يوتيوب** 🔴\n\n"
        "🎬 بوت احترافي لاستخراج جميع روابط وعناوين الفيديوهات من يوتيوب!\n\n"
        "✅ **المميزات:**\n"
        "• استخراج جميع روابط أي قائمة تشغيل\n"
        "• جلب كل فيديوهات أي قناة (حتى 20,000 فيديو!)\n"
        "• عرض عناوين الفيديوهات مع الروابط\n"
        "• إرسال ملف نصي منظم بجميع البيانات\n\n"
        "📌 **طريقة الاستخدام:**\n"
        "• لقائمة تشغيل: أرسل الرابط\n"
        "• لقناة: أرسل @اسم_القناة\n"
        "• مثال: @AlJazeera\n\n"
        "👨‍💻 **برمجة وتطوير:** Ibrahim alshabany\n\n"
        "📋 **الأوامر:**\n"
        "/start - بدء الاستخدام\n"
        "/help - المساعدة\n"
        "/about - معلومات عن البوت\n\n"
        "⚡ جربه الآن!"
    )
    await update.message.reply_text(about_message, parse_mode='Markdown')

# أمر /channel
async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر استخراج فيديوهات قناة"""
    
    # التحقق من وجود اسم القناة
    if not context.args:
        await update.message.reply_text(
            "❌ الرجاء إدخال اسم القناة.\n"
            "مثال: `/channel @AlJazeeraChannel`"
        )
        return
    
    channel_input = context.args[0]
    
    # إظهار أن البوت يكتب
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # إرسال رسالة "جاري المعالجة"
    processing_msg = await update.message.reply_text(f"⏳ جاري جلب فيديوهات القناة {channel_input}...\nهذا قد يستغرق دقيقة أو أكثر...")
    
    try:
        # جلب الفيديوهات
        videos, channel_title, error = await get_channel_videos(channel_input)
        
        if error:
            await processing_msg.edit_text(f"❌ حدث خطأ: {error}")
            return
        
        if not videos:
            await processing_msg.edit_text("❌ لم يتم العثور على فيديوهات في هذه القناة.")
            return
        
        # تجهيز الرد
        num_videos = len(videos)
        
        # إرسال ملخص
        summary = f"✅ **{channel_title}**\n"
        summary += f"📊 تم العثور على **{num_videos} فيديو** في القناة.\n\n"
        summary += "📌 **أحدث 5 فيديوهات:**\n"
        
        for i, (title, url) in enumerate(videos[:5], 1):
            # تقصير العنوان إذا كان طويلاً
            short_title = title[:50] + "..." if len(title) > 50 else title
            summary += f"{i}. [{short_title}]({url})\n"
        
        await processing_msg.edit_text(summary, parse_mode='Markdown')
        
        # إنشاء ملف نصي وإرساله (دائماً)
        file_content = f"قناة: {channel_title}\n"
        file_content += f"عدد الفيديوهات: {num_videos}\n"
        file_content += "=" * 50 + "\n\n"
        
        for i, (title, url) in enumerate(videos, 1):
            file_content += f"{i}. {title}\n   {url}\n\n"
        
        filename = f"channel_{channel_input.replace('@', '')[:20]}.txt"
        
        with open(filename, "w", encoding='utf-8') as f:
            f.write(file_content)
        
        with open(filename, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=filename,
                caption=f"📥 ملف يحتوي على {num_videos} فيديو من قناة {channel_title}"
            )
        
        # حذف الملف المؤقت
        os.remove(filename)
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ حدث خطأ غير متوقع: {str(e)}")
        logger.error(f"Error: {e}")

# معالجة الرسائل النصية
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة رسالة المستخدم"""
    
    # إظهار أن البوت يكتب
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # الحصول على نص الرسالة
    message_text = update.message.text.strip()
    
    # التحقق إذا كان رسالة قناة (تبدأ بـ @)
    if message_text.startswith('@'):
        # استخراج فيديوهات قناة
        processing_msg = await update.message.reply_text(f"⏳ جاري جلب فيديوهات القناة {message_text}...\nهذا قد يستغرق دقيقة أو أكثر...")
        
        try:
            videos, channel_title, error = await get_channel_videos(message_text)
            
            if error:
                await processing_msg.edit_text(f"❌ حدث خطأ: {error}")
                return
            
            if not videos:
                await processing_msg.edit_text("❌ لم يتم العثور على فيديوهات في هذه القناة.")
                return
            
            num_videos = len(videos)
            
            summary = f"✅ **{channel_title}**\n"
            summary += f"📊 تم العثور على **{num_videos} فيديو**.\n\n"
            summary += "📌 **أحدث 5 فيديوهات:**\n"
            
            for i, (title, url) in enumerate(videos[:5], 1):
                short_title = title[:50] + "..." if len(title) > 50 else title
                summary += f"{i}. [{short_title}]({url})\n"
            
            await processing_msg.edit_text(summary, parse_mode='Markdown')
            
            # إنشاء ملف نصي وإرساله (دائماً)
            file_content = f"قناة: {channel_title}\n"
            file_content += f"عدد الفيديوهات: {num_videos}\n"
            file_content += "=" * 50 + "\n\n"
            
            for i, (title, url) in enumerate(videos, 1):
                file_content += f"{i}. {title}\n   {url}\n\n"
            
            filename = f"channel_{message_text.replace('@', '')[:20]}.txt"
            
            with open(filename, "w", encoding='utf-8') as f:
                f.write(file_content)
            
            with open(filename, "rb") as f:
                await update.message.reply_document(
                    document=f,
                    filename=filename,
                    caption=f"📥 ملف يحتوي على {num_videos} فيديو من قناة {channel_title}"
                )
            
            os.remove(filename)
            
        except Exception as e:
            await processing_msg.edit_text(f"❌ حدث خطأ غير متوقع: {str(e)}")
            logger.error(f"Error: {e}")
    
    else:
        # معالجة رابط قائمة التشغيل
        processing_msg = await update.message.reply_text("⏳ جاري معالجة الرابط...")
        
        try:
            parsed_url = urllib.parse.urlparse(message_text)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            playlist_id = query_params.get('list', [None])[0]
            
            if not playlist_id:
                await processing_msg.edit_text(
                    "❌ لم أتمكن من العثور على معرف قائمة التشغيل في الرابط.\n"
                    "تأكد من أن الرابط صحيح (مثال: youtube.com/playlist?list=...)"
                )
                return
            
            await processing_msg.edit_text(f"⏳ جاري جلب روابط القائمة...\nهذا قد يستغرق بضع ثوانٍ...")
            
            # جلب الفيديوهات مع العناوين
            videos, error = await get_playlist_videos(playlist_id)
            
            if error:
                await processing_msg.edit_text(f"❌ حدث خطأ: {error}")
                return
            
            if not videos:
                await processing_msg.edit_text("❌ لم يتم العثور على فيديوهات في هذه القائمة.")
                return
            
            num_videos = len(videos)
            
            # عرض أول 5 فيديوهات (دائماً)
            summary = f"✅ تم العثور على {num_videos} فيديو.\n\n"
            summary += "📊 **أول 5 فيديوهات:**\n"
            for i, (title, url) in enumerate(videos[:5], 1):
                short_title = title[:50] + "..." if len(title) > 50 else title
                summary += f"{i}. [{short_title}]({url})\n"
            
            await processing_msg.edit_text(summary, parse_mode='Markdown')
            
            # إنشاء ملف نصي وإرساله (دائماً، حتى مع 3 روابط)
            file_content = f"قائمة تشغيل: {playlist_id}\n"
            file_content += f"عدد الفيديوهات: {num_videos}\n"
            file_content += "=" * 50 + "\n\n"
            
            for i, (title, url) in enumerate(videos, 1):
                file_content += f"{i}. {title}\n   {url}\n\n"
            
            filename = f"playlist_{playlist_id[:8]}.txt"
            
            with open(filename, "w", encoding='utf-8') as f:
                f.write(file_content)
            
            with open(filename, "rb") as f:
                await update.message.reply_document(
                    document=f,
                    filename=filename,
                    caption=f"📥 ملف يحتوي على {num_videos} فيديو من قائمة التشغيل"
                )
            
            os.remove(filename)
        
        except Exception as e:
            await processing_msg.edit_text(f"❌ حدث خطأ غير متوقع: {str(e)}")
            logger.error(f"Error: {e}")

# الدالة الرئيسية
def main():
    """تشغيل البوت"""
    
    # إنشاء التطبيق
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("channel", channel_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # تشغيل البوت
    print("🤖 البوت المطور يعمل الآن... اضغط Ctrl+C للإيقاف")
    print("✅ الميزات الجديدة:")
    print("   - عرض عناوين الفيديوهات مع الروابط")
    print("   - استخراج فيديوهات قناة كاملة (@username)")
    print("   - إرسال ملف نصي لجميع النتائج (حتى لو كان عدد الفيديوهات قليلاً)")
    print("   - أمر /about مع معلومات عن البوت")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()