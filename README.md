# Prometheus IP Discovery

Simple frankenstein Python script that scans network subnet using `nmap` for currently live hosts
and then generate Prometheus target files that can be read using Prometheus `file_sd_configs`.

## Preresquites

- Python (3.x)
- nmap

## Usage

1. Clone the repository
``` bash
git clone https://github.com/ndkprd/prometheus-ip-discovery.git
```

2. Navigate to the project directory
``` bash
cd prometheus-ip-discovery
```

3. Run the script
```
python prom-ip-discovery.py --subnet <your_subnet> --label <label_name1=label_value1> <label_name2=label_value2> ...
```

Replace `<your_subnet>` with target subnets (e.g., *10.10.10.0/24*) and then add labels as you like.

4. You can check the generated target file in `output/discovered_targets.yml'.

## Example

``` bash
python prom-ip-discovery.py --subnet 10.10.10.0/24 --label env=prod app=myapp

```

## Prometheus Configuration

```
global:
  scrape_interval: 1m
  scrape_timeout: 15s
  #evaluation_internal: 1m

scrape_configs:

  - job_name: 'blackbox-icmp'
    metrics_path: /probe
    params:
      module: [icmp]
    file_sd_configs:
      - files:
          - output/discovered_targets.yaml
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115

```

## License

This project is licensed under [MIT license](https://mit-license.org/).
