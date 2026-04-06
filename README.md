# ZAP_Product_Deduplication_Assignment
A GenAI-powered solution for product entity resolution and price optimization for ZAP Group.

## עברית

### תיאור הפרויקט
פרויקט זה פותח כחלק ממשימת הבית לתפקיד GenAI Exploration Lead ב-ZAP.
הפתרון מקבל רשימת מוצרים עם כפילויות ושמות לא אחידים, מאחד אותם ומחזיר רשימה מסודרת עם המחיר המינימלי לכל מוצר.

---

### 💡 גישת החשיבה

#### Role Prompting — הגדרת תפקיד
במקום לתת לקלוד הוראות גנריות, הכנסתי אותו לנעליים של **אנליסט נתונים בחברת איקומרס**.
הסיבה: מודל LLM מגיב טוב יותר כשיש לו תפקיד ברור — הוא חושב מתוך הפרספקטיבה הנכונה ומקבל החלטות יותר מדויקות.

#### Chain of Thought — צעד אחרי צעד
חלקתי את המשימה ל-4 שלבים ברורים:
1. ניקוי דאטה
2. זיהוי כפילויות לפי פרמטרים מגדירים
3. סינון רעשים שלא משנים את זהות המוצר
4. הפקת פלט מסודר

הסיבה: Chain of Thought מוכח כמשפר את דיוק המודל במשימות מורכבות — במקום לקבל תוצאה אחת, המודל "חושב בקול" בשלבים.

#### Clear Constraints — דגלים ברורים
הגדרתי במדויק מה **כן** נחשב הבדל (אחסון, RAM, דור תקשורת) ומה **לא** נחשב הבדל (שפה, יבואן, תיאורים שיווקיים).
הסיבה: ללא הגדרות ברורות, המודל עלול לאחד מוצרים שגויים או לפצל מוצרים זהים.

#### User-Centric Output — מיקוד בלקוח
המטרה הסופית היא תמיד הלקוח — הצגת המחיר הנמוך ביותר, ממוין מהזול ליקר.

---

### 🗂️ מבנה הפרויקט
```
zap_project/
├── zap_dedup.py         # קוד Python ראשי
├── README.md            # קובץ זה
└── zap_products_summary.xlsx  # פלט לדוגמה
```

---

### ⚙️ התקנה והרצה

#### דרישות מקדימות
```bash
pip install anthropic pandas openpyxl
```

#### הגדרת API Key
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

#### הרצה
```bash
python zap_dedup.py
```

---

### 📥 קלט לדוגמה
| שם מוצר | מחיר |
|---------|------|
| Samsung Galaxy S23 256GB 8GB RAM 5G | 2,990 ₪ |
| סמסונג גלקסי S23 256GB 8GB RAM 5G יבואן רשמי | 3,100 ₪ |
| Samsung S23 256GB 8GB 5G במבצע! | 2,850 ₪ |
| Samsung Galaxy S23 128GB 8GB RAM 5G | 2,500 ₪ |
| iPhone 15 128GB | 3,500 ₪ |
| אייפון 15 128GB משלוח חינם | 3,600 ₪ |

### 📤 פלט לדוגמה
| שם_מוצר_מנורמל | מותג | אחסון | RAM | דור | מחיר_מינימלי | מספר_הופעות |
|----------------|------|-------|-----|-----|--------------|-------------|
| Samsung Galaxy S23 | Samsung | 128GB | 8GB | 5G | 2,500 ₪ | 1 |
| Samsung Galaxy S23 | Samsung | 256GB | 8GB | 5G | 2,850 ₪ | 3 |
| iPhone 15 | Apple | 128GB | - | - | 3,500 ₪ | 2 |

---

### ⚠️ הנחות ומגבלות
- הפתרון מניח שהדאטה מכיל עמודות `name` ו-`price`
- צבע מוצר מתעלם אלא אם שונה משמעותית
- במקרי ספק — המוצרים נשמרים נפרדים (Conservative approach)

---
---

## English

### Project Description
This project was developed as part of the home assignment for the GenAI Exploration Lead role at ZAP.
The solution receives a list of products with duplicates and inconsistent naming, deduplicates them, and returns a sorted list with the minimum price per product.

---

### 💡 Thought Process

#### Role Prompting — Assigning a Persona
Instead of giving Claude generic instructions, I placed it in the role of an **Ecommerce Data Analyst**.
Reason: LLMs respond more accurately when given a clear role — they reason from the right perspective and make more precise decisions.

#### Chain of Thought — Step by Step
I broke the task into 4 clear steps:
1. Data cleaning
2. Duplicate detection based on defining parameters
3. Noise filtering for attributes that don't affect product identity
4. Structured output generation

Reason: Chain of Thought is proven to improve model accuracy on complex tasks — instead of a single output, the model "thinks aloud" step by step.

#### Clear Constraints — Explicit Flags
I defined precisely what **does** constitute a difference (storage, RAM, network generation) and what **does not** (language, importer name, marketing descriptions).
Reason: Without clear definitions, the model may incorrectly merge different products or split identical ones.

#### User-Centric Output — Customer First
The final goal is always the customer — displaying the lowest price, sorted from cheapest to most expensive.

---

### 🗂️ Project Structure
```
zap_project/
├── zap_dedup.py         # Main Python script
├── README.md            # This file
└── zap_products_summary.xlsx  # Sample output
```

---

### ⚙️ Installation & Usage

#### Prerequisites
```bash
pip install anthropic pandas openpyxl
```

#### Set API Key
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

#### Run
```bash
python zap_dedup.py
```

---

### 📥 Sample Input
| Product Name | Price |
|-------------|-------|
| Samsung Galaxy S23 256GB 8GB RAM 5G | 2,990 ₪ |
| סמסונג גלקסי S23 256GB 8GB RAM 5G יבואן רשמי | 3,100 ₪ |
| Samsung S23 256GB 8GB 5G במבצע! | 2,850 ₪ |
| Samsung Galaxy S23 128GB 8GB RAM 5G | 2,500 ₪ |
| iPhone 15 128GB | 3,500 ₪ |
| אייפון 15 128GB משלוח חינם | 3,600 ₪ |

### 📤 Sample Output
| product_name | brand | storage | ram | generation | min_price | occurrences |
|-------------|-------|---------|-----|------------|-----------|-------------|
| Samsung Galaxy S23 | Samsung | 128GB | 8GB | 5G | 2,500 ₪ | 1 |
| Samsung Galaxy S23 | Samsung | 256GB | 8GB | 5G | 2,850 ₪ | 3 |
| iPhone 15 | Apple | 128GB | - | - | 3,500 ₪ | 2 |

---

### ⚠️ Assumptions & Limitations
- Solution assumes input data contains `name` and `price` columns
- Product color is ignored unless significantly different
- When uncertain — products are kept separate (Conservative approach)

