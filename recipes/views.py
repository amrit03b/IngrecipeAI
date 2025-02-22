from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
import random
import json
import re
import os
from dotenv import load_dotenv
load_dotenv()


def land(request):
    return render(request, 'landingPage.html')


def getresponse(request):
    if len(request.GET) != 0:
        ingredient = request.GET.get("ingredient")
        meal_type = request.GET.get("meal_type")
        equipment = request.GET.getlist("equipment")
        time = request.GET.get('time')
        height = request.GET.get('height')  # Get user height in cm
        weight = request.GET.get('weight')  # Get user weight in kg

        # Validate input
        if not ingredient or len(ingredient) < 1 or not height or not weight:
            return render(request, "notFound.html")

        try:
            height = float(height) / 100  # Convert height to meters
            weight = float(weight)
            bmi = weight / (height ** 2)  # Calculate BMI
        except ValueError:
            return render(request, "notFound.html")

        # Determine BMI category
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            bmi_category = "Normal weight"
        elif 25 <= bmi < 29.9:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        prompt = (f"User's BMI category: {bmi_category}. "
                  f"Suggest three Indian-style recipes based on the user's health. "
                  f"Ingredients: {ingredient}, Meal: {meal_type}, Time: {time}, Equipment: {equipment}")

        api_key = os.getenv('API_KEY')
        external_user_id = random.choice(api_key)

        # Create Chat Session
        create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
        create_session_headers = {'apikey': api_key}
        create_session_body = {"pluginIds": [], "externalUserId": external_user_id}

        response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
        response_data = response.json()
        session_id = response_data['data']['id']

        # Submit Query
        submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        submit_query_headers = {'apikey': api_key}
        submit_query_body = {
            "endpointId": "predefined-openai-gpt4o",
            "query": prompt,
            "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
            "responseMode": "sync",
            "modelConfigs": {
                "fulfillmentPrompt": (
                    "Considering the user's BMI category ({bmi_category}), suggest three Indian-style recipes that align with their health goals. "
                    "Ensure the recipes are well-balanced, keeping in mind calorie intake and nutritional requirements. "
                    "Provide the recipes in JSON format with fields: name, preparation_time (with unit), "
                    "macros (with unit) (calories, protein, carbohydrates, fats), ingredients, and instructions."
                )
            }
        }

        query_response = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body)
        query_response_data = query_response.json()

        try:
            answer_text = query_response_data['data']['answer']
        except:
            return render(request, "notFound.html")

        json_str = re.sub(r'```json|```', '', answer_text)

        try:
            recipes = json.loads(json_str)
        except:
            return render(request, "notFound.html")

        return render(request, "result.html", {'recipes': recipes})

    return render(request, 'getPrompt.html')


def about(request):
    return render(request, 'about.html')
