#!/usr/bin/env python3
import argparse
import sys
import pickle
import base64
import random
from libs.knock import event_types, event_fields, write_chain


def generate_knocking_chain(length=3, host='localhost') -> list:
    """
    Generates a knocking chain of specified length.
    """
    events = []
    for i in range(length):
        event_type_id = random.choice(list(event_types.keys()))
        event_type_name = event_types[event_type_id]
        event = {'type': event_type_name}
        for field_name, field_type, field_value in event_fields[event_type_name]:
            if field_type == str:
                if field_name == 'data':
                    event[field_name] = field_value
                elif field_name == 'host':
                    event[field_name] = host
                else:
                    event[field_name] = random.choice(field_value)
            elif field_type == int:
                event[field_name] = random.randint(1, field_value)
            else:
                raise ValueError(f"Unsupported field type: {field_type}")
        events.append(event)
    return events


def main():
    """
    CLI function to generate a knocking chain.
    """
    parser = argparse.ArgumentParser(description="Generate a knocking chain")
    parser.add_argument('--length', '-l', type=int, help="Length of the chain", default=7)
    parser.add_argument('--host', type=str, help="Host", default='localhost')
    parser.add_argument("--output", "-o", type=str, help="Output file", default=None)
    parser.add_argument("--target-port", "-t", type=int, help="Target port", default=None)

    args = parser.parse_args()

    if args.target_port is None:
        print("No target port specified.")
        sys.exit(1)
    chain = generate_knocking_chain(length=args.length, host=args.host)
    chain.append({'type': 'accept_knock', 'port': args.target_port})
    serialized_chain = pickle.dumps(chain)
    encoded_chain = base64.b64encode(serialized_chain)
    print(f"Chain: {encoded_chain.decode('utf-8')}")

    if args.output is not None:
        write_chain(chain, args.output)
        print(f"Chain saved to {args.output}")


if __name__ == "__main__":
    main()
