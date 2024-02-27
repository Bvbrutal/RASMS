def generate_valid_id_card(base_id):
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = "10X98765432"

    # 从基础ID中获取前17位
    id_front_17 = base_id[:17]

    # 计算校验码
    total = sum(int(num) * coef for num, coef in zip(id_front_17, coefficients))
    remainder = total % 11
    check_code = check_codes[remainder]

    # 生成完整的身份证号码
    valid_id_card = id_front_17 + check_code
    return valid_id_card

# 给定的接近身份证号码
base_id = "500382200006244671"[:-1]  # 移除原始身份证号码的最后一位，只保留前17位
valid_id_card = generate_valid_id_card(base_id)
print("符合校验的身份证号码:", valid_id_card)
