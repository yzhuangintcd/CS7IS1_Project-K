from collections import defaultdict
from rdflib import Graph, Namespace, RDF

# Define namespaces matching your TTL file
NS1 = Namespace("https://example.org/irish-tourism/")

INPUT_FILE = "output/output_foodspot.ttl"
OUTPUT_FILE = "output/output_foodspot_condensed.ttl"
MAX_PER_COUNTY = 2

# 1. Load the Turtle graph
g = Graph()
g.parse(INPUT_FILE, format="turtle")

# 2. Group FoodSpot subjects by county
# Sort subjects for deterministic selection (e.g., foodspots/1, foodspots/10, ...)
foodspots = sorted(g.subjects(RDF.type, NS1.FoodSpot), key=str)

county_counts = defaultdict(int)
spots_to_remove = set()

for spot in foodspots:
    county = g.value(spot, NS1.locatedInCounty)
    # Normalize URI case (e.g., .../county/Dublin vs .../county/dublin)
    county_key = str(county).lower() if county else "unknown"

    if county_counts[county_key] < MAX_PER_COUNTY:
        county_counts[county_key] += 1
    else:
        spots_to_remove.add(spot)

# 3. Remove only the triples where the subject is a discarded FoodSpot.
# All other triples (counties, venue types, and their rdfs:labels) remain untouched.
for spot in spots_to_remove:
    g.remove((spot, None, None))

# 4. Save the filtered graph
g.serialize(destination=OUTPUT_FILE, format="turtle")

print(f"Kept {sum(county_counts.values())} FoodSpots across {len(county_counts)} counties.")
print(f"Removed {len(spots_to_remove)} FoodSpots. Saved to {OUTPUT_FILE}.")