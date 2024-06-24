Root Github repo of the Personal Primer project, a book-like artefact inspired by Stephenson's Young Lady's Illustrated Primer implementing concept of Human-Machine Peer Learning ( https://www.frontiersin.org/articles/10.3389/feduc.2023.1063337/full ).

# Getting started
* Get hardware (e.g. Raspberry Pi Zero, e-ink screen etc.) listed in https://www.isca-archive.org/interspeech_2023/hromada23_interspeech.html
* git clone https://github.com/hromi/personal_Primer
* pip3 install -r requirements.txt
* copy config.yaml to primer.yaml and adapt to Your needs
* python3 start.py LESSON_URL

# Lesson sources
The canonic source of lessons is currently https://fibel.digital . There is a special template called index.json which generates the lessons for Your artefact. Run start.py with https://fibel.digital/Curriculum/deutsche%20Sprache/Silben/blau/index.json command line argument to install the most simple syllable lesson.
# AI & Human-Machine Peer Learning
For more advanced functionalities like voice identification or speech recognition, it is recommended to have https://github.com/hromi/primer-backend installed on some NVIDIA Jetson or so...
