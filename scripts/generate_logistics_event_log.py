import pandas as pd
import random
import argparse
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# CLI Argument Parsing
parser = argparse.ArgumentParser(description="Generate a simulated logistics event log.")
parser.add_argument('--size', choices=['small', 'medium', 'large'], required=True,
                    help="Size of the event log: 'small' (~500 events), 'medium' (~1000 events), or 'large' (~5000 events)")
args = parser.parse_args()

# Parameters based on size
if args.size == 'small':
    num_products = 100
    num_shipments = 30
    num_transports = 15
    target_events = 500
    output_filename = "logistics_event_log_small.csv"

elif args.size == 'medium':
    num_products = 200
    num_shipments = 50
    num_transports = 30
    target_events = 1000
    output_filename = "logistics_event_log_medium.csv"

elif args.size == 'large':
    num_products = 1000
    num_shipments = 300
    num_transports = 150
    target_events = 5000
    output_filename = "logistics_event_log_large.csv"

else:
    raise ValueError("Invalid size argument. Choose 'small', 'medium', or 'large'.")

error_rate = 0.05  # 5% chance of delay/error

# Lists to store events
events = []
event_id = 1
current_time = datetime(2025, 4, 29, 8, 0, 0)

# Functions to create events
def create_event(activity, product=None, shipment=None, transport=None, location=None, status="Normal"):
    global event_id, current_time
    event = {
        "event_id": event_id,
        "activity": activity,
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "product": product,
        "shipment": shipment,
        "transport": transport,
        "location": location,
        "status": status
    }
    events.append(event)
    event_id += 1
    current_time += timedelta(minutes=random.randint(5, 30))  # Random time gap

# Object pools
products = [f"prod_{i+1:03d}" for i in range(num_products)]
shipments = [f"ship_{i+1:03d}" for i in range(num_shipments)]
transports = [f"trans_{i+1:03d}" for i in range(num_transports)]
warehouses = ["Warehouse_A", "Warehouse_B", "Warehouse_C", "Warehouse_D"]
destinations = ["City_X", "City_Y", "City_Z"]

# --- Simulate the process ---

# Create Products and Store them
for product in products:
    create_event("Create Product", product=product, location="Factory")
    create_event("Store Product", product=product, location=random.choice(warehouses))

# Create Shipments
for shipment in shipments:
    create_event("Create Shipment", shipment=shipment, location=random.choice(warehouses))

# Assign Products to Shipments
for product in products:
    assigned_shipment = random.choice(shipments)
    create_event("Assign Product to Shipment", product=product, shipment=assigned_shipment, location=random.choice(warehouses))

# Create Transport Orders
for transport in transports:
    create_event("Create Transport Order", transport=transport, location=random.choice(warehouses))

# Load Shipments onto Transport
for shipment in shipments:
    assigned_transport = random.choice(transports)
    create_event("Load Shipment on Transport", shipment=shipment, transport=assigned_transport, location=random.choice(warehouses))

# Start Transport
for transport in transports:
    status = "Delayed" if random.random() < error_rate else "Normal"
    create_event("Start Transport", transport=transport, location="On Road", status=status)

# Deliver Products
for product in products:
    assigned_shipment = random.choice(shipments)
    assigned_transport = random.choice(transports)
    status = "Delayed" if random.random() < error_rate else "Normal"
    create_event("Deliver Product", product=product, shipment=assigned_shipment, transport=assigned_transport, location=random.choice(destinations), status=status)

# Truncate if events exceed target
events = events[:target_events]

# Convert to DataFrame
df = pd.DataFrame(events)

# Save to CSV inside data/ folder
df.to_csv(f"data/{output_filename}", index=False)

print(f"✅ Event log generated: {output_filename} with {len(df)} events.")


#example usage
#python scripts/generate_logistics_event_log.py --size small
#python scripts/generate_logistics_event_log.py --size medium
#python scripts/generate_logistics_event_log.py --size large
