import openai
openai.api_key = "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"  # usternly
config = {
    "model": "gpt-4",
    "temperature": 1,
    "max_tokens": 2048,
    # Most models have a context length of 2048 tokens (except for the newest models, which support 4096).
    "top_p": 1,
    "presence_penalty": 0.5,  # must be between -2 and 2
    "frequency_penalty": 0.5,  # must be between -2 and 2
}

import json
from icecream import ic

# Read Existing JSON File
with open('organization_data.json') as f:
    data = json.load(f)


for org in data:
    infoprompt = 'Write a ~100 word third-person description about an organization called "'+org["name"]+'" with the following description: "'+org["description"]+'" \n'+'Below is an excerpt taken directly from the about page of '+org["name"]+"'s website: \n"+org["description from about page (written by the organization themselves)"]

    print(infoprompt)

    message = [
        {'role': 'system',
         'content': "Write in a third-person, professional tone."},
        {'role': 'user',
         'content': infoprompt},
    ]

    response = openai.ChatCompletion.create(model=config["model"], messages=message, temperature=config["temperature"],
                                            max_tokens=config["max_tokens"],
                                            presence_penalty=config["presence_penalty"],
                                            frequency_penalty=config["frequency_penalty"], top_p=config["top_p"])

    ic(message, response)
    print(response.choices[0].message.content)
    ic("$" + str(round(response.usage.completion_tokens / 1000 * 0.06 + response.usage.prompt_tokens / 1000 * 0.03, 3)))

    org["generated_description"]=response.choices[0].message.content

# Create new JSON file
with open('organization_data_with_descriptions.json', 'w') as f:
    json.dump(data, f, indent=4)

# Closing file
f.close()


