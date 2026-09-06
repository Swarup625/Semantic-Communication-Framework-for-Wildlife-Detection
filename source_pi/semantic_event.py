from semantic_builder import build_event
from chunk_generator import generate_chunks

event_zip = build_event()

generate_chunks(event_zip)
