#!/usr/bin/env python3
import argparse
import pickle
import base64
import sys
from libs.knock import rule_templates, read_rules

def generate_knocking_rules(rules = []) -> list:
    knock_rules = []
    initial_rule = rules[0]
    initial_rule.update({'target_address_list': 'KNOCK-0'})
    knock_rules.append(rule_templates[initial_rule['type']][0].format(**initial_rule))
    final_rule = rules[-2]
    final_rule.update({'src_address_list': f"KNOCK-{len(rules)-1}", 'target_address_list': 'KNOCK-ACCEPT'})
    accept_rule = rules[-1]
    accept_rule.update({'src_address_list': 'KNOCK-ACCEPT'})
    rules = rules[0:-2]
    for rule in rules:
        rule.update({'src_address_list': f"KNOCK-{rules.index(rule)+1}", 'target_address_list': f"KNOCK-{rules.index(rule)+2}"})
        knock_rules.append(rule_templates[rule['type']][1].format(**rule))
    knock_rules.append(rule_templates[final_rule['type']][2].format(**final_rule))
    knock_rules.append(rule_templates[accept_rule['type']].format(**accept_rule))
    return knock_rules

def main():
    """
    CLI function to generate Mikrotik knock rules.
    """
    parser = argparse.ArgumentParser(description="Generate Mikrotik knock rules")
    parser.add_argument("--input", "-i", type=str, help="Input file with base64 encoded chain", default=None)

    args = parser.parse_args()

    if args.input is not None:
        print(f"Input file: {args.input}")
        chain = read_rules(args.input)
    else:
        print("No input file specified.")
        sys.exit(1)

    rules = generate_knocking_rules(chain)
    for rule in rules:
        print(rule)

if __name__ == "__main__":
    main()
