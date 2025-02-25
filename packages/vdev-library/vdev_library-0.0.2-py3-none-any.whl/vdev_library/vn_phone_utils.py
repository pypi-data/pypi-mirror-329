import re

def find_vietnamese_phone_numbers(text):
    # Mẫu regex cho số điện thoại Việt Nam: bắt đầu bằng +84 hoặc 0, theo sau là 9 hoặc 10 chữ số
    pattern = re.compile(r'(?:(?:\+84)|(?:0))\d{9,10}')
    
    # Tìm tất cả số điện thoại phù hợp
    phone_numbers = pattern.findall(text)
    
    # Thay thế +84 bằng 0 nếu có
    phone_numbers = [num.replace("+84", "0", 1) if num.startswith("+84") else num for num in phone_numbers]
    
    # Gộp các số trùng lặp
    phone_numbers = list(set(phone_numbers))
    
    return phone_numbers