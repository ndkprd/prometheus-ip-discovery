import subprocess
from jinja2 import Environment, FileSystemLoader
import argparse

def run_nmap(subnet):
    # Run nmap and capture the output
    nmap_command = f'nmap -sn {subnet} -oG -'
    nmap_output = subprocess.check_output(nmap_command, shell=True).decode('utf-8')

    # Extract live hosts and return them as a list
    live_hosts = [line.split()[1] for line in nmap_output.splitlines() if 'Up' in line]
    return live_hosts

def generate_prometheus_config(ip_addresses, labels):
    template_env = Environment(loader=FileSystemLoader('.'))
    template = template_env.get_template('templates/target_template.yml.j2')

    rendered_config = template.render(ip_addresses=ip_addresses, labels=labels)
    with open('output/discovered_targets.yml', 'w') as f:
        f.write(rendered_config)

if __name__ == "__main__":
    # Use argparse to get the subnet and dynamic labels from the command line
    parser = argparse.ArgumentParser(description='Scan network and generate Prometheus config.')
    parser.add_argument('--subnet', required=True, help='Subnet to scan (e.g., 10.10.10.0/24)')
    
    # Dynamic labels (name-value pairs)
    parser.add_argument('--label', nargs='+', action='append', help='Dynamic labels in the format name=value')

    args = parser.parse_args()

    # Step 1: Run nmap and get live hosts
    subnet_to_scan = args.subnet
    live_hosts = run_nmap(subnet_to_scan)

    # Step 2: Parse dynamic labels into a dictionary
    labels = {}
    if args.label:
        for label_pair in args.label:
            for item in label_pair:
                key, value = item.split('=')
                labels[key] = value

    # Step 3: Use live hosts to generate Prometheus config with dynamic labels
    generate_prometheus_config(live_hosts, labels)

