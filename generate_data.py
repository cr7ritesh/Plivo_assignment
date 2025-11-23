"""
Generate synthetic noisy STT training data with PII entities.

Simulates realistic Speech-to-Text transcription errors:
- Spelled-out numbers (e.g., "four one five" instead of "415")
- "dot" instead of "."
- "at" instead of "@"
- No punctuation
- Lowercase text
- Occasional word substitutions/errors
"""
import json
import random
from typing import List, Dict, Tuple

# Sample data pools
FIRST_NAMES = [
    "john", "mary", "michael", "sarah", "david", "jennifer", "robert", "linda",
    "james", "patricia", "william", "barbara", "richard", "elizabeth", "joseph",
    "susan", "thomas", "jessica", "charles", "karen", "daniel", "nancy", "matthew",
    "lisa", "anthony", "betty", "mark", "margaret", "donald", "sandra", "steven",
    "ashley", "paul", "kimberly", "andrew", "emily", "joshua", "donna", "kenneth",
    "michelle", "kevin", "carol", "brian", "amanda", "george", "melissa", "edward",
    "deborah", "ronald", "stephanie", "timothy", "rebecca", "jason", "sharon"
]

LAST_NAMES = [
    "smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis",
    "rodriguez", "martinez", "hernandez", "lopez", "gonzalez", "wilson", "anderson",
    "thomas", "taylor", "moore", "jackson", "martin", "lee", "perez", "thompson",
    "white", "harris", "sanchez", "clark", "ramirez", "lewis", "robinson", "walker",
    "young", "allen", "king", "wright", "scott", "torres", "nguyen", "hill", "flores",
    "green", "adams", "nelson", "baker", "hall", "rivera", "campbell", "mitchell"
]

CITIES = [
    "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia",
    "san antonio", "san diego", "dallas", "san jose", "austin", "jacksonville",
    "fort worth", "columbus", "charlotte", "san francisco", "indianapolis", "seattle",
    "denver", "boston", "nashville", "baltimore", "portland", "las vegas", "detroit",
    "memphis", "louisville", "milwaukee", "albuquerque", "tucson", "fresno", "sacramento",
    "kansas city", "atlanta", "miami", "cleveland", "new orleans", "oakland", "minneapolis",
    "tulsa", "tampa", "arlington", "orlando", "st louis", "pittsburgh", "cincinnati"
]

LOCATIONS = [
    "main street", "park avenue", "fifth avenue", "broadway", "wall street",
    "sunset boulevard", "michigan avenue", "market street", "central park",
    "times square", "golden gate bridge", "empire state building", "madison square garden",
    "oak street", "maple avenue", "elm street", "washington street", "first street",
    "second avenue", "third street", "lake shore drive", "river road", "hill street",
    "pine street", "cedar lane", "birch avenue", "willow street", "cherry lane"
]

EMAIL_DOMAINS = ["gmail dot com", "yahoo dot com", "hotmail dot com", "outlook dot com", 
                "icloud dot com", "aol dot com", "mail dot com", "protonmail dot com"]

TEMPLATES = [
    # Credit card templates
    "my credit card number is {credit_card}",
    "the card number is {credit_card}",
    "you can charge {credit_card}",
    "please use card {credit_card}",
    "my card is {credit_card}",
    
    # Phone templates
    "call me at {phone}",
    "my phone number is {phone}",
    "reach me on {phone}",
    "you can contact me at {phone}",
    "my number is {phone}",
    
    # Email templates
    "email me at {email}",
    "my email is {email}",
    "send it to {email}",
    "contact {email}",
    "reach out at {email}",
    
    # Name templates
    "my name is {person_name}",
    "this is {person_name}",
    "im {person_name}",
    "call me {person_name}",
    "i am {person_name}",
    
    # Date templates
    "on {date}",
    "scheduled for {date}",
    "meeting on {date}",
    "due date is {date}",
    "appointment on {date}",
    
    # Mixed templates
    "hi this is {person_name} my number is {phone}",
    "im {person_name} from {city} email me at {email}",
    "{person_name} at {email} phone {phone}",
    "my name is {person_name} i live in {city} on {location}",
    "contact {person_name} at {email} or {phone}",
    "{person_name} scheduled for {date} at {location}",
    "meeting with {person_name} on {date} in {city}",
    "call {person_name} at {phone} regarding {date} appointment",
    "email {email} or call {phone} for {person_name}",
    "im {person_name} my credit card is {credit_card} expiring {date}",
]

def number_to_words(n: int) -> str:
    """Convert number to spoken form."""
    digit_map = {
        '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
        '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
    }
    return ' '.join(digit_map[d] for d in str(n))

def generate_credit_card() -> Tuple[str, str]:
    """Generate credit card number in spoken form."""
    # Generate 16-digit number
    cc_numeric = ''.join([str(random.randint(0, 9)) for _ in range(16)])
    
    # Randomly choose format: all digits spoken, or grouped
    if random.random() < 0.5:
        # All digits: "four one two three..."
        cc_spoken = number_to_words(cc_numeric).replace(' ', ' ')
    else:
        # Grouped: "four one two three space five six..."
        groups = [cc_numeric[i:i+4] for i in range(0, 16, 4)]
        cc_spoken = ' '.join([number_to_words(g) for g in groups])
    
    return cc_spoken, cc_numeric

def generate_phone() -> Tuple[str, str]:
    """Generate phone number in spoken form."""
    # Format: (XXX) XXX-XXXX
    area = random.randint(200, 999)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    
    # Spoken form variations
    variations = [
        f"{number_to_words(area)} {number_to_words(prefix)} {number_to_words(line)}",
        f"{area} {number_to_words(prefix)} {number_to_words(line)}",
        f"{number_to_words(area)} {prefix} {line}",
    ]
    
    spoken = random.choice(variations)
    numeric = f"{area}{prefix}{line}"
    
    return spoken, numeric

def generate_email() -> Tuple[str, str]:
    """Generate email in spoken form."""
    username = random.choice(FIRST_NAMES) + str(random.randint(1, 999))
    domain = random.choice(EMAIL_DOMAINS)
    
    spoken = f"{username} at {domain}"
    actual = spoken.replace(" at ", "@").replace(" dot ", ".")
    
    return spoken, actual

def generate_person_name() -> str:
    """Generate person name."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"

def generate_date() -> str:
    """Generate date in spoken form."""
    months = ["january", "february", "march", "april", "may", "june",
              "july", "august", "september", "october", "november", "december"]
    
    month = random.choice(months)
    day = random.randint(1, 28)
    year = random.randint(2020, 2025)
    
    # Variations
    variations = [
        f"{month} {day} {year}",
        f"{month} {number_to_words(day)} {year}",
        f"{month} {day}",
        f"{day} {month} {year}",
    ]
    
    return random.choice(variations)

def generate_city() -> str:
    """Generate city name."""
    return random.choice(CITIES)

def generate_location() -> str:
    """Generate location/address."""
    street_num = random.randint(1, 9999)
    street = random.choice(LOCATIONS)
    
    variations = [
        street,
        f"{street_num} {street}",
        f"{number_to_words(street_num)} {street}",
    ]
    
    return random.choice(variations)

def add_stt_noise(text: str) -> str:
    """Add realistic STT noise to text."""
    # Random word errors
    if random.random() < 0.1:
        words = text.split()
        if len(words) > 2:
            idx = random.randint(0, len(words)-1)
            # Skip entity words
            words[idx] = random.choice(["um", "uh", "like", "you know"])
            text = ' '.join(words)
    
    return text

def generate_example(example_id: int) -> Dict:
    """Generate one training example."""
    template = random.choice(TEMPLATES)
    text = template
    entities = []
    
    # Track character positions
    offset = 0
    
    # Generate entities based on template placeholders
    generators = {
        'credit_card': lambda: generate_credit_card()[0],
        'phone': lambda: generate_phone()[0],
        'email': lambda: generate_email()[0],
        'person_name': generate_person_name,
        'date': generate_date,
        'city': generate_city,
        'location': generate_location,
    }
    
    # Find all placeholders and replace
    for entity_type, generator in generators.items():
        placeholder = f"{{{entity_type}}}"
        if placeholder in template:
            entity_value = generator()
            start_pos = text.find(placeholder)
            
            # Replace placeholder
            text = text.replace(placeholder, entity_value, 1)
            
            # Add entity annotation
            end_pos = start_pos + len(entity_value)
            
            # Map entity type to label
            label_map = {
                'credit_card': 'CREDIT_CARD',
                'phone': 'PHONE',
                'email': 'EMAIL',
                'person_name': 'PERSON_NAME',
                'date': 'DATE',
                'city': 'CITY',
                'location': 'LOCATION',
            }
            
            entities.append({
                "start": start_pos,
                "end": end_pos,
                "label": label_map[entity_type]
            })
    
    # Add STT noise
    text = add_stt_noise(text)
    
    # Sort entities by start position
    entities.sort(key=lambda x: x['start'])
    
    return {
        "id": f"utt_{example_id:04d}",
        "text": text,
        "entities": entities
    }

def generate_dataset(num_examples: int, start_id: int = 0) -> List[Dict]:
    """Generate multiple examples."""
    return [generate_example(start_id + i) for i in range(num_examples)]

def main():
    random.seed(42)
    
    # Generate training data (800 examples)
    print("Generating training data...")
    train_data = generate_dataset(800, start_id=0)
    with open("data/train.jsonl", "w", encoding="utf-8") as f:
        for example in train_data:
            f.write(json.dumps(example) + "\n")
    print(f"Generated {len(train_data)} training examples")
    
    # Generate dev data (150 examples)
    print("Generating dev data...")
    dev_data = generate_dataset(150, start_id=1000)
    with open("data/dev.jsonl", "w", encoding="utf-8") as f:
        for example in dev_data:
            f.write(json.dumps(example) + "\n")
    print(f"Generated {len(dev_data)} dev examples")
    
    # Generate test data (100 examples, no labels - just keep entities empty for now)
    print("Generating test data...")
    test_data = generate_dataset(100, start_id=2000)
    # Remove labels for test set
    for example in test_data:
        example['entities'] = []
    with open("data/test.jsonl", "w", encoding="utf-8") as f:
        for example in test_data:
            f.write(json.dumps(example) + "\n")
    print(f"Generated {len(test_data)} test examples")
    
    print("\nSample training example:")
    print(json.dumps(train_data[0], indent=2))
    print("\nData generation complete!")

if __name__ == "__main__":
    main()
