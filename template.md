---
papersize: a4
title: "{{title}}"
author: "{{author}} @ {{ip}}"
date: "{{date}} 电"
geometry: margin=2cm
mainfont: Sarasa UI SC

header-includes: |
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhead[C]{{{title}}}
    \fancyhead[L]{{{author}}}
    \fancyhead[R]{{{date}} 电}
    

# mainfontoptions:
# - BoldFont=Sarasa UI SC
# - ItalicFont=Font-Italic.otf
# - BoldItalicFont=Font-BoldItalic.otf
---

{{body}}