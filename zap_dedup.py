import anthropic
import pandas as pd
import json

# -------------------------------------------------------
# 1. דאטה סינתטי — רשימת מוצרים עם כפילויות
# -------------------------------------------------------
raw_data = [
    {"name": "Samsung Galaxy S23 256GB 8GB RAM 5G",         "price": 2990},
    {"name": "סמסונג גלקסי S23 256GB 8GB RAM 5G יבואן רשמי","price": 3100},
    {"name": "Samsung S23 256GB 8GB 5G במבצע!",             "price": 2850},
    {"name": "Samsung Galaxy S23 128GB 8GB RAM 5G",         "price": 2500},
    {"name": "iPhone 15 128GB",                             "price": 3500},
    {"name": "אייפון 15 128GB משלוח חינם",                  "price": 3600},
    {"name": "iPhone 15 256GB",                             "price": 3900},
    {"name": "Samsung Galaxy S23 256GB 8GB RAM 4G",         "price": 2700},  # 4G — מוצר שונה!
    {"name": "",                                            "price": None},  # שורה ריקה
    {"name": "Xiaomi Redmi Note 12 128GB 6GB RAM 5G",       "price": 1200},
    {"name": "שיאומי רדמי נוט 12 128GB 6GB RAM 5G חדש!",   "price": 1250},
]

# -------------------------------------------------------
# 2. הפרומפט שכתבתי
# -------------------------------------------------------
PROMPT = """
אתה עובד בחברת ZAP בתור מומחה נתונים ל-Ecommerce וקיבלת רשימה של מוצרים עם כפילויות ושמות לא אחידים.
המטרה ותפקידך היא להחזיר קובץ מסכם שמאחד את הכפילויות ומחזיר רשימה עם המחיר המינימלי לכל מוצר ללקוח.
המשימה תתבצע בכמה שלבים:

1. ניקוי נתונים
תסקור ותקרא את הנתונים בקובץ הנתון, תמחק שורות ריקות שלא מצורף להן דאטה ותבצע DATA Cleaning.

2. זיהוי מוצרים זהים
מוצר יהיה זהה רק אם כל הפרמטרים המגדירים אותו מתאימים ולא שונים:
- דגם: למשל Samsung S23 ו-סמסונג גלקסי 23 — מוצר שונה, לא אותו מוצר.
- מפרט טכני ליבתי:
  - נפח אחסון: 128GB לעומת 256GB — לא אותו מוצר.
  - זיכרון RAM: 8GB לעומת 12GB — לא אותו מוצר.
  - דור תקשורת: 4G לעומת 5G — לא אותו מוצר.
- מותג: Samsung לעומת Apple — מוצר שונה (הבדל שפה במותג אינו הבדל).

3. סינון רעשים
התעלם מגורמים שאינם משנים את זהות המוצר:
- שפה: עברית לעומת אנגלית — אותו מוצר.
- שם היבואן: "יבואן רשמי" לעומת "סל-קומיוניקיישן" — אותו מכשיר, רק המוכר שונה.
- תיאורים שיווקיים: "במבצע!", "חדש!", "משלוח חינם", "מבצע לחג".
- צבע: התעלם אלא אם הצבעים שונים משמעותית.

4. פורמט הפלט
החזר JSON בלבד (ללא טקסט נוסף) במבנה הבא:
[
  {
    "product_name": "שם מנורמל באנגלית",
    "brand": "מותג",
    "storage": "נפח אחסון",
    "ram": "זיכרון RAM",
    "generation": "דור תקשורת",
    "min_price": מחיר מינימלי כמספר,
    "occurrences": מספר הופעות כמספר
  }
]
מיין את הרשימה מהמחיר הנמוך לגבוה.
אם אינך בטוח אם שני מוצרים זהים — השאר אותם נפרדים.

הנה רשימת המוצרים:
{products}
"""

# -------------------------------------------------------
# 3. שליחה ל-Claude API
# -------------------------------------------------------
def run_dedup(products: list) -> list:
    client = anthropic.Anthropic()  # קורא ANTHROPIC_API_KEY מה-environment

    products_str = json.dumps(products, ensure_ascii=False, indent=2)
    prompt = PROMPT.format(products=products_str)

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    result = json.loads(response_text)
    return result

# -------------------------------------------------------
# 4. שמירה כקובץ Excel
# -------------------------------------------------------
def save_to_excel(data: list, filename: str = "zap_products_summary.xlsx"):
    df = pd.DataFrame(data)

    # עיצוב עמודת מחיר
    df["min_price"] = df["min_price"].apply(lambda x: f"{x:,} ₪")

    # שינוי שמות עמודות לעברית
    df.columns = [
        "שם_מוצר_מנורמל", "מותג", "אחסון", "RAM", "דור", "מחיר_מינימלי", "מספר_הופעות"
    ]

    df.to_excel(filename, index=False)
    print(f"✅ הקובץ נשמר: {filename}")

# -------------------------------------------------------
# 5. הרצה ראשית
# -------------------------------------------------------
if __name__ == "__main__":
    print("🔄 שולח נתונים ל-Claude...")
    result = run_dedup(raw_data)

    print("\n📊 תוצאה:")
    for item in result:
        print(f"  {item['product_name']} | {item['min_price']} ₪ | הופעות: {item['occurrences']}")

    save_to_excel(result)
