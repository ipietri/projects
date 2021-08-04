#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

# Create an instance of the Flask class
app = Flask(__name__)

# Initialize a new Kafka producer
# Set the host and port the producer should contact: Kafka container port 29092
producer = KafkaProducer(bootstrap_servers='kafka:29092')

# Define functions to handle events

# Define a function to send the events to kafka
def log_to_kafka(topic, event):
    # Add http header fields information to the events to have more information about users
    event.update(request.headers)
    # Send encoded events to kafka
    # The json.dumps() method encodes the event into JSON formatted String.
    producer.send(topic, json.dumps(event).encode())

# Define a function to handle the default response
# The route() decorator tells Flask what URL should trigger the function
# The function creates a "key" : "value" pair to define the type of the event
# The function calls the Kafka producer (using the log_to_kafka function) and sends the encoded event to the kafka topic `events`
# The function returns a message to the user
@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

# Define functions to handle the user action of purchasing a sword. Two types of swords are supported: gold and katana
# The route() decorator tells Flask what URL should trigger the function
# The function creates two "key" : "value" pairs to define the type of the event and the type of sword
# The function calls the Kafka producer (using the log_to_kafka function) and sends the encoded event to the kafka topic `events`
# The function returns a message to the user
@app.route("/purchase_a_gold_sword")
def purchase_a_gold_sword():
    purchase_gold_sword_event = {'event_type': 'purchase_sword', 'type': 'gold' }
    log_to_kafka('events', purchase_gold_sword_event)
    return "Gold sword Purchased!\n"

@app.route("/purchase_a_katana_sword")
def purchase_a_katana_sword():
    purchase_katana_sword_event = {'event_type': 'purchase_sword', 'type': 'katana' }
    log_to_kafka('events', purchase_katana_sword_event)
    return "Katana sword Purchased!\n"

# Define functions to handle the user action of joining a guild. Two guilds are available: warriors and crusaders 
# The route() decorator tells Flask what URL should trigger the function
# The function creates two "key" : "value" pairs to define the type of the event and the name of the guild
# The function calls the Kafka producer (using the log_to_kafka function) and sends the encoded event to the kafka topic `events`
# The function returns a message to the user
@app.route("/join_warriors_guild")
def join_warriors_guild():
    join_warriors_guild_event = {'event_type': 'join_guild', 'name': 'warriors' }
    log_to_kafka('events', join_warriors_guild_event)
    return "Joined Warriors Guild!\n"

@app.route("/join_crusaders_guild")
def join_crusaders_guild():
    join_crusaders_guild_event = {'event_type': 'join_guild', 'name': 'crusaders' }
    log_to_kafka('events', join_crusaders_guild_event)
    return "Joined Crusaders Guild!\n"

# Define functions to handle the user action of purchasing a crossbow. Two crossbows are available: small and medium
# The route() decorator tells Flask what URL should trigger the function
# The function creates two "key" : "value" pairs to define the type of the event and the type of crossbow
# The function calls the Kafka producer (using the log_to_kafka function) and sends the encoded event to the kafka topic `events`
# The function returns a message to the user
@app.route("/purchase_a_small_crossbow")
def purchase_a_small_crossbow():
    purchase_small_crossbow_event = {'event_type': 'purchase_crossbow', 'type': 'small' }
    log_to_kafka('events', purchase_small_crossbow_event)
    return "Small Crossbow Purchased!\n"

@app.route("/purchase_a_medium_crossbow")
def purchase_a_medium_crossbow():
    purchase_medium_crossbow_event = {'event_type': 'purchase_crossbow', 'type': 'medium' }
    log_to_kafka('events', purchase_medium_crossbow_event)
    return "Medium Crossbow Purchased!\n"

# Define a function to handle the user action of purchasing a shield. Only one type of shield is available: buckler shield
# The route() decorator tells Flask what URL should trigger the function
# The function creates two "key" : "value" pairs to define the type of the event and the type of shield
# The function calls the Kafka producer (using the log_to_kafka function) and sends the encoded event to the kafka topic `events`
# The function returns a message to the user
@app.route("/purchase_a_shield")
def purchase_a_shield():
    purchase_shield_event = {'event_type': 'purchase_shield', 'type': 'buckler'}
    log_to_kafka('events', purchase_shield_event)
    return "Shield Purchased!\n"
