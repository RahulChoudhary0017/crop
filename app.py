from flask import Flask, render_template, request

app = Flask(__name__)

# Crop details dictionary
CROP_DETAILS = {
    "Rice": {
        "image": "/static/images/crop_rice.jpg",
        "hindi": "चावल",
        "season": "Kharif",
        "desc": "Rice is a staple food crop grown in alluvial soil with high rainfall."
    },
    "Cotton": {
        "image": "/static/images/crop_cotton.jpg",
        "hindi": "कपास",
        "season": "Kharif",
        "desc": "Cotton is grown in black soil with warm temperatures."
    },
    "Maize": {
        "image": "/static/images/crop_maize.jpg",
        "hindi": "मक्का",
        "season": "Kharif/Rabi",
        "desc": "Maize is a versatile crop grown in various soils."
    },
    "Wheat": {
        "image": "/static/images/download.jpeg",
        "hindi": "गेहूं",
        "season": "Rabi",
        "desc": "Wheat is a major rabi crop grown in cool climates."
    },
    "Jute": {
        "image": "/static/images/crop_jute.jpg",
        "hindi": "जूट",
        "season": "Kharif",
        "desc": "Jute is a fiber crop grown in warm, humid climates."
    },
    # Add more crops as needed...
}
DEFAULT_IMAGE = "/static/images/download.jpeg"
DEFAULT_HINDI = "NA"
DEFAULT_SEASON = "NA"
DEFAULT_DESC = "No description available."

def predict_crop(soil, temperature, rainfall, ph):
    if soil == "Alluvial" and rainfall > 100 and 20 <= temperature <= 35:
        crop = "Rice"
    elif soil == "Black" and ph < 7 and temperature >= 25:
        crop = "Cotton"
    elif soil == "Red" and ph >= 6.5 and rainfall < 90:
        crop = "Maize"
    else:
        crop = "Wheat"
    details = CROP_DETAILS.get(crop, {})
    image_url = details.get("image", DEFAULT_IMAGE)
    hindi = details.get("hindi", DEFAULT_HINDI)
    season = details.get("season", DEFAULT_SEASON)
    desc = details.get("desc", DEFAULT_DESC)
    return crop, image_url, hindi, season, desc

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    result = None
    error = None
    if request.method == 'POST':
        try:
            soil = request.form.get('soil_type', '').strip()
            temperature = request.form.get('temperature', '').strip()
            rainfall = request.form.get('rainfall', '').strip()
            ph = request.form.get('ph', '').strip()
            if not soil or not temperature or not rainfall or not ph:
                raise ValueError("All fields are required. Please fill in all the details.")
            try:
                temperature = float(temperature)
                rainfall = float(rainfall)
                ph = float(ph)
            except ValueError:
                raise ValueError("Temperature, Rainfall, and pH must be valid numbers.")
            crop, image_url, hindi, season, desc = predict_crop(soil, temperature, rainfall, ph)
            result = {
                'crop': crop,
                'image_url': image_url,
                'hindi': hindi,
                'season': season,
                'desc': desc,
                'soil': soil,
                'temperature': temperature,
                'rainfall': rainfall,
                'ph': ph
            }
        except Exception as e:
            error = str(e)
    return render_template('predict.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
