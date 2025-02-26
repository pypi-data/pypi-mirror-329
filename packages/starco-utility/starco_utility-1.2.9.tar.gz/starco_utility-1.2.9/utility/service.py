from deep_translator import GoogleTranslator
def translator(txt,dest,src='auto'):
    if dest=='ch':dest = 'zh-CN'
    try:return GoogleTranslator(source=src, target=dest).translate(txt)
    except Exception as e:print(e)

import random

def fake_mobile():
    # Valid Iranian mobile prefixes
    prefixes = ['0910', '0911', '0912', '0913', '0914', '0915', '0916', '0917', 
                '0918', '0919', '0990', '0991', '0992', '0993', '0994']
    
    # Select random prefix
    prefix = random.choice(prefixes)
    
    # Generate random 7 digits
    suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    
    # Combine prefix and suffix
    phone_number = prefix + suffix
    
    return phone_number

import random

def fake_email():
    # Iranian names and surnames
    names = ['علی', 'محمد', 'حسین', 'رضا', 'امیر', 'مهدی', 'سارا', 'مریم', 'فاطمه', 'زهرا',
             'امین', 'حسن', 'نیما', 'پویا', 'سینا', 'آرش', 'شیما', 'نازنین', 'پریسا', 'لیلا']
    
    surnames = ['محمدی', 'حسینی', 'رضایی', 'کریمی', 'موسوی', 'هاشمی', 'احمدی', 'اکبری', 'علوی', 'رحیمی',
                'صادقی', 'نجفی', 'عباسی', 'حیدری', 'قاسمی', 'طاهری', 'نوری', 'یوسفی', 'مرادی', 'جعفری']
    
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    
    # Generate unique combinations
    name = random.choice(names)
    surname = random.choice(surnames)
    domain = random.choice(domains)
    
    # Add random number for uniqueness (1-999)
    random_number = random.randint(65, 80)
    
    # Convert Persian names to English transliteration
    name_en = {
        'علی': 'ali', 'محمد': 'mohammad', 'حسین': 'hossein', 'رضا': 'reza',
        'امیر': 'amir', 'مهدی': 'mehdi', 'سارا': 'sara', 'مریم': 'maryam',
        'فاطمه': 'fateme', 'زهرا': 'zahra', 'امین': 'amin', 'حسن': 'hasan',
        'نیما': 'nima', 'پویا': 'pouya', 'سینا': 'sina', 'آرش': 'arash',
        'شیما': 'shima', 'نازنین': 'nazanin', 'پریسا': 'parisa', 'لیلا': 'leila'
    }
    
    surname_en = {
        'محمدی': 'mohammadi', 'حسینی': 'hosseini', 'رضایی': 'rezaei', 'کریمی': 'karimi',
        'موسوی': 'mousavi', 'هاشمی': 'hashemi', 'احمدی': 'ahmadi', 'اکبری': 'akbari',
        'علوی': 'alavi', 'رحیمی': 'rahimi', 'صادقی': 'sadeghi', 'نجفی': 'najafi',
        'عباسی': 'abbasi', 'حیدری': 'heidari', 'قاسمی': 'ghasemi', 'طاهری': 'taheri',
        'نوری': 'nouri', 'یوسفی': 'yousefi', 'مرادی': 'moradi', 'جعفری': 'jafari'
    }
    
    # Create email formats
    formats = [
        f"{name_en[name]}{surname_en[surname]}{random_number}@{domain}",
        f"{name_en[name]}.{surname_en[surname]}{random_number}@{domain}",
        f"{surname_en[surname]}.{name_en[name]}{random_number}@{domain}",
        f"{name_en[name]}_{surname_en[surname]}{random_number}@{domain}"
        f"{name_en[name]}{surname_en[surname]}@{domain}",
        f"{name_en[name]}.{surname_en[surname]}@{domain}",
        f"{surname_en[surname]}.{name_en[name]}@{domain}",
        f"{name_en[name]}_{surname_en[surname]}@{domain}"
    ]
    
    if random.choice([True, False]):
        nickname = generate_nickname()
        formats.extend([
            f"{name_en[name]}{surname_en[surname]}.{nickname}@{domain}",
            f"{name_en[name]}.{surname_en[surname]}@{domain}",
            f"{surname_en[surname]}.{nickname}.{name_en[name]}@{domain}",
            f"{name_en[name]}_{surname_en[surname]}_{nickname}@{domain}"
        ])
    
    return random.choice(formats)

def generate_nickname():
    
    nouns = ['tech', 'pro','wolf', 'dragon', 'hunter','king', 'shadow']
    
    
    return random.choice(nouns).lower()
