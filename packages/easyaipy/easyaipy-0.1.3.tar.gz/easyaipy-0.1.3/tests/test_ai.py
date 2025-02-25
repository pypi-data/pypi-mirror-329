import pdb

# from easyaipy.openai_easy import openai_easy_prompt
from easyaipy.easyai import gemini_easy_prompt, openai_easy_prompt


api_key="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"
gemini_api_key='AIzaSyAHI8a13IiccvdL18f_egZN6Ol2bI8Unfo'

prompts_with_expected_data = [
    ["How many pandas do you see. Give me their imaginary names too.", {'pandas_names': list, 'number_of_pandas': int}],
    ["What are the top 5 highest-grossing movies of all time?", {'movies': list, 'box_office_revenue': list}],
    ["List the planets in the solar system in order of distance from the sun.", {'planets': list}],
    ["Who were the last 5 Nobel Prize winners in Physics?", {'winners': list, 'years': list}],
    ["What are the key differences between Python and Java?", {'differences': list}],
    ["Give me a list of the best-selling books of all time.", {'books': list, 'copies_sold_millions': list}],
    ["Summarize the plot of 'The Matrix'.", {'summary': str, 'main_characters': list}],
    ["What are the major components of an electric car?", {'components': list}],
    ["List the symptoms of the flu.", {'symptoms': list}],
    ["Give me the nutritional breakdown of a banana.", {'calories': int, 'carbohydrates_g': float, 'proteins_g': float, 'fats_g': float}],
    ["What are the fundamental laws of thermodynamics?", {'laws': list}],
    ["How do vaccines work?", {'mechanism': str, 'types_of_vaccines': list}],
    ["What is the Pythagorean theorem and how is it used?", {'theorem': str, 'example_usage': str}],
    ["List the largest deserts in the world by area.", {'deserts': list, 'areas_sq_km': list}],
    ["Who are the richest people in the world right now?", {'people': list, 'net_worth_billion': list}],
    ["What are the key benefits of regular exercise?", {'benefits': list, 'scientific_sources': list}],
    ["Explain the greenhouse effect.", {'explanation': str, 'causes': list, 'impacts': list}],
    ["List the most commonly used data structures in programming.", {'data_structures': list}],
    ["What are the most common cybersecurity threats today?", {'threats': list, 'mitigation_strategies': list}],
    ["Who are the past 5 U.S. presidents?", {'presidents': list, 'years_in_office': list}],
    ["List some renewable energy sources and their advantages.", {'energy_sources': list, 'advantages': list}],
    ["Explain the main steps in machine learning model training.", {'steps': list}],
    ["What are the main causes of climate change?", {'causes': list}],
    ["Describe the water cycle.", {'stages': list, 'importance': str}],
    ["What are the different types of artificial intelligence?", {'types': list, 'examples': list}],
    ["Who painted the Mona Lisa?", {'artist': str, 'year': int}],
    ["List the most popular tourist destinations in Europe.", {'destinations': list, 'countries': list}],
    ["What are the effects of space travel on the human body?", {'effects': list}],
    ["What are the most used Linux distributions?", {'distributions': list}],
    ["Explain the process of nuclear fission.", {'process': str, 'key_elements': list}],
    ["List some famous unsolved mysteries.", {'mysteries': list, 'details': list}],
    ["What are the most commonly used financial investment strategies?", {'strategies': list, 'risk_levels': list}],
    ["Explain the Big Bang Theory in simple terms.", {'explanation': str, 'evidence': list}],
    ["What are the most consumed fruits in the world?", {'fruits': list, 'annual_production_tonnes': list}],
    ["List some of the most influential philosophers in history.", {'philosophers': list, 'key_ideas': list}],
    ["How do airplanes stay in the air?", {'principle': str, 'forces_involved': list}],
    ["What are the major symptoms of Alzheimer's disease?", {'early_symptoms': list, 'late_symptoms': list}],
    ["Describe the process of human digestion.", {'stages': list, 'enzymes_involved': list}],
    ["What are the main differences between classical and quantum mechanics?", {'differences': list}],
    ["List the most commonly used programming paradigms.", {'paradigms': list, 'languages_using_them': list}]
]


def test_openai():
    for i in range(len(prompts_with_expected_data)):
        a = openai_easy_prompt(prompts_with_expected_data[i][0], output_schema=prompts_with_expected_data[i][1],
                               api_key=api_key)
        print(a.choices[0].data_dict)
        print(type(a.choices[0].data_dict))
        if i == 4:
            break


def test_gemini():
    for i in range(len(prompts_with_expected_data)):
        a = gemini_easy_prompt(prompts_with_expected_data[i][0], output_schema=prompts_with_expected_data[i][1],
                               api_key=gemini_api_key)
        print(a)
        print(type(a))
        if i == 4:
            break

test_openai()
test_gemini()
