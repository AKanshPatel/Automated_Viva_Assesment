import json
from pathlib import Path
from typing import Dict, List


class FilterQuestionBank:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.session_file_path = Path("data/sessions") / f"{session_id}.json"
        self.qb_file_path = Path("data/question_bank.json")
        self.selected_topics_by_unit: Dict[str, List[str]] = {}
        self.question_bank: Dict = {}
        self.filtered_qb: Dict[str, Dict[str, List[str]]] = {}

        self.load_qb()
        self.load_selected_topics()

    # Get the question bank from the json file
    def load_qb(self):
        if not self.qb_file_path.exists():
            raise FileNotFoundError(f"Question bank file not found: {self.qb_file_path}")
        with open(self.qb_file_path, 'r') as file:
            self.question_bank = json.load(file)

    # Get the selected topics from the session file
    def load_selected_topics(self):
        if not self.session_file_path.exists():
            raise FileNotFoundError(f"Session file not found: {self.session_file_path}")
        with open(self.session_file_path, 'r') as file:
            session_data = json.load(file)
        self.selected_topics_by_unit = session_data.get("selected_topics", {})

    # Filter the question bank based on selected topics
    def fetch(self, question_bank: Dict):
        filtered = {}
        for unit in question_bank.get("Units", []):
            unit_name = unit.get("Unit Name")
            if unit_name in self.selected_topics_by_unit:
                original_topics = unit.get("Topics", {})
                selected_topics = self.selected_topics_by_unit[unit_name]
                filtered_topics = {
                    topic: original_topics[topic]
                    for topic in selected_topics
                    if topic in original_topics
                }
                if filtered_topics:
                    filtered[unit_name] = filtered_topics
        self.filtered_qb = filtered
    
    # Save the filtered question bank to a json file
    def save_filtered_qb(self):
        output_path = Path("data/sessions") / f"{self.session_id}_filtered_qb.json"
        with open(output_path, 'w') as file:
            json.dump(self.filtered_qb, file, indent=4)
        return output_path

    # Main function to run the filtering process
    def run(self) -> Dict[str, Dict[str, List[str]]]:
        self.fetch(self.question_bank) # Updates the filtered_qb attribute
        self.save_filtered_qb() # Saves the filtered question bank to a file
        return self.filtered_qb # Returns the filtered question bank

if __name__ == "__main__":
    # Example usage
    session_id = "78c1ad84-fa7e-4af6-b86b-bc453678a623"
    filter_qb = FilterQuestionBank(session_id)
    filtered_qb = filter_qb.run()
    print(json.dumps(filtered_qb, indent=4))
    output_path = filter_qb.save_filtered_qb()
    print(f"Filtered question bank saved to: {output_path}")