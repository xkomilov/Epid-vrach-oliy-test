# Savol yozish bo'yicha yo'riqnoma (agentlar uchun)

Siz tibbiyot oliygohi o'qituvchisi va test tuzuvchisisiz. Mavzu materiallari: `/projects/sandbox/work2/txt/NNN.txt` (o'zbek lotin yozuvida; oxirida "Foydalanilgan adabiyotlar" ro'yxati bor, matn ichida [n] havolalar).
Natija: `/projects/sandbox/work2/q/NNN.txt` — har mavzu uchun bitta fayl, **12 ta savol** (kamida 10 bo'lishi shart). Savollar o'zbek tilida (lotin) yoziladi.

## Fayl formati (aynan shunday)

```
=== 001
? Savol matni
+ To'g'ri javob
- Noto'g'ri 1
- Noto'g'ri 2
- Noto'g'ri 3
- Noto'g'ri 4
! Qisqa ilmiy izoh (1–2 gap, nuqta bilan tugasin)
@ Manba1; Manba2
? Keyingi savol...
#D 001 / <savol raqami>: mavzu materiali rasmiy manbadan farq qilgan joy (bo'lsa)
#U 001 / <savol raqami>: faqat mavzu materialiga tayangan, tashqi manba bilan tasdiqlanmagan fakt (bo'lsa)
```
- Har qator bitta qatorda. Savol bloki: `?`, `+`, aynan 4 ta `-`, `!`, `@`.
- Savol ichida mavzu nomini/raqamini YOZMANG ("001-mavzuda..." kabi yozuvlar yo'q).
- `+` javobni oxirida nuqta qo'ymasdan yozing (skript o'zi qo'yadi).
- `!` izohda "To'g'ri javob:" va "Manba:" so'zlarini yozmang — skript qo'shadi. Izoh to'g'ri javob matnini takrorlamasin, sababini tushuntirsin.
- `@`: qisqa, aniq manba nomlari, nuqta-vergul bilan. FAQAT mavzu fayli oxiridagi "Foydalanilgan adabiyotlar" ro'yxatidagi manbalardan (masalan "WHO. ... (2019)", "CDC. Principles of Epidemiology (SS1978), Lesson 1") yoki ishonchli, o'zingiz aniq biladigan rasmiy hujjatlardan (JSST, CDC, SanPiN/MU/MUK, O'zR SSV buyruqlari) foydalaning — hujjat raqami yoki yilini o'ylab topmang. Agar fakt faqat mavzu materialida bo'lsa: `Mavzu materiali (NNN.docx)` deb yozing va shu faktni `#U` qatoriga qo'shing.
- Mavzu materialida yo'q, tasdiqlanmagan fakt to'qib chiqarmang. Material rasmiy manbadan farq qilsa — `#D` qatori.

## Mazmun
- Mavzuning turli qismlarini qamrang: ta'rif, qo'zg'atuvchi, yuqish, klinika, laboratoriya usullari, me'yor va raqamlar (muddatlar, dozalar, haroratlar, konsentratsiyalar), hisob-kitob (agar mos bo'lsa), profilaktika, o'choqdagi tadbirlar, hujjatlar/vazifalar.
- Savol bitta aniq to'g'ri javobli bo'lsin. Noto'g'ri javoblar ishonarli, lekin aniq noto'g'ri (boshqa kasallik/qo'zg'atuvchi, boshqa usul, boshqa raqam, yaqin tushunchalar). Ikki ma'noli yoki munozarali variant bo'lmasin. "Yuqoridagilarning barchasi", "hech biri" kabi variantlar yo'q.
- Barcha 5 variant savolga grammatik mos bo'lsin (to'g'ri javob grammatik jihatdan yagona mos variant bo'lib qolmasin).
- To'g'ri javobni O'ZINGIZ joylashtirish tartibi haqida o'ylamang — skript aralashtiradi. Faqat `+` ni birinchi, `-` larni keyin yozing.

## Variantlar sifati (SKRIPT TEKSHIRADI)
1. To'g'ri javob belgilar soni eng uzun noto'g'ri javobdan 10 % dan ko'p uzun bo'lmasin (ya'ni len(+) <= 1.10 × max(len(-))). Eng ishonchli yo'l: noto'g'ri javoblardan kamida bittasini to'g'ri javobdek (yoki undan uzunroq) batafsil yozing. To'g'ri javob tafsiloti, qavsdagi izohi yoki "va ..." qo'shimchasi bilan ajralib qolmasin — noto'g'ri javoblar ham xuddi shunday batafsil bo'lsin.
2. "Faqat…", "Hech qachon…", "Umuman…", "Barcha…" bilan boshlanuvchi noto'g'ri javob bir savolda ko'pi bilan 1 ta.
3. 3 yoki undan ko'p noto'g'ri javob bir xil so'z bilan boshlanmasin (to'g'ri javob ham shu so'z bilan boshlansa — ruxsat). Raqamli/formulali savollarda bir xil tuzilish ruxsat etiladi (lekin bunda ham boshlanish so'zi bir xil 3 ta bo'lsa skript bayroq qo'yadi — iloji boricha so'z tartibini o'zgartiring).
4. Variantlar bir-biridan takrorlanmasin.

## Tekshirish
Yozib bo'lgach: `cd /projects/sandbox/work2 && python3 build.py --check | grep -E "^(NNN|MMM)"` (o'z mavzu raqamlaringiz bilan). Bayroqlangan savollarni tuzating, bayroq qolmaguncha takrorlang. (Skript hamma fayllarni tekshiradi; faqat o'zingizniki bilan ishlang. `out/` papkasiga tegmang.)
