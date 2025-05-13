from flask import Flask, render_template, request, jsonify
from config import db
from models import Weather

app = Flask(__name__)

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 初始化数据库对象
db.init_app(app)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/weather', methods=["GET"])
def weather():
    # weather_data = Weather.query.all()
    # cities = db.session.query(Weather.location).distinct()
    cities = db.session.execute(db.select(Weather.location).distinct()).scalars().all()
    return render_template('weather.html', cities=cities)


@app.route('/weather/<city>')
def weather_city(city):
    weather_data = Weather.query.filter_by(location=city).order_by(Weather.date_time).limit(100).all()
    
    data = {
        "date_time": [wd.date_time for wd in weather_data],
        "temperature_c": [wd.temperature_c for wd in weather_data],
        "humidity_pct": [wd.humidity_pct for wd in weather_data],
        "precipitation_mm": [wd.precipitation_mm for wd in weather_data],
        "wind_speed_kmh": [wd.wind_speed_kmh for wd in weather_data],
    }

    return jsonify(data)


@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        data = request.json.get('data')
        for row in data[1:]:
            if len(row) == 6:
                new_record = Weather(
                    location=row[0].strip(),
                    date_time=row[1].strip(),
                    temperature_c=float(row[2].strip()),
                    humidity_pct=float(row[3].strip()),
                    precipitation_mm=float(row[4].strip()),
                    wind_speed_kmh=float(row[5].strip())
                )
                db.session.add(new_record)
        db.session.commit()
        return jsonify({'message': '数据上传成功！'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'上传失败: {str(e)}'}), 500



if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )