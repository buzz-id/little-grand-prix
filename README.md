# Little Grand Prix

A one-page web app with a racing theme that teaches numbers, addition, English and Chinese (中文) to 5 year olds.

- **Daily races:** three a day, Numbers, English and 中文. Each has 4 short laps and wins a trophy for the 7-day trophy cabinet. The same date and class always give the same race.
  - **Numbers:** count the cars, which garage has more, add red cars and blue cars, find the missing number.
  - **English:** find the letter you hear, which letter a word starts with, match big and small letters (Pro: read a short word like "cat"), find a sight word.
  - **中文:** Chinese numbers, picture to word, listen and pick, car colours (红色, 蓝色 …). Pinyin is shown under every word.
- **The Grand Prix:** a 10-lap game after five start lights. There is no clock. Wrong answers fade and never cost points, missed questions come back once, and every race ends on the podium with 1 to 3 stars.
- **The garage:** free play. Add cars on two ten-frames, an ABC board and a 汉字 board. Tap anything to hear it.
- **Classes:** Kart (numbers to 5, capital letters), Junior (to 10, small letters), Pro (to 20, adding across ten, short words, two-character Chinese words).

## Run it

Open `index.html` in any browser. There is no build step and no server.
It loads fonts from Google Fonts (Racing Sans One, Fredoka, Nunito, Andika, Noto Sans SC) and falls back to system fonts when offline.

## Online and on the home screen

The site is published with GitHub Pages at <https://buzz-id.github.io/little-grand-prix/> (Settings → Pages → Deploy from a branch → `main`, `/ (root)`).

To install it like an app:
- **iPad / iPhone (Safari):** Share → Add to Home Screen.
- **Android (Chrome):** menu ⋮ → Add to Home screen / Install app.
- **Windows (Edge or Chrome):** the install icon in the address bar.

It opens full screen with the race car icon and the name "Grand Prix". The icon is drawn in `icons/icon.svg`; the PNG sizes next to it are rendered from that file.
It still needs the internet the first time it opens each session, for the fonts and the page itself.

## Sound

Questions are read aloud with the browser's built-in speech (Web Speech API): English for instructions and Mandarin for Chinese words.
Which voices exist depends on the device. Microsoft Edge, Chrome, and iPad/iPhone Safari usually have both.
On Windows without a Mandarin voice, add Chinese (Simplified) under Settings, Time & Language, Speech.
The grown-ups section shows which voices the app found. Without a voice, every question still works as text, with the letter, word or pinyin shown on screen.

Trophies, the streak and best stars are saved in the browser's `localStorage`, on that device only.
