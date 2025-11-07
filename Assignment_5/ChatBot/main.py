import requests

welcome_message = "Hello! I am your OVGU course assistant. How can I help you today?"

def map_query_to_fields(query):
    prompt = """
        You are an expert in mapping user queries to specific fields in a dataset. You must do this correctly.
          Given a user query, identify the most relevant field from the following list:
            - module_title
            - abbreviation
            - applicability_in_curriculum
            - classes
            - comments
            - content
            - credit_points
            - document
            - duration
            - german_title
            - intended_learning_outcomes
            - language
            - lecturer
            - level
            - literature
            - lsf_link
            - media
            - module_id
            - module_title
            - pre_examination_requirements
            - prerequisites_according_to_examination_regulations
            - recommended_prerequisites
            - responsibility
            - semester
            - teaching_method_sws
            - term
            - title
            - type_of_examination
            - workload

            Example response:

            _source": {
					"module_title": "Introduction to Simulation",
					"german_title": "Introduction to Simulation",
					"module_id": "FIN-INF-120345",
					"lsf_link": "https://lsf.ovgu.de/qislsf/rds?state=wsearchv&search=1&subdir=veranstaltung&veranstaltung.semester=20252&veranstaltung.dtxt=Introduction+to+Simulation&P_start=0&P_anzahl=30&P.sort=veranstaltung.dtxt&_form=display",
					"responsibility": "Graham Horton",
					"lecturer": "Graham Horton",
					"classes": [
						"LectureIntroduction to Simulation",
						"Exercise classIntroduction to Simulation"
					],
					"applicability_in_curriculum": [
						"- M.Sc. DKE: Fundamentals of Data Science",
						"- M.Sc. DE: Grundlagen Informatik"
					],
					"abbreviation": "ItS",
					"credit_points": 6,
					"semester": "Winter",
					"term": "ab 1.",
					"duration": "1 Semester",
					"language": "english",
					"level": "Master",
					"intended_learning_outcomes": [
						"can analyse discrete, continuous and hybrid systems using a professional simulation tool",
						"know how to obtain an accurate result efficiently when integrating initial value problems numerically",
						"can carry out input and output analysis to obtain statistically significant results for stochastic, discrete-event models",
						"can select an appropriate modelling paradigm for a given situation",
						"can perform a simulation study and interpret its results"
					],
					"content": [
						"discrete-event simulation",
						"random variables and random number generation",
						"statistical data analysis",
						"ordinary differential equations and numerical integration",
						"stochastic Petri nets",
						"the AnyLogic simulation system",
						"discrete-time Markov chains",
						"agent-based simulation"
					],
					"workload": "56 contact hours + 124 h self study",
					"pre_examination_requirements": "",
					"type_of_examination": "2h written exam",
					"teaching_method_sws": [
						"2 SWS lecture",
						"2 SWS exercise class"
					],
					"prerequisites_according_to_examination_regulations": "keine",
					"recommended_prerequisites": "Basic engineering mathematics",
					"media": "",
					"literature": "Banks, Carson, Nelson, Nicol: Discrete-Event System Simulation",
					"comments": null
				}
			}

            and prepare a query like below if user is asking for a specific information.
            Example:

            {
                "query": {
                    "match": {
                        "module_title": "Advanced"
                    }
                }
                You should use query as below if user asks for multiple information. Example:

                {
                    "query": {
                        "bool": {
                        "must": [
                            { "match": { "module_title": "Advanced" } },
                            { "match": { "lecturer": "Andreas" } }
                        ]
                        }
                    }
                    }

                The user query is: "{user_query}"
                Note: Only provide the final query in your response without any additional explanations.
            """
    
    prompt = """
       ### System Persona
You are an expert in mapping user queries to specific fields in a dataset. You must do this correctly.

### Task
You must:
1.  Identify all key **criteria** in the user's query (e.g., a person, a time, a topic).
2.  Map each criterion to the most relevant field from the "Available Fields" list.
3.  Build the correct Elasticsearch query based on the "Query Construction Rules."

---

### 1. Available Fields
- module_title
- abbreviation
- applicability_in_curriculum
- classes
- comments
- content
- credit_points
- ... (and so on) ...
- lecturer
- level
- responsibility
- semester
- title
- workload

---

### 2. Example Data (For Structure Only)
Use this purely to understand field names and value *types*.
```json
{
  "_source": {
    "module_title": "Some Title",
    "lecturer": "A Professor's Name",
    "credit_points": 5,
    "semester": "Winter",
    "level": "Master",
    "content": [ "topic a", "topic b" ],
  }
}
3. Field Mapping Hints
Who? (e.g., "by Andreas") -> lecturer or responsibility

When? (e.g., "in winter") -> semester

What topic? (e.g., "about simulation") -> module_title or content

What level? (e.g., "master's course") -> level

How many credits? (e.g., "6 credits") -> credit_points

4. Query Construction Rules
Rule A: For a single criterion Use a match query. Example User Query: "Show me Advanced modules" Example Output:

JSON

{
  "query": {
    "match": {
      "module_title": "Advanced"
    }
  }
}
Rule B: For multiple criteria Use a bool query with a must clause. Example User Query: "Find Advanced modules by Andreas" Example Output:

JSON

{
  "query": {
    "bool": {
      "must": [
        { "match": { "module_title": "Advanced" } },
        { "match": { "lecturer": "Andreas" } }
      ]
    }
  }
}
5. FINAL INSTRUCTION (VERY IMPORTANT)
You must ONLY use the information from the "User Query to Process" below.

Do NOT use any of the values from the examples (like "Advanced", "Andreas", "Some Title", or "Master") unless the user's query also contains them.

Your entire response must be the JSON query and nothing else.

User Query to Process:
"{user_query}" """
    prompt = prompt.replace("{user_query}", query)
    response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False,  # Set to True for streamed response
        "context":[]
    }
    )

    # Print the generated response

    resp = response.json()["response"]
    # print(resp)


if __name__ == "__main__":
    print(welcome_message)

    while True:
        user_input = input("You: ").lower()
        if user_input in ['exit', 'quit', 'bye']:
            print("ChatBot: Goodbye! Have a great day!")
            break
        else:
            map_query_to_fields(user_input)