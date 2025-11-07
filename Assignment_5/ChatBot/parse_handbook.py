import json
from bs4 import BeautifulSoup
import requests

def parse_module_page(html_content):
    """
    Parses the HTML content of a university module page and extracts
    key information into a dictionary.
    
    Args:
        html_content (str): The raw HTML string of the page.
        
    Returns:
        dict: A dictionary containing the extracted module data.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    module_data = {}

    # Helper function to safely get text
    def get_safe_text(element):
        return element.get_text(strip=True) if element else None

    # Helper function to find text next to a <strong> tag in a table row
    def get_table_data(table, strong_text):
        try:
            header = table.find('strong', string=strong_text)
            return header.parent.find_next_sibling('td').get_text(strip=True)
        except AttributeError:
            return None

    # --- 1. Main Title ---
    try:
        module_data['module_title'] = get_safe_text(soup.find('h1', id='bkmrk-page-title'))
    except AttributeError:
        module_data['module_title'] = None

    # --- 2. German Title ---
    try:
        german_title_p = soup.find('p', id='bkmrk-%28in-german%3A-%5Bmodulti-1')
        module_data['german_title'] = german_title_p.get_text(strip=True).replace('(in German:', '').replace(')', '').strip()
    except AttributeError:
        module_data['german_title'] = None

    # --- 3. Module-ID ---
    try:
        module_id_strong = soup.find('strong', string=lambda t: t and 'Module-ID:' in t)
        module_data['module_id'] = module_id_strong.find_next('span').get_text(strip=True)
    except AttributeError:
        module_data['module_id'] = None

    # --- 4. Main Details Table (Link, Responsibility, etc.) ---
    try:
        table1 = soup.find('table', id='bkmrk-verantwortung%3A-verwe')
        if table1:
            # LSF Link
            try:
                link_header = table1.find('strong', string='Link:')
                module_data['lsf_link'] = link_header.parent.find_next_sibling('td').find('a')['href']
            except (AttributeError, TypeError):
                module_data['lsf_link'] = None
            
            # Responsibility & Lecturer
            module_data['responsibility'] = get_table_data(table1, 'Responsibility:')
            module_data['lecturer'] = get_table_data(table1, 'Lecturer:')
            
            # Classes (List)
            try:
                classes_header = table1.find('strong', string='Classes:')
                classes_ul = classes_header.parent.find_next_sibling('td').find('ul')
                module_data['classes'] = [li.get_text(strip=True) for li in classes_ul.find_all('li')]
            except AttributeError:
                module_data['classes'] = []

            # Applicability (has <br> tags)
            try:
                app_header = table1.find('strong', string='Applicability in curriculum:')
                app_td = app_header.parent.find_next_sibling('td')
                # Get text and split by the <br> separator
                module_data['applicability_in_curriculum'] = [s.strip() for s in app_td.get_text(separator='<br>').split('<br>') if s.strip()]
            except AttributeError:
                module_data['applicability_in_curriculum'] = []
    except AttributeError:
        pass # Table 1 not found

    # --- 5. Horizontal Stats Table (Abbreviation, CP, etc.) ---
    try:
        table2 = soup.find('table', attrs={'bgcolor': '#7FB3D9', 'id': 'bkmrk-'})
        data_map = {}
        for td in table2.find_all('td'):
            try:
                header = td.find('strong').get_text(strip=True)
                value = td.find_all('p')[1].get_text(strip=True)
                data_map[header] = value
            except (AttributeError, IndexError):
                continue
        
        module_data['abbreviation'] = data_map.get('Abbreviation')
        try:
            module_data['credit_points'] = int(data_map.get('Credit Points'))
        except (ValueError, TypeError):
            module_data['credit_points'] = None
        module_data['semester'] = data_map.get('Semester')
        module_data['term'] = data_map.get('Term')
        module_data['duration'] = data_map.get('Duration')
        module_data['language'] = data_map.get('Language')
        module_data['level'] = data_map.get('Level')
    except AttributeError:
        pass # Table 2 not found

    # --- 6. Lists (Outcomes, Content) ---
    try:
        outcomes_ul = soup.find('ul', id='bkmrk-can-analyse-discrete')
        module_data['intended_learning_outcomes'] = [li.get_text(strip=True) for li in outcomes_ul.find_all('li')]
    except AttributeError:
        module_data['intended_learning_outcomes'] = []

    try:
        content_ul = soup.find('ul', id='bkmrk-discrete-event-simul')
        module_data['content'] = [li.get_text(strip=True) for li in content_ul.find_all('li')]
    except AttributeError:
        module_data['content'] = []

    # --- 7. Workload ---
    try:
        workload_p = soup.find('p', id='bkmrk-arbeitsaufwand%3A')
        # Get the text node *after* the <strong> tag
        module_data['workload'] = workload_p.find('strong').next_sibling.strip()
    except AttributeError:
        module_data['workload'] = None

    # --- 8. Vertical Tables (Exam, SWS, Prerequisites, etc.) ---
    # Helper for tables with headers in row 1, data in row 2
    def parse_vertical_table(table_id):
        try:
            table = soup.find('table', id=table_id)
            headers = [get_safe_text(h) for h in table.find('tr').find_all('td')]
            values = table.find_all('tr')[1].find_all('td')
            return {headers[i]: values[i] for i in range(len(headers))}
        except (AttributeError, IndexError):
            return {}

    # Exam Table
    exam_data = parse_vertical_table('bkmrk-studien-%2Fpr%C3%BCfungslei')
    module_data['pre_examination_requirements'] = get_safe_text(exam_data.get('Pre-examination requirements:'))
    module_data['type_of_examination'] = get_safe_text(exam_data.get('Type of examination:'))
    try:
        sws_ul = exam_data.get('Teaching method / lecture hours per week (SWS):').find('ul')
        module_data['teaching_method_sws'] = [li.get_text(strip=True) for li in sws_ul.find_all('li')]
    except AttributeError:
        module_data['teaching_method_sws'] = []

    # Prerequisites Table
    prereq_data = parse_vertical_table('bkmrk-voraussetzungen-nach')
    module_data['prerequisites_according_to_examination_regulations'] = get_safe_text(prereq_data.get('Prerequisites according to examination regulations:'))
    module_data['recommended_prerequisites'] = get_safe_text(prereq_data.get('Recommended prerequisites:'))

    # Literature Table
    lit_data = parse_vertical_table('bkmrk-medienformen%3A-litera')
    module_data['media'] = get_safe_text(lit_data.get('Media:'))
    module_data['literature'] = get_safe_text(lit_data.get('Literature:'))
    
    # --- 9. Comments ---
    try:
        comments_p = soup.find('p', id='bkmrk-%5Bliteratur%5D')
        module_data['comments'] = comments_p.find('strong').next_sibling.strip()
    except AttributeError:
        module_data['comments'] = None

    return module_data


# --- Main execution ---
def get_handbook_data():
    base_link = "https://bookstack.cs.ovgu.de/books/msc-data-and-knowledge-engineering-winter-202526-qon/page/"
    links = [
            "https://bookstack.cs.ovgu.de/books/msc-data-and-knowledge-engineering-sommer-2026-vorlaufig-uBY/page/advanced-topics-in-machine-learning",
            "https://bookstack.cs.ovgu.de/books/msc-data-and-knowledge-engineering-winter-202526-qon/page/introduction-to-simulation",    
            "https://bookstack.cs.ovgu.de/books/msc-data-and-knowledge-engineering-winter-202526-qon/page/machine-learning",
            "https://bookstack.cs.ovgu.de/books/msc-data-and-knowledge-engineering-winter-202526-qon/page/learning-generative-models",
            "https://bookstack.cs.ovgu.de/books/msc-data-and-knowledge-engineering-sommer-2026-vorlaufig-uBY/page/introduction-to-deep-learning"
            ]
            # You can add more links here for testing]
    page_details = []
    for link in links:
        print(link)
        response = requests.get(link)
        parsed_data = parse_module_page(response.text)
        page_details.append(parsed_data)

    
    # json_output = json.dumps(page_details, indent=2, ensure_ascii=False)
    # print(json_output)
    # return json_output
    return page_details

if __name__ == "__main__":
    get_handbook_data()