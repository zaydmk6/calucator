from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/visit', methods=['GET'])
def visit():
    uid = request.args.get('uid')  # استخراج UID من الرابط
    if not uid:
        return jsonify({"error": "يجب إرسال UID"}), 400
    
    # إرجاع نفس تنسيق بيانات Darkvisit
    response = {
        "message": "1 requests sent successfully",
        "results": [None],
        "status": "success"
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)