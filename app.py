import os
import random
import json
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

@app.route('/')
def land():
    return render_template('landingPage.html')

@app.route('/getstarted/', methods=['GET'])
def getresponse():
    if request.args:
        ingredient = request.args.get('ingredient', '').strip()
        meal_type = request.args.get('meal_type', '').strip()
        dietary_preference = request.args.get('dietary_preference', '').strip()
        time = request.args.get('time', '').strip()
        height = request.args.get('height', '').strip()
        weight = request.args.get('weight', '').strip()
        goal = request.args.get('goal', '').strip()
        cuisine = request.args.get('cuisine', '').strip()
        activity_level = request.args.get('activity_level', '').strip()
        allergies = request.args.getlist('allergies')

        # Set defaults if any are missing
        if not goal:
            goal = 'Not specified'
        if not cuisine:
            cuisine = 'Indian'
        if not activity_level:
            activity_level = 'Not specified'
        if not dietary_preference:
            dietary_preference = 'Not specified'
        if not meal_type:
            meal_type = 'Not specified'

        print(f"[DEBUG] ingredient: {ingredient}, meal_type: {meal_type}, dietary_preference: {dietary_preference}, time: {time}, height: {height}, weight: {weight}, goal: {goal}, cuisine: {cuisine}, activity_level: {activity_level}, allergies: {allergies}")

        if not ingredient or len(ingredient) < 1 or not height or not weight:
            print("[DEBUG] Missing required input.")
            return render_template('notFound.html')
        try:
            height = float(height) / 100
            weight = float(weight)
            bmi = weight / (height ** 2)
            bmi_category = get_bmi_category(bmi)
        except ValueError:
            print("[DEBUG] Invalid height or weight value.")
            return render_template('notFound.html')

        allergies_str = ', '.join(allergies) if allergies else 'None'
        prompt = (
            f"User's BMI is {bmi:.1f} ({bmi_category}). "
            f"Goal: {goal}. "
            f"Dietary preference: {dietary_preference}. "
            f"Cuisine: {cuisine}. "
            f"Activity level: {activity_level}. "
            f"Allergies: {allergies_str}. "
            f"Suggest three {cuisine if cuisine else 'Indian-style'} recipes based on the user's health, goal, and preferences. "
            f"Ingredients: {ingredient}, Meal: {meal_type}, Time: {time}."
        )
        print(f"[DEBUG] Prompt: {prompt}")

        api_key = os.getenv('API_KEY')
        if not api_key:
            print("[DEBUG] API_KEY not found in environment.")
            return render_template('notFound.html')
        external_user_id = random.choice(api_key)

        create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
        create_session_headers = {'apikey': api_key}
        create_session_body = {"pluginIds": [], "externalUserId": external_user_id}

        response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
        try:
            response_data = response.json()
        except Exception as e:
            print(f"[DEBUG] Error parsing session response JSON: {e}")
            print(f"[DEBUG] Raw session response: {response.text}")
            return render_template('notFound.html')
        print(f"[DEBUG] Session response: {response_data}")
        if 'data' not in response_data or 'id' not in response_data['data']:
            print("[DEBUG] Session response missing 'data' or 'id'.")
            return render_template('notFound.html')
        session_id = response_data['data']['id']

        submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        submit_query_headers = {'apikey': api_key}
        submit_query_body = {
            "endpointId": "predefined-openai-gpt4o",
            "query": prompt,
            "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
            "responseMode": "sync",
            "modelConfigs": {
                "fulfillmentPrompt": (
                    f"Considering the user's BMI ({bmi:.1f}, {bmi_category}), goal ({goal}), dietary preference ({dietary_preference}), cuisine ({cuisine}), activity level ({activity_level}), and allergies ({allergies_str}), suggest three {cuisine if cuisine else 'Indian-style'} recipes that align with their health goals. "
                    "Ensure the recipes are well-balanced, keeping in mind calorie intake and nutritional requirements. "
                    "Provide the recipes in JSON format with fields: name, preparation_time (with unit), "
                    "macros (with unit) (calories, protein, carbohydrates, fats), ingredients, and instructions."
                )
            }
        }

        query_response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
        try:
            query_response_data = query_response.json()
        except Exception as e:
            print(f"[DEBUG] Error parsing query response JSON: {e}")
            print(f"[DEBUG] Raw query response: {query_response.text}")
            return render_template('notFound.html')
        print(f"[DEBUG] Query response: {query_response_data}")

        try:
            answer_text = query_response_data['data']['answer']
        except Exception as e:
            print(f"[DEBUG] No 'answer' in query response: {e}")
            return render_template('notFound.html')

        # Extract JSON array from the answer text
        json_match = re.search(r'\[\s*{.*?}\s*\]', answer_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                recipes = json.loads(json_str)
            except Exception as e:
                print(f"[DEBUG] Error parsing recipes JSON: {e}")
                print(f"[DEBUG] Extracted JSON: {json_str}")
                return render_template('notFound.html')
        else:
            print("[DEBUG] Could not find JSON array in answer text.")
            print(f"[DEBUG] Raw answer text: {answer_text}")
            return render_template('notFound.html')

        print(f"[DEBUG] Parsed recipes: {recipes}")
        return render_template(
            'result.html',
            recipes=recipes,
            bmi=round(bmi, 1),
            bmi_category=bmi_category,
            dietary_preference=dietary_preference,
            goal=goal,
            cuisine=cuisine,
            activity_level=activity_level,
            allergies=allergies
        )
    return render_template('getPrompt.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True) 