from config import db

# 定义天气模型
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 自增主键
    location = db.Column(db.String(100), nullable=False)  # 地点
    date_time = db.Column(db.String(20), nullable=False)  # 日期时间 (ISO 格式)
    temperature_c = db.Column(db.Float, nullable=False)   # 温度 (摄氏度)
    humidity_pct = db.Column(db.Float, nullable=False)    # 湿度 (%)
    precipitation_mm = db.Column(db.Float, nullable=False)  # 降水量 (毫米)
    wind_speed_kmh = db.Column(db.Float, nullable=False)  # 风速 (公里/小时)

    def __repr__(self):
        return f"<Weather {self.location} at {self.date_time}>"