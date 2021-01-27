# 1.project ATA - combination testing

## Verzia pred Ambiguity review:

Pokud je požadováno přemístění nákladu z jednoho místa do druhého, vozík si
náklad vyzvedne do 1 minuty. Pokud se to nestihne, nákladu se nastavuje prioritní
vlastnost. Každý prioritní náklad musí být vyzvednutý vozíkem do 1 minuty od
nastavení prioritního požadavku. Pokud vozík nakládá prioritní náklad, přepíná
se do režimu pouze-vykládka. V tomto režimu zůstává, dokud nevyloží všechen
takový náklad. Normálně vozík během své jízdy může nabírat a vykládat další
náklady v jiných zastávkách. Na jednom místě může vozík akceptovat nebo
vyložit jeden i více nákladů. Pořadí vyzvednutí nákladů nesouvisí s pořadím
vytváření požadavků. Vozík neakceptuje náklad, pokud jsou všechny jeho sloty
obsazené nebo by jeho převzetím byla překročena maximální nosnost.

---

Pokud vozík nakládá prioritní náklad, přepíná se do režimu pouze-vykládka.

- v prípade ak vozík nakladá prioritní náklad, tak by sa mal vozík prepnúť do režimu pouze-nakládka.
- zároveň čo s režimom výkladka a v prípade ak vozík neobsluhuje? 

Pokud vozík nakládá prioritní náklad, přepíná se do režimu pouze-nakládka.

---

V tomto režimu zůstává, dokud nevyloží všechen takový náklad.

- principiálne totožná chyba. nevyloží -> nenaloží

V tomto režimu zůstává, dokud nenaloží všechen takový náklad.

---

Normálně vozík během své jízdy může nabírat a vykládat další náklady v jiných zastávkách.

- gramatický detail

Vozík během své jízdy může nabírat a vykládat další náklady v jiných zastávkách.

---

Na jednom místě může vozík akceptovat nebo vyložit jeden i více nákladů.

- vo vete chýba obmedzujúca podmienka

Na jednom místě může vozík akceptovat nebo vyložit jeden i více nákladů až dokud nejsou vyčerpány všechny sloty.

---

Vozík neakceptuje náklad, pokud jsou všechny jeho sloty obsazené nebo by jeho převzetím byla překročena maximální nosnost.

- nejasnosť - Neakceptuje náklad v akom čase? Je nutné prísť k tomu nákladu? Kde príde ku odmietnutiu?

Vozík neakceptuje náklad v dobe zadania požiadavku, pokud jsou všechny jeho sloty obsazené nebo by jeho převzetím byla překročena maximální nosnost.

---

##Verzia po Ambiguity review:

Pokud je požadováno přemístění nákladu z jednoho místa do druhého, vozík si
náklad vyzvedne do 1 minuty. Pokud se to nestihne, nákladu se nastavuje prioritní
vlastnost. Každý prioritní náklad musí být vyzvednutý vozíkem do 1 minuty od
nastavení prioritního požadavku. Pokud vozík nakládá prioritní náklad, přepíná 
se do režimu pouze-nakládka. V tomto režimu zůstává, dokud nenaloží všechen 
takový náklad. Vozík během své jízdy může nabírat a vykládat další náklady v
jiných zastávkách. Na jednom místě může vozík akceptovat nebo vyložit jeden i více 
nákladů dokud nejsou vyčerpány všechny sloty. Pořadí vyzvednutí nákladů nesouvisí s pořadím
vytváření požadavků. Vozík neakceptuje náklad v dobe zadania požiadavku, pokud jsou všechny jeho sloty
obsazené nebo by jeho převzetím byla překročena maximální nosnost.