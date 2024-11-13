
     ███╗   ███╗████████╗███████╗██████╗"     
     ████╗ ████║╚══██╔══╝██╔════╝██╔══██╗"     
     ██╔████╔██║   ██║   ███████╗██████╔╝"     
     ██║╚██╔╝██║   ██║   ╚════██║██╔═══╝"     
     ██║ ╚═╝ ██║   ██║   ███████║██║"          
     ╚═╝     ╚═╝   ╚═╝   ╚══════╝╚═╝"          
                                                  
Music Terminal Shell Player


# MTSP (Music Player Application)

![Screenshot](https://github.com/almezali/mtsp/blob/main/Screenshot.png)

## مقدمة
**MTSP** هو برنامج بسيط لتشغيل الموسيقى تم تطويره بلغة Python باستخدام مكتبة Tkinter لواجهة المستخدم الرسومية وPygame للتشغيل الصوتي. يتيح البرنامج تشغيل ملفات الصوت بتنسيقات مثل MP3 وWAV وOGG، مع خيارات للتبديل العشوائي والتكرار.

## الميزات
- تشغيل وإيقاف مؤقت، وتشغيل الصوتيات من قائمة تشغيل.
- التحكم في مستوى الصوت.
- دعم ميزة التبديل العشوائي والتكرار.
- إضافة ملفات وقوائم تشغيل.
- يعمل على أنظمة لينكس، ويندوز، وماك.

## المتطلبات
### Linux (مثل Arch Linux وFedora وUbuntu)
1. Python 3.6 أو أحدث
2. مكتبة Tkinter (غالباً تكون مثبتة مع Python، إذا لم تكن مثبتة يمكن تثبيتها كما يلي):
   - Arch Linux:
     ```bash
     sudo pacman -S tk python-pygame
     ```
   - Ubuntu/Debian:
     ```bash
     sudo apt install python3-tk python3-pygame
     ```
   - Fedora:
     ```bash
     sudo dnf install python3-tkinter python3-pygame
     ```

### Windows
1. قم بتنزيل وتثبيت [Python](https://www.python.org/downloads/) مع اختيار خيار "Add Python to PATH" أثناء التثبيت.
2. تثبيت مكتبة Pygame باستخدام الأمر:
   ```bash
   pip install pygame

