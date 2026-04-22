def calculate_bmi(weight: float, height_cm: float) -> float:
    """计算BMI"""
    height_m = height_cm / 100
    return weight / (height_m ** 2)


def get_bmi_status(bmi: float) -> str:
    """获取BMI状态"""
    if bmi < 18.5:
        return "偏瘦"
    elif bmi < 24:
        return "正常"
    elif bmi < 28:
        return "超重"
    else:
        return "肥胖"


def calculate_ideal_weight(height_cm: float) -> tuple[float, float]:
    """计算理想体重范围（BMI 18.5-24）"""
    height_m = height_cm / 100
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24 * (height_m ** 2)
    return (min_weight, max_weight)


def get_body_fat_status(body_fat: float, gender: str) -> str:
    """获取体脂状态"""
    if gender == "male":
        if body_fat < 10:
            return "偏低"
        elif body_fat < 20:
            return "正常"
        elif body_fat < 25:
            return "偏高"
        else:
            return "过高"
    else:
        if body_fat < 20:
            return "偏低"
        elif body_fat < 30:
            return "正常"
        elif body_fat < 35:
            return "偏高"
        else:
            return "过高"


def calculate_all_metrics(measurement: dict, user: dict) -> dict:
    """计算所有健康指标"""
    weight = measurement.get("weight", 0)
    height = user.get("height", 170)
    body_fat = measurement.get("body_fat_percent")
    gender = user.get("gender", "male")
    
    bmi = calculate_bmi(weight, height)
    bmi_status = get_bmi_status(bmi)
    ideal_range = calculate_ideal_weight(height)
    
    result = {
        "bmi": round(bmi, 1),
        "bmi_status": bmi_status,
        "ideal_weight_range": (round(ideal_range[0], 1), round(ideal_range[1], 1)),
    }
    
    if body_fat is not None:
        result["body_fat_status"] = get_body_fat_status(body_fat, gender)
    
    return result